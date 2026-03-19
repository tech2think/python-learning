# Template de Prompts — Qualidade de Dados de Consumidores

Coleção de prompts prontos para uso no projeto de qualidade de cadastro de UCs.
Substitua os campos entre `[COLCHETES]` antes de usar.

---

## 1. Gerar Função de Validação

```
Contexto:
Sou analista de dados em uma distribuidora de energia elétrica brasileira.
Stack: Python 3.11, pandas 2.2, Snowflake.
Projeto: pipeline de qualidade do cadastro de Unidades Consumidoras (UCs).

Tarefa:
Crie uma função Python para validar a seguinte regra de negócio:
[DESCREVER A REGRA — ex: "consumidores da classe RESIDENCIAL devem ter modalidade B1"]

Estrutura do DataFrame de entrada (`df`):
- cod_consumidor: int (chave primária)
- nom_consumidor: str
- cpf_cnpj: str (CPF=11 dígitos ou CNPJ=14 dígitos sem formatação)
- cod_modalidade_tarifaria: str (B1/B2/B3/B4/A4/A3a/A3/A2/A1/AS)
- cod_classe_consumo: str (RESIDENCIAL/COMERCIAL/INDUSTRIAL/RURAL/PODER PUBLICO/ILUMINACAO PUBLICA)
- vlr_consumo_medio_kwh: float
- flg_ativo: bool

Retorno esperado:
DataFrame com colunas:
- cod_consumidor: int
- nome_regra: str (nome da regra validada)
- status: str ("OK" ou "FALHA")
- detalhe: str (descrição do problema, ou None se OK)

Requisitos técnicos:
- Type hints Python 3.11
- Docstring em português (Google style) com exemplo de uso
- Sem loops explícitos — use operações pandas vetorizadas
- Trate valores nulos nos campos verificados
- Nome da função: validar_[NOME_DA_REGRA]
```

---

## 2. Gerar Query Snowflake de Qualidade

```
Snowflake SQL:
- Account/Database: conforme .env
- Schema: CADASTRO
- Tabela: CONSUMIDORES_UC

Colunas relevantes:
COD_CONSUMIDOR, NOM_CONSUMIDOR, CPF_CNPJ, COD_MODALIDADE_TARIFARIA,
COD_CLASSE_CONSUMO, NOM_MUNICIPIO, COD_UF, NUM_CEP, NUM_MEDIDOR,
FLG_ATIVO, DAT_ULTIMA_LEITURA, VLR_CONSUMO_MEDIO_KWH

Crie uma query que:
[DESCREVER O OBJETIVO DA QUERY]

Requisitos:
- Use CTEs se tiver mais de 2 passos lógicos
- Comentários em português acima de cada CTE
- Alias de colunas em snake_case
- Ordene por: [CAMPO DE ORDENAÇÃO]
- Limite: [N] registros (ou sem limite se análise completa)
- A query será executada via Python com:
  df = pd.read_sql(query, conn)
  Certifique-se de que os tipos sejam compatíveis com pandas.
```

---

## 3. Explicar Resultado Anômalo

```
Contexto:
Estou analisando a qualidade do cadastro de consumidores de energia elétrica.

Recebi o seguinte resultado inesperado:
[COLAR O RESULTADO — ex: saída de print(), tabela, etc.]

Origem dos dados: [ex: "query na tabela CONSUMIDORES_UC, filtrado por cod_uf='SP'"]

Perguntas:
1. O que pode causar este resultado no contexto de uma distribuidora de energia?
2. Qual é o nível de severidade (crítico/atenção/informativo)?
3. Quais verificações adicionais devo fazer para confirmar o problema?
4. Que ação corretiva você recomenda?
5. Como eu priorizaria a correção em relação a outros problemas de qualidade?
```

---

## 4. Refatorar Código para Produção

```
Tenho o seguinte código Python que funciona em Jupyter:
[COLAR O CÓDIGO]

Preciso refatorá-lo para uso em produção com os seguintes requisitos:

1. Transformar em uma classe ou módulo reutilizável
2. Adicionar tratamento de exceções (conexão falha, dados vazios, timeout)
3. Adicionar logging (usar biblioteca `logging`, não `print`)
4. Parametrizar os valores hard-coded (schema, tabela, limites)
5. Adicionar testes básicos (pytest) cobrindo o caminho feliz e casos de erro
6. Documentação completa em português

Stack: Python 3.11, pandas 2.2, snowflake-connector-python 3.12
Estilo: PEP8, max 100 caracteres por linha
```

---

## 5. Gerar Dicionário de Dados

```
Crie um dicionário de dados em Markdown para a seguinte tabela Snowflake:

Tabela: [NOME_DA_TABELA]
Schema: [SCHEMA]
Descrição: [UMA FRASE DESCREVENDO A TABELA]

Colunas:
[COLAR CREATE TABLE ou lista de colunas com tipos]

Para cada coluna, inclua:
- Descrição de negócio (não apenas o tipo técnico)
- Tipo de dado (SQL e equivalente Python/pandas)
- Obrigatório (sim/não)
- Valores possíveis ou domínio (se categórico)
- Regras de qualidade (o que é considerado inválido)
- Exemplo de valor válido

Contexto do negócio:
[DESCREVER O CONTEXTO — ex: "dados do setor de distribuição de energia elétrica, ANEEL, PRODIST"]

Formato de saída: Markdown com tabela e seções por grupo de campos
(identificação, endereço, cadastro técnico, etc.)
```

---

## 6. Debugar Erro

```
Erro ao executar código Python [versão]:
[COLAR A MENSAGEM DE ERRO COMPLETA COM TRACEBACK]

Código que causou o erro:
```python
[COLAR O CÓDIGO]
```

Contexto:
- Ambiente: [Jupyter Lab / script Python / etc.]
- Dados: [descrever o DataFrame ou input que estava sendo processado]
- O que estava tentando fazer: [DESCREVER]

Por favor:
1. Explique a causa raiz do erro
2. Mostre a correção com comentário explicando o que mudou
3. Indique se há outras formas de o mesmo erro ocorrer que devo prevenir
```

---

## Dicas de Uso

- **Seja específico** sobre versões de biblioteca quando o comportamento pode variar
- **Inclua exemplos de dados** (fictícios, nunca dados reais de produção)
- **Especifique o formato de saída** esperado — DataFrame, dict, Excel, etc.
- **Mencione restrições** — "sem loops", "apenas pandas", "compatível com Snowflake"
- **Itere** — se a primeira resposta não for perfeita, refine com "ajuste X para Y"
