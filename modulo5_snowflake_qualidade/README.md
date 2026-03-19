# Módulo 5 — Snowflake & Qualidade de Dados

Conecte Python ao Snowflake e construa um pipeline completo de qualidade de dados do cadastro de consumidores.

## Notebooks

| Arquivo | Conteúdo | Duração |
|---------|----------|---------|
| `01_conexao_snowflake.ipynb` | Conexão, autenticação, queries básicas | 1h |
| `02_analise_qualidade_dados.ipynb` | Verificações de qualidade via Snowflake | 1.5h |
| `03_queries_avancadas.ipynb` | CTEs, window functions, séries temporais | 1.5h |

## Configuração

Crie um arquivo `.env` na raiz do projeto com as credenciais fornecidas pelo instrutor:

```
SF_ACCOUNT=seu-account-aqui
SF_USER=seu-usuario
SF_PASSWORD=sua-senha
SF_WAREHOUSE=COMPUTE_WH
SF_DATABASE=DB_ENERGIA
SF_SCHEMA=CADASTRO
SF_ROLE=ANALYST
```

**Importante:** Nunca commite o arquivo `.env` no git!

## Dependências

```bash
pip install snowflake-connector-python python-dotenv
```

## Recursos

- Documentação Snowflake: docs.snowflake.com
- Connector Python: docs.snowflake.com/en/developer-guide/python-connector
- Arquivo de dicionário de dados: `documentacao/dicionario_dados.md`
