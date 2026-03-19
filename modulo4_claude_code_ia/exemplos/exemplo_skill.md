# Skill: data-quality-check

Executa uma análise completa de qualidade de dados no DataFrame ou tabela Snowflake atual.

## Uso

```
/data-quality-check
```

Ou com argumentos:

```
/data-quality-check --tabela CONSUMIDORES_UC --schema CADASTRO --exportar
```

## Instruções para Claude

Quando este comando for ativado, execute as seguintes etapas em ordem:

### Passo 1 — Identificar o contexto

Verifique se existe:
- Um DataFrame `df` carregado no ambiente Jupyter atual, OU
- Uma conexão Snowflake ativa e uma tabela especificada pelo usuário

Se não houver contexto claro, pergunte ao usuário qual DataFrame ou tabela analisar.

### Passo 2 — Executar análise de Completude

Calcule o percentual de preenchimento de cada coluna:

```python
completude = pd.DataFrame({
    'campo': df.columns,
    'pct_preenchido': [(df[col].notna() & (df[col].astype(str).str.strip() != '')).sum() / len(df) * 100 for col in df.columns],
    'nulos': [df[col].isnull().sum() for col in df.columns]
}).sort_values('pct_preenchido')

# Status por campo
completude['status'] = completude['pct_preenchido'].apply(
    lambda x: 'CRÍTICO' if x < 80 else ('ATENÇÃO' if x < 95 else 'OK')
)
```

### Passo 3 — Verificar Unicidade

Verifique duplicatas nas chaves primárias conhecidas:
- `cod_consumidor` (se existir)
- `cpf_cnpj` + `nom_municipio` (combinação)
- `num_medidor` (se existir)

### Passo 4 — Verificar Consistência

Para dados de consumidores de energia, aplique:
- Modalidade tarifária vs. classe de consumo (ver CLAUDE.md)
- Consumo médio entre 0 e 500.000 kWh
- Data de última leitura não nula para UCs ativas

### Passo 5 — Detectar Outliers

Para colunas numéricas de consumo, use o método IQR com fator 3.0:

```python
q1 = serie.quantile(0.25)
q3 = serie.quantile(0.75)
iqr = q3 - q1
outliers = serie[(serie < q1 - 3*iqr) | (serie > q3 + 3*iqr)]
```

### Passo 6 — Gerar Relatório

Produza um relatório em Markdown com:

```markdown
## Relatório de Qualidade — [nome da tabela/DataFrame]
**Data:** [data atual]
**Total de registros:** N

### Resumo Executivo
- Score geral de qualidade: X%
- Campos críticos: [lista]
- Ação imediata necessária: [sim/não]

### Completude
[tabela com pct por campo]

### Unicidade
[resultado das verificações de duplicata]

### Consistência
[problemas encontrados]

### Outliers
[lista de registros com valores anômalos]

### Recomendações
1. [prioridade alta]
2. [prioridade média]
```

Se `--exportar` foi especificado, gere também um arquivo Excel:

```python
with pd.ExcelWriter(f'dados/relatorios/qualidade_{datetime.today().strftime("%Y%m%d")}.xlsx') as writer:
    completude.to_excel(writer, sheet_name='Completude', index=False)
    duplicatas.to_excel(writer, sheet_name='Duplicatas', index=False)
    outliers_df.to_excel(writer, sheet_name='Outliers', index=False)
```

## Parâmetros aceitos

| Parâmetro | Tipo | Default | Descrição |
|-----------|------|---------|-----------|
| `--tabela` | str | None | Nome da tabela Snowflake |
| `--schema` | str | CADASTRO | Schema do Snowflake |
| `--exportar` | flag | False | Exportar relatório para Excel |
| `--limiar-completude` | float | 0.80 | Limite mínimo de completude (0-1) |

## Exemplo de saída esperada

```
=== Análise de Qualidade — CONSUMIDORES_UC ===

Completude:
  cpf_cnpj               88.0% [ATENÇÃO]
  dat_ultima_leitura      96.0% [OK]
  num_medidor             98.0% [OK]

Unicidade:
  cod_consumidor: 2 duplicatas encontradas [CRÍTICO]

Consistência:
  Modalidade tarifária inconsistente: 3 registros

Outliers:
  vlr_consumo_medio_kwh: 1 outlier (cod_consumidor=100049, valor=9.999.999 kWh)

Score geral de qualidade: 78.4%
Ação imediata: SIM (duplicatas de chave primária)
```
