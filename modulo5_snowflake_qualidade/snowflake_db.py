"""Conexão e utilitários para o Snowflake.

Este módulo contém a classe e as funções necessárias para leitura e gravação
de dados no Snowflake, com suporte a autenticação por chave privada (PKI).

Funções:
    * read_sql_file           — lê arquivo .sql para string (suporta templates Jinja2)
    * read_sql_to_dataframe   — executa SQL e retorna DataFrame
    * write_dataframe_to_snowflake — grava DataFrame em tabela Snowflake

Classes:
    * SnowflakeDB — gerencia conexão com autenticação por chave privada
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from jinja2 import Template
from snowflake.connector import SnowflakeConnection
from snowflake.connector import connect as snowflake_connect
from snowflake.connector.errors import DatabaseError
from snowflake.connector.pandas_tools import write_pandas

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# ---------------------------------------------------------------------------
# Configuração de conexão (preencha com as credenciais fornecidas)
# ---------------------------------------------------------------------------

SNOWFLAKE_CONFIG = {
    "account": "khb56279.us-east-1",
    "user": "SEU_EMAIL@EMPRESA.COM",
    "private_key_path": "chaves/rsa_key.p8",   # caminho relativo à raiz do projeto
    "private_key_passphrase": "SUA_PASSPHRASE",
    "warehouse": "WH_EQTLINFO",
    "database": "EQTLINFO_HML",
    "schema": "EQTL_MA",
}


# ---------------------------------------------------------------------------
# Utilitários de SQL
# ---------------------------------------------------------------------------

def read_sql_file(sql_file: Union[str, Path], **sql_kwargs) -> str:
    """
    Lê o conteúdo de um arquivo .sql e processa placeholders Jinja2.

    Args:
        sql_file: Caminho do arquivo SQL.
        **sql_kwargs: Variáveis para substituir no template.
            Listas são convertidas para formato IN: ('A', 'B', 'C')

    Returns:
        SQL como string, sem ponto e vírgula final.

    Raises:
        FileNotFoundError: Se o arquivo não existir ou não tiver extensão .sql.

    Exemplo:
        # arquivo query.sql:
        #   SELECT * FROM UC WHERE cod_uf IN ({{ ufs }}) AND ano = {{ ano }}
        query = read_sql_file("query.sql", ufs=["SP", "MG"], ano=2024)
    """
    sql_file = Path(sql_file)

    if sql_file.suffix != ".sql":
        raise FileNotFoundError(f"Arquivo não possui extensão .sql: {sql_file}")
    if not sql_file.exists():
        raise FileNotFoundError(f"Arquivo SQL não encontrado: {sql_file}")

    texto = sql_file.read_text(encoding="utf-8").replace(";", "")

    if sql_kwargs:
        kwargs_formatados = _formatar_kwargs_sql(sql_kwargs)
        return Template(texto).render(**kwargs_formatados)

    return texto


def _formatar_kwargs_sql(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Converte listas/tuplas para strings SQL prontas para IN (...)."""
    resultado = {}
    for chave, valor in kwargs.items():
        if isinstance(valor, (list, tuple)):
            resultado[chave] = ", ".join(f"'{item}'" for item in valor)
        else:
            resultado[chave] = valor
    return resultado


def read_sql_to_dataframe(
    sql_source: Union[str, Path],
    config: Optional[Dict[str, Any]] = None,
    **sql_kwargs,
) -> pd.DataFrame:
    """
    Executa uma query SQL no Snowflake e retorna um DataFrame pandas.

    Args:
        sql_source: Caminho de arquivo .sql OU string com a query.
        config: Dicionário de configuração da conexão. Se None, usa SNOWFLAKE_CONFIG.
        **sql_kwargs: Variáveis para substituir no template SQL.

    Returns:
        DataFrame com os resultados. Colunas em UPPER_CASE (padrão Snowflake).
        Retorna DataFrame vazio se a query não retornar linhas.

    Exemplo:
        df = read_sql_to_dataframe("queries/consumidores.sql", cod_uf=["MA", "PA"])
        df = read_sql_to_dataframe("SELECT COUNT(*) FROM CONSUMIDORES_UC")
    """
    cfg = config or SNOWFLAKE_CONFIG

    if isinstance(sql_source, Path) or (
        isinstance(sql_source, str) and Path(sql_source).suffix == ".sql"
    ):
        query = read_sql_file(sql_source, **sql_kwargs)
    else:
        query = str(sql_source).replace(";", "")

    with SnowflakeDB(**cfg) as db:
        colunas, dados = db.execute_query(query)

    if not colunas or not dados:
        return pd.DataFrame()

    return pd.DataFrame(data=dados, columns=colunas)


def write_dataframe_to_snowflake(
    df: pd.DataFrame,
    table_name: str,
    config: Optional[Dict[str, Any]] = None,
    **write_kwargs,
) -> None:
    """
    Grava um DataFrame em uma tabela do Snowflake.

    Args:
        df: DataFrame a ser gravado.
        table_name: Nome da tabela destino (sem schema — usa o do config).
        config: Configuração da conexão. Se None, usa SNOWFLAKE_CONFIG.
        **write_kwargs: Argumentos extras para write_pandas:
            - chunk_size (int): linhas por lote
            - overwrite (bool): se True, substitui a tabela
            - auto_create_table (bool): cria a tabela se não existir

    Exemplo:
        write_dataframe_to_snowflake(df_resultado, "TB_QUALIDADE_CADASTRO", overwrite=True)
    """
    if df.empty:
        logger.warning("DataFrame vazio — nenhum dado enviado ao Snowflake.")
        return

    cfg = config or SNOWFLAKE_CONFIG

    with SnowflakeDB(**cfg) as db:
        db.write_dataframe(df, table_name, **write_kwargs)


# ---------------------------------------------------------------------------
# Classe principal
# ---------------------------------------------------------------------------

def _exige_conexao(func):
    """Decorador: garante que a conexão foi estabelecida antes de operar."""
    def wrapper(self, *args, **kwargs):
        if not self.connection:
            raise RuntimeError(
                "Conexão não estabelecida. Use o context manager: 'with SnowflakeDB(...) as db:'"
            )
        return func(self, *args, **kwargs)
    return wrapper


class SnowflakeDB:
    """
    Gerencia conexão com o Snowflake usando autenticação por chave privada (PKI).

    Aceita a chave como:
      - ``private_key`` (bytes já serializados no formato DER/PKCS8), OU
      - ``private_key_path`` (caminho para arquivo .p8) + ``private_key_passphrase``

    Suporte a context manager para garantir o fechamento da conexão:

        with SnowflakeDB(**SNOWFLAKE_CONFIG) as db:
            colunas, dados = db.execute_query("SELECT * FROM CONSUMIDORES_UC LIMIT 5")
            df = db.query_to_dataframe("SELECT COUNT(*) FROM CONSUMIDORES_UC")
    """

    def __init__(
        self,
        *,
        account: str,
        user: str,
        warehouse: str,
        database: str,
        schema: str,
        private_key: Optional[bytes] = None,
        private_key_path: Optional[Union[str, Path]] = None,
        private_key_passphrase: Optional[Union[str, bytes]] = None,
        role: Optional[str] = None,
    ) -> None:
        self.account = account
        self.user = user
        self.warehouse = warehouse
        self.database = database
        self.schema = schema
        self.role = role

        self._private_key_bytes: Optional[bytes] = private_key
        self._private_key_path: Optional[Path] = (
            Path(private_key_path) if private_key_path else None
        )
        self._private_key_passphrase: Optional[bytes] = (
            private_key_passphrase.encode()
            if isinstance(private_key_passphrase, str)
            else private_key_passphrase
        )

        self.connection: Optional[SnowflakeConnection] = None
        self.cursor = None

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "SnowflakeDB":
        self.connection = self._conectar()
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self._fechar()
        return False  # não suprime exceções

    # ------------------------------------------------------------------
    # Conexão
    # ------------------------------------------------------------------

    def _conectar(self) -> SnowflakeConnection:
        try:
            logger.info(
                "Conectando ao Snowflake (account=%s, database=%s, schema=%s)...",
                self.account, self.database, self.schema,
            )
            conn = snowflake_connect(
                account=self.account,
                user=self.user,
                private_key=self._obter_chave_privada(),
                warehouse=self.warehouse,
                database=self.database,
                schema=self.schema,
                role=self.role,
            )
            logger.info("Conexão estabelecida com sucesso.")
            return conn
        except DatabaseError as err:
            logger.critical("Erro ao conectar ao Snowflake: %s", err)
            raise

    def _fechar(self) -> None:
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connection:
            self.connection.close()
            self.connection = None
        logger.info("Conexão encerrada.")

    # ------------------------------------------------------------------
    # Operações
    # ------------------------------------------------------------------

    @_exige_conexao
    def execute_query(self, query: str) -> Tuple[List[str], List[tuple]]:
        """
        Executa uma query e retorna (colunas, dados).

        Returns:
            Tupla (lista de nomes de colunas, lista de tuplas com os dados).
            Retorna ([], []) em caso de erro.
        """
        try:
            self.cursor.execute(query)
            colunas = [desc[0] for desc in self.cursor.description]
            dados = self.cursor.fetchall()
            return colunas, dados
        except DatabaseError as err:
            logger.critical("Erro ao executar query: %s", err)
            logger.debug("SQL: %s", query)
            return [], []

    @_exige_conexao
    def query_to_dataframe(self, query: str) -> pd.DataFrame:
        """Atalho: executa query e retorna DataFrame diretamente."""
        colunas, dados = self.execute_query(query)
        if not colunas:
            return pd.DataFrame()
        return pd.DataFrame(data=dados, columns=colunas)

    @_exige_conexao
    def write_dataframe(
        self,
        df: pd.DataFrame,
        table_name: str,
        *,
        chunk_size: Optional[int] = None,
        auto_create_table: bool = False,
        overwrite: bool = False,
    ) -> None:
        """
        Grava um DataFrame em uma tabela Snowflake usando write_pandas.

        Args:
            df: DataFrame a gravar.
            table_name: Nome da tabela destino.
            chunk_size: Número de linhas por lote (None = tudo de uma vez).
            auto_create_table: Cria a tabela se não existir.
            overwrite: Se True, substitui os dados existentes.
        """
        if df.empty:
            logger.warning("DataFrame vazio — nada a gravar em '%s'.", table_name)
            return

        success, nchunks, nrows, _ = write_pandas(
            conn=self.connection,
            df=df,
            table_name=table_name,
            schema=self.schema,
            chunk_size=chunk_size,
            overwrite=overwrite,
            auto_create_table=auto_create_table,
        )

        if not success:
            raise RuntimeError(
                f"Falha ao gravar DataFrame no Snowflake "
                f"(tabela={table_name}, chunks={nchunks}, linhas={nrows})."
            )

        logger.info(
            "DataFrame gravado com sucesso (tabela=%s, linhas=%s, chunks=%s).",
            table_name, nrows, nchunks,
        )

    # ------------------------------------------------------------------
    # Utilitários internos de chave privada
    # ------------------------------------------------------------------

    def _obter_chave_privada(self) -> bytes:
        """Retorna os bytes DER/PKCS8 da chave privada sem criptografia."""
        if self._private_key_bytes:
            return self._private_key_bytes

        if not self._private_key_path:
            raise ValueError(
                "Forneça 'private_key' (bytes) ou 'private_key_path' (caminho do arquivo .p8)."
            )

        return self._carregar_chave_do_arquivo(
            self._private_key_path, self._private_key_passphrase
        )

    @staticmethod
    def _carregar_chave_do_arquivo(
        path: Path, passphrase: Optional[bytes]
    ) -> bytes:
        """Carrega chave PEM ou DER e a converte para DER/PKCS8 sem criptografia."""
        if not path.exists():
            raise FileNotFoundError(f"Arquivo de chave privada não encontrado: {path}")

        key_data = path.read_bytes()

        try:
            chave = serialization.load_pem_private_key(
                key_data, password=passphrase, backend=default_backend()
            )
        except ValueError:
            chave = serialization.load_der_private_key(
                key_data, password=passphrase, backend=default_backend()
            )

        return chave.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
