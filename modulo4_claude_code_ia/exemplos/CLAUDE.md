# Projeto: Qualidade de Dados — Cadastro de Consumidores

## Contexto de Negócio

Pipeline de verificação e monitoramento da qualidade do cadastro de
Unidades Consumidoras (UCs) de uma distribuidora de energia elétrica brasileira.
Os dados alimentam os sistemas de faturamento e os indicadores regulatórios
reportados à ANEEL (DEC, FEC, PRODIST).

**Área responsável:** Gestão de Dados e Cadastro
**Criticidade:** Alta — erros impactam faturamento e conformidade regulatória

## Stack Tecnológica

- Python 3.11
- pandas 2.2.3
- great-expectations 1.3.x
- snowflake-connector-python 3.12.x
- python-dotenv (credenciais via .env)
- openpyxl (exportação de relatórios)

## Estrutura do Banco de Dados (Snowflake)

- **Account:** ver .env
- **Database:** DB_ENERGIA
- **Schema principal:** CADASTRO
- **Schema staging:** STAGING
- **Schema analytics:** ANALYTICS

### Tabelas principais

| Tabela | Descrição |
|--------|-----------|
| `CADASTRO.CONSUMIDORES_UC` | Cadastro mestre de UCs (tabela principal) |
| `CADASTRO.HISTORICO_LEITURAS` | Histórico de leituras de medidores |
| `CADASTRO.TARIFAS_VIGENTES` | Tarifas vigentes por modalidade |
| `STAGING.UC_IMPORTADAS` | Registros recém-importados (antes de validação) |

### Colunas da tabela CONSUMIDORES_UC

```
COD_CONSUMIDOR          INT       PK
NOM_CONSUMIDOR          VARCHAR
CPF_CNPJ               VARCHAR   CPF=11 dígitos, CNPJ=14 dígitos
COD_MODALIDADE_TARIFARIA VARCHAR  B1/B2/B3/B4/A4/A3a/A3/A2/A1/AS
COD_CLASSE_CONSUMO      VARCHAR   RESIDENCIAL/COMERCIAL/INDUSTRIAL/RURAL/PODER PUBLICO/...
NOM_LOGRADOURO          VARCHAR
NUM_LOGRADOURO          VARCHAR
NOM_BAIRRO              VARCHAR
NOM_MUNICIPIO           VARCHAR
COD_UF                  CHAR(2)
NUM_CEP                 VARCHAR   formato: XXXXX-XXX
NUM_MEDIDOR             BIGINT
DAT_INICIO_VIGENCIA     DATE
DAT_FIM_VIGENCIA        DATE      NULL = vigência em aberto
FLG_ATIVO               BOOLEAN
COD_UNIDADE_CONSUMIDORA VARCHAR
NUM_LATITUDE            FLOAT
NUM_LONGITUDE           FLOAT
DAT_ULTIMA_LEITURA      DATE
VLR_CONSUMO_MEDIO_KWH   FLOAT
```

## Convenções de Código

### Python
- Nomes de funções e variáveis: `snake_case`
- Nomes de classes: `PascalCase`
- Constantes: `UPPER_SNAKE_CASE`
- Docstrings em português, formato Google style
- Type hints obrigatórios em funções públicas
- Sem loops explícitos — use operações pandas vetorizadas

### SQL (Snowflake)
- Palavras-chave SQL em maiúsculas: `SELECT`, `FROM`, `WHERE`
- Nomes de objetos em maiúsculas: `CONSUMIDORES_UC`, `CPF_CNPJ`
- Aliases em snake_case minúsculas: `uc`, `total_consumidores`
- CTEs para queries com mais de 2 passos
- Comentários em português
- Queries parametrizadas: usar `%s` com cursor.execute(), nunca f-strings

### Nomenclatura de arquivos
- Notebooks: `NN_descricao_curta.ipynb` (ex: `01_exploracao.ipynb`)
- Scripts Python: `descricao_funcao.py` (ex: `validacoes_cpf.py`)
- Relatórios gerados: `relatorio_YYYYMM_descricao.xlsx`

## Instruções para Claude

### Como gerar queries

Sempre use CTEs quando a query tiver mais de 2 passos lógicos. Exemplo:

```sql
-- Comentário descrevendo o objetivo
WITH base AS (
    SELECT ...
    FROM CADASTRO.CONSUMIDORES_UC
    WHERE flg_ativo = TRUE
),
agregado AS (
    SELECT ...
    FROM base
    GROUP BY ...
)
SELECT * FROM agregado
ORDER BY coluna_relevante DESC
LIMIT 1000;
```

### Como estruturar funções de validação

```python
def validar_NOME_REGRA(df: pd.DataFrame) -> pd.Series:
    """
    Valida se [DESCREVER REGRA].

    Returns:
        Series booleana onde True indica registro INVÁLIDO.
    """
    return condicao_de_invalidade
```

### Como gerar relatórios

Use a função `gerar_relatorio_excel()` em `src/relatorios.py` como base.
Sempre crie ao menos 3 abas: Resumo, Detalhamento, Metadados.

## Regras de Negócio Importantes

1. **Modalidade tarifária por classe:**
   - `RESIDENCIAL` → somente `B1`
   - `RURAL` → somente `B2`
   - `ILUMINACAO PUBLICA` → somente `B4`
   - `COMERCIAL`, `INDUSTRIAL`, `PODER PUBLICO` → podem ser B3, A4, A3a, A3, A2, A1, AS

2. **Validação de CPF:** verificar dígitos verificadores (não apenas comprimento)

3. **Consumo anormal:** acima de 500.000 kWh/mês para qualquer classe é suspeito

4. **Data de leitura:** deve ser no máximo 45 dias atrás para UCs ativas

## Proibições (NUNCA faça)

- NUNCA execute `DELETE`, `UPDATE` ou `DROP` sem cláusula `WHERE` explícita
- NUNCA commite o arquivo `.env` ou qualquer credencial
- NUNCA use f-strings para montar queries SQL (risco de SQL injection)
- NUNCA salve dados de produção no diretório `dados/amostras/`
- NUNCA imprima CPF/CNPJ completo nos logs — use mascaramento: `xxx.xxx.XXX-XX`

## Comandos Úteis

```bash
# Rodar testes
pytest tests/ -v

# Verificar qualidade do código
flake8 src/ --max-line-length 100
black src/ --check

# Gerar relatório mensal
python scripts/gerar_relatorio_mensal.py --ano 2025 --mes 02

# Testar conexão Snowflake
python scripts/testar_conexao.py
```

## Contatos

- Owner do projeto: time-dados@distribuidora.com.br
- Dúvidas sobre regras de negócio: cadastro@distribuidora.com.br
