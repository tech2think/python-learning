# Módulo 2 — Análise de Dados com Pandas

Pandas é a biblioteca central para análise de dados em Python. Neste módulo trabalhamos com um cadastro simulado de consumidores de energia elétrica.

## Notebooks

| Arquivo | Conteúdo | Duração |
|---------|----------|---------|
| `01_pandas_intro.ipynb` | DataFrames, leitura de CSV, exploração básica | 1h |
| `02_limpeza_dados.ipynb` | Nulos, duplicatas, normalização, validação | 1.5h |
| `03_analise_qualidade_cadastro.ipynb` | Score de qualidade, relatório de problemas | 1.5h |

## Dados

O arquivo `dados/consumidores_simulado.csv` contém **50 registros** com problemas intencionais de qualidade:

| Problema | Ocorrências |
|----------|-------------|
| CPF/CNPJ ausente | 5 registros |
| CPF/CNPJ com formato inválido | 2 registros |
| Registro duplicado (cod_consumidor) | 1 duplicata |
| Nome duplicado com cod diferente | 1 par |
| CEP sem formatação | 1 registro |
| Data de leitura ausente | 2 registros |
| Medidor ausente | 1 registro |
| Consumo outlier (>999.999 kWh) | 1 registro |
| Nome em maiúsculas (inconsistente) | 3 registros |

## Objetivos de Aprendizagem

Ao final deste módulo, você será capaz de:

- Carregar e explorar DataFrames com Pandas
- Identificar e tratar valores nulos
- Detectar e remover duplicatas
- Normalizar strings e converter tipos de dados
- Calcular um score de qualidade por registro
- Gerar um relatório de problemas de qualidade
