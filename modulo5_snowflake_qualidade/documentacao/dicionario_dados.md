# Dicionário de Dados — CADASTRO.CONSUMIDORES_UC

**Tabela:** `CONSUMIDORES_UC`
**Schema:** `CADASTRO`
**Database:** `DB_ENERGIA`
**Descrição:** Cadastro mestre de Unidades Consumidoras (UCs) da distribuidora. Contém todos os dados cadastrais, tarifários e de endereço de cada ponto de fornecimento de energia elétrica.

**Atualização:** Diária (via carga do sistema de faturamento)
**Owner:** Equipe de Gestão de Dados
**Criticidade:** Alta — alimenta faturamento, indicadores ANEEL e relatórios regulatórios

---

## Grupos de Campos

### 1. Identificação

| Campo | Tipo SQL | Tipo Python | Obrigatório | Descrição |
|-------|----------|-------------|-------------|-----------|
| `COD_CONSUMIDOR` | `BIGINT` | `int` | Sim (PK) | Código único do consumidor no sistema de faturamento. Chave primária da tabela. Gerado automaticamente pelo sistema. |
| `NOM_CONSUMIDOR` | `VARCHAR(200)` | `str` | Sim | Nome completo do consumidor (pessoa física) ou razão social (pessoa jurídica). Deve estar em formato Title Case. |
| `CPF_CNPJ` | `VARCHAR(14)` | `str` | Não | Documento do consumidor sem formatação. CPF: 11 dígitos. CNPJ: 14 dígitos. |
| `COD_UNIDADE_CONSUMIDORA` | `VARCHAR(20)` | `str` | Sim | Código da unidade consumidora no sistema de distribuição. Diferente do cod_consumidor — um consumidor pode ter múltiplas UCs. |

**Regras de qualidade — Identificação:**
- `COD_CONSUMIDOR` não pode ser nulo nem duplicado
- `CPF_CNPJ` deve ter exatamente 11 (CPF) ou 14 (CNPJ) dígitos após remoção de caracteres especiais
- CPFs com todos os dígitos iguais (ex: 111.111.111-11) são inválidos
- `NOM_CONSUMIDOR` não pode ter menos de 3 caracteres

---

### 2. Classificação Tarifária

| Campo | Tipo SQL | Tipo Python | Obrigatório | Valores possíveis |
|-------|----------|-------------|-------------|-------------------|
| `COD_MODALIDADE_TARIFARIA` | `VARCHAR(5)` | `str` | Sim | `B1`, `B2`, `B3`, `B4`, `A4`, `A3a`, `A3`, `A2`, `A1`, `AS` |
| `COD_CLASSE_CONSUMO` | `VARCHAR(30)` | `str` | Sim | `RESIDENCIAL`, `COMERCIAL`, `INDUSTRIAL`, `RURAL`, `PODER PUBLICO`, `ILUMINACAO PUBLICA`, `SERVICO PUBLICO` |

**Detalhamento das modalidades tarifárias (conforme PRODIST/ANEEL):**

| Modalidade | Grupo | Tensão de fornecimento | Classes permitidas |
|------------|-------|------------------------|-------------------|
| `B1` | B (Baixa Tensão) | < 1 kV | RESIDENCIAL |
| `B2` | B (Baixa Tensão) | < 1 kV | RURAL |
| `B3` | B (Baixa Tensão) | < 1 kV | COMERCIAL, INDUSTRIAL, PODER PUBLICO, SERVICO PUBLICO |
| `B4` | B (Baixa Tensão) | < 1 kV | ILUMINACAO PUBLICA |
| `A4` | A (Alta Tensão) | 2,3 kV a 25 kV | COMERCIAL, INDUSTRIAL, PODER PUBLICO |
| `A3a` | A (Alta Tensão) | 30 kV a 44 kV | COMERCIAL, INDUSTRIAL |
| `A3` | A (Alta Tensão) | 69 kV | COMERCIAL, INDUSTRIAL |
| `A2` | A (Alta Tensão) | 88 kV a 138 kV | COMERCIAL, INDUSTRIAL |
| `A1` | A (Alta Tensão) | >= 230 kV | COMERCIAL, INDUSTRIAL |
| `AS` | A (Alta Tensão) | Subterrâneo | INDUSTRIAL |

**Regras de qualidade — Tarifária:**
- `COD_MODALIDADE_TARIFARIA` não pode ser nulo
- A combinação classe × modalidade deve ser consistente conforme tabela acima
- Consumidores `RESIDENCIAL` só podem ter modalidade `B1`
- Consumidores `RURAL` só podem ter modalidade `B2`
- Consumidores `ILUMINACAO PUBLICA` só podem ter modalidade `B4`

---

### 3. Endereço

| Campo | Tipo SQL | Tipo Python | Obrigatório | Descrição |
|-------|----------|-------------|-------------|-----------|
| `NOM_LOGRADOURO` | `VARCHAR(200)` | `str` | Não | Tipo e nome do logradouro (ex: "Rua das Flores"). |
| `NUM_LOGRADOURO` | `VARCHAR(10)` | `str` | Não | Número do imóvel no logradouro. Pode conter letras (ex: "123A"). |
| `NOM_COMPLEMENTO` | `VARCHAR(100)` | `str` | Não | Complemento do endereço (ex: "Apto 301", "Bloco B"). |
| `NOM_BAIRRO` | `VARCHAR(100)` | `str` | Não | Nome do bairro. |
| `NOM_MUNICIPIO` | `VARCHAR(100)` | `str` | Sim | Nome do município. Deve corresponder a um município válido do IBGE. |
| `COD_UF` | `CHAR(2)` | `str` | Sim | Sigla do estado (UF) em maiúsculas (ex: "SP", "MG"). |
| `NUM_CEP` | `VARCHAR(9)` | `str` | Sim | CEP no formato `XXXXX-XXX`. |

**Regras de qualidade — Endereço:**
- `NOM_MUNICIPIO` e `COD_UF` são obrigatórios
- `NUM_CEP` deve estar no formato `XXXXX-XXX` (8 dígitos com hífen)
- `COD_UF` deve conter apenas letras maiúsculas e estar na lista de UFs brasileiras

---

### 4. Cadastro Técnico

| Campo | Tipo SQL | Tipo Python | Obrigatório | Descrição |
|-------|----------|-------------|-------------|-----------|
| `NUM_MEDIDOR` | `BIGINT` | `int` | Não | Número de série do medidor instalado na UC. Pode ser nulo para UCs em implantação. |
| `DAT_INICIO_VIGENCIA` | `DATE` | `date` | Sim | Data em que a UC iniciou o fornecimento de energia. |
| `DAT_FIM_VIGENCIA` | `DATE` | `date` | Não | Data de encerramento do contrato. Nulo indica vigência em aberto (UC ativa). |
| `FLG_ATIVO` | `BOOLEAN` | `bool` | Sim | Indica se a UC está com fornecimento ativo (`TRUE`) ou encerrado/suspenso (`FALSE`). |
| `DAT_ULTIMA_LEITURA` | `DATE` | `date` | Não | Data da última leitura do medidor registrada no sistema. |
| `VLR_CONSUMO_MEDIO_KWH` | `FLOAT` | `float` | Não | Consumo médio mensal calculado com base nas últimas leituras. Em kWh. |

**Regras de qualidade — Cadastro Técnico:**
- `FLG_ATIVO = TRUE` e `DAT_ULTIMA_LEITURA` nula por mais de 45 dias é suspeito
- `VLR_CONSUMO_MEDIO_KWH` deve estar entre 0 e 500.000 kWh (acima = outlier suspeito)
- `DAT_FIM_VIGENCIA` deve ser posterior a `DAT_INICIO_VIGENCIA` quando informada
- UCs ativas (`FLG_ATIVO = TRUE`) devem ter `NUM_MEDIDOR` informado

---

### 5. Geolocalização

| Campo | Tipo SQL | Tipo Python | Obrigatório | Descrição |
|-------|----------|-------------|-------------|-----------|
| `NUM_LATITUDE` | `FLOAT` | `float` | Não | Latitude em graus decimais (WGS84). Para o Brasil: entre -33,0 e +5,0. |
| `NUM_LONGITUDE` | `FLOAT` | `float` | Não | Longitude em graus decimais (WGS84). Para o Brasil: entre -73,0 e -34,0. |

**Regras de qualidade — Geolocalização:**
- Latitude para o Brasil: deve estar entre -33,0 e +5,0
- Longitude para o Brasil: deve estar entre -73,0 e -34,0
- Ambas devem ser nulas ou ambas informadas (não pode ter apenas uma)

---

## Exemplos de Registros

### Registro válido — Consumidor Residencial
```json
{
  "COD_CONSUMIDOR": 100042,
  "NOM_CONSUMIDOR": "Maria da Silva Santos",
  "CPF_CNPJ": "12345678909",
  "COD_MODALIDADE_TARIFARIA": "B1",
  "COD_CLASSE_CONSUMO": "RESIDENCIAL",
  "NOM_LOGRADOURO": "Rua das Acácias",
  "NUM_LOGRADOURO": "245",
  "NOM_BAIRRO": "Jardim das Flores",
  "NOM_MUNICIPIO": "São Paulo",
  "COD_UF": "SP",
  "NUM_CEP": "01310-100",
  "NUM_MEDIDOR": 40019273,
  "DAT_INICIO_VIGENCIA": "2018-03-15",
  "DAT_FIM_VIGENCIA": null,
  "FLG_ATIVO": true,
  "DAT_ULTIMA_LEITURA": "2025-02-10",
  "VLR_CONSUMO_MEDIO_KWH": 245.3,
  "NUM_LATITUDE": -23.548,
  "NUM_LONGITUDE": -46.636
}
```

### Problemas de qualidade comuns

| Problema | Exemplo | Impacto |
|----------|---------|---------|
| CPF nulo | `CPF_CNPJ = NULL` | Impossibilidade de emitir NF-e |
| Modalidade inconsistente | `RESIDENCIAL + A4` | Erro de tarifação |
| CEP malformado | `"0131010"` (7 dígitos) | Impossibilidade de correspondência |
| Consumo outlier | `VLR_CONSUMO = 9999999` | Erro de medição ou dado corrompido |
| Coordenadas fora do Brasil | `LAT = 40.0` | Dado de migração incorreto |

---

## Consultas de Diagnóstico Recomendadas

```sql
-- 1. Completude geral
SELECT
    COUNT(*) total,
    COUNT(cpf_cnpj) com_cpf,
    COUNT(num_medidor) com_medidor,
    COUNT(dat_ultima_leitura) com_leitura,
    COUNT(num_latitude) com_coordenadas
FROM CADASTRO.CONSUMIDORES_UC
WHERE flg_ativo = TRUE;

-- 2. Inconsistências tarifárias
SELECT cod_consumidor, cod_classe_consumo, cod_modalidade_tarifaria
FROM CADASTRO.CONSUMIDORES_UC
WHERE (cod_classe_consumo = 'RESIDENCIAL' AND cod_modalidade_tarifaria <> 'B1')
   OR (cod_classe_consumo = 'RURAL' AND cod_modalidade_tarifaria <> 'B2')
   OR (cod_classe_consumo = 'ILUMINACAO PUBLICA' AND cod_modalidade_tarifaria <> 'B4');

-- 3. Outliers de consumo
SELECT cod_consumidor, nom_consumidor, vlr_consumo_medio_kwh
FROM CADASTRO.CONSUMIDORES_UC
WHERE vlr_consumo_medio_kwh > 500000 OR vlr_consumo_medio_kwh < 0;
```
