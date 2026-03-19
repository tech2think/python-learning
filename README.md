# Curso Python para Distribuição de Energia Elétrica

Curso prático de Python voltado a profissionais do setor de distribuição de energia elétrica, com foco em análise de dados, qualidade de cadastro de consumidores e uso de ferramentas de IA generativa no desenvolvimento.

## Estrutura do Curso

| Parte | Módulo | Tema | Duração |
|-------|--------|------|---------|
| 1 | 1 | Fundamentos Python | 1h15 |
| 1 | 2 | Análise de Dados com Pandas | 1h30 |
| 1 | 3 | Visualização de Indicadores | 45min |
| **1** | | **Total Parte 1** | **3h30** |
| 2 | 4 | Claude Code & IA no Desenvolvimento | 1h30 |
| 2 | 5 | Snowflake & Qualidade de Dados | 2h |
| **2** | | **Total Parte 2** | **3h30** |

## Como usar

### 1. Instalar o uv (gerenciador de pacotes)

```bash
# Linux / Mac
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Configurar ambiente

```bash
# Criar ambiente virtual e instalar dependências (tudo em um comando)
uv sync

# Ativar o ambiente
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

> O `uv` é significativamente mais rápido que pip/conda e gerencia o ambiente automaticamente a partir do `pyproject.toml`.

### 2. Iniciar apresentação
```bash
python serve_apresentacao.py
# Acesse: http://localhost:8080
```

### 3. Iniciar Jupyter
```bash
jupyter lab
```

## Contexto do Projeto

O projeto de qualidade de dados foca no **cadastro de consumidores** — validação, enriquecimento e monitoramento dos dados que alimentam os sistemas de faturamento e indicadores regulatórios (DEC, FEC, ANEEL/PRODIST).
