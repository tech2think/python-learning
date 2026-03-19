# Glossário do Setor Elétrico

Termos técnicos e regulatórios do setor de distribuição de energia elétrica brasileira, com foco em análise de dados e qualidade de cadastro.

---

## A

**ABNT NBR 14519**
Norma técnica brasileira que define os requisitos para o sistema de medição de energia elétrica. Relevante para validação de dados de medidores.

**ANEEL (Agência Nacional de Energia Elétrica)**
Agência reguladora do setor elétrico brasileiro, vinculada ao Ministério de Minas e Energia. Estabelece as regras de tarifação, indicadores de qualidade (DEC, FEC) e obrigações das distribuidoras via PRODIST e PRORET.

**ANSI**
Sigla para American National Standards Institute. No contexto elétrico, refere-se a tipos de medidores (ex: medidor ANSI de 4 terminais).

---

## B

**Baixa Tensão (BT)**
Tensão de fornecimento inferior a 1 kV (1.000 V). Consumidores do grupo B são atendidos em baixa tensão. Inclui residências, pequenos comércios e estabelecimentos rurais.

**Bandeira Tarifária**
Sistema de sinalizador de cores (verde, amarela, vermelha) que informa ao consumidor sobre as condições de geração de energia. Reflete o custo de produção e impacta diretamente o valor da fatura.

**B1, B2, B3, B4**
Modalidades tarifárias do grupo B (baixa tensão):
- **B1:** Residencial
- **B2:** Rural
- **B3:** Demais classes (Comercial, Industrial BT, Serviços Públicos)
- **B4:** Iluminação Pública

---

## C

**CEP (Código de Endereçamento Postal)**
Código de 8 dígitos (formato XXXXX-XXX) usado pelos Correios para identificar logradouros. Fundamental para geolocalização de UCs.

**Classe de Consumo**
Categorização do consumidor conforme a finalidade do uso da energia: RESIDENCIAL, COMERCIAL, INDUSTRIAL, RURAL, PODER PÚBLICO, ILUMINAÇÃO PÚBLICA, SERVIÇO PÚBLICO.

**Conjunto de Distribuição**
Agrupamento de alimentadores de distribuição utilizado para cálculo dos indicadores DEC e FEC. Definido pelo PRODIST.

**CPF (Cadastro de Pessoas Físicas)**
Documento de identificação de pessoa física emitido pela Receita Federal. Composto de 11 dígitos com dois dígitos verificadores.

**CNPJ (Cadastro Nacional de Pessoa Jurídica)**
Documento de identificação de pessoa jurídica emitido pela Receita Federal. Composto de 14 dígitos com dois dígitos verificadores.

---

## D

**DEC (Duração Equivalente de Interrupção por Consumidor)**
Indicador de continuidade que representa a duração média, em horas, que cada consumidor ficou sem energia em determinado período. Calculado como: `DEC = Σ(Di × Ci) / Ct`, onde Di = duração da interrupção, Ci = consumidores afetados, Ct = total de consumidores. Monitorado pela ANEEL com limites anuais por conjunto.

**Demanda**
Potência elétrica (em kW ou kVA) demandada por um consumidor em determinado período. Consumidores do grupo A contratam demanda e são cobrados por ela, independentemente do consumo de energia.

**Distribuidora**
Empresa concessionária ou permissionária responsável pela distribuição de energia elétrica em determinada área geográfica. Obrigada a atender todos os consumidores dentro de sua área de concessão.

---

## E

**Energia Ativa**
Energia efetivamente consumida e convertida em trabalho (iluminação, calor, movimento). Medida em kWh (quilowatt-hora). É a base do faturamento para consumidores do grupo B.

**Energia Reativa**
Energia que circula entre a rede e os equipamentos sem realizar trabalho útil. Medida em kVAr. Consumidores com baixo fator de potência podem ser cobrados por excesso de reativo.

---

## F

**Fator de Potência (FP)**
Relação entre a energia ativa e a energia aparente. Valor ideal: 0,92 ou superior. Consumidores com FP < 0,92 (indutivo) podem receber penalidades na fatura.

**Faturamento**
Processo de cálculo e emissão da conta de energia elétrica. Baseado nos dados de medição e no cadastro do consumidor.

**FEC (Frequência Equivalente de Interrupção por Consumidor)**
Indicador de continuidade que representa o número médio de interrupções que cada consumidor sofreu em determinado período. Calculado como: `FEC = Σ(Ci) / Ct`. Complementar ao DEC — juntos formam os principais indicadores de qualidade de fornecimento da ANEEL.

**FERC**
Sigla para Federal Energy Regulatory Commission (EUA). Referência em regulação setorial — comparado com a ANEEL no Brasil.

---

## G

**GD (Geração Distribuída)**
Pequenas centrais geradoras de energia conectadas à rede de distribuição (ex: painéis solares). Consumidores com GD podem injetar energia na rede e receber créditos. Regulamentado pela ANEEL via Resolução Normativa 482/2012 e Lei 14.300/2022.

**Grupo A**
Consumidores atendidos em média ou alta tensão (a partir de 2,3 kV). Modalidades: A1, A2, A3, A3a, A4, AS. Faturamento inclui demanda contratada.

**Grupo B**
Consumidores atendidos em baixa tensão (< 1 kV). Modalidades: B1, B2, B3, B4. Faturamento baseado em consumo (kWh).

---

## I

**ICMS (Imposto sobre Circulação de Mercadorias e Serviços)**
Imposto estadual incidente sobre a energia elétrica. Alíquota varia por estado e por faixa de consumo.

**Inadimplência**
Situação do consumidor que não pagou a conta de energia no prazo. Após determinado período, a distribuidora pode suspender o fornecimento (corte), respeitando regras da ANEEL e do CDC.

---

## K

**kVA (Quilovolt-Ampere)**
Unidade de potência aparente. Combina energia ativa (kW) e reativa (kVAr).

**kW (Quilowatt)**
Unidade de potência ativa. 1 kW = 1.000 W.

**kWh (Quilowatt-hora)**
Unidade de energia. 1 kWh = energia consumida por um aparelho de 1 kW operando durante 1 hora. Unidade base do faturamento residencial.

---

## L

**Leitura de Medidor**
Processo de coleta do valor registrado no medidor de energia para fins de faturamento. Pode ser feita por leiturista (campo) ou remotamente (telemetria).

**Limite de DEC/FEC**
Valor máximo de DEC e FEC que a distribuidora pode atingir por conjunto de distribuição em determinado período. Definido pela ANEEL no PRODIST. Ultrapassar o limite implica compensações financeiras aos consumidores.

---

## M

**Medidor**
Equipamento que mede o consumo de energia elétrica. Pode ser eletrônico, eletromecânico ou inteligente (smart meter). Identificado pelo `NUM_MEDIDOR` no cadastro.

**Microgeração Distribuída**
Geração de energia elétrica com potência instalada de até 75 kW, por fonte incentivada ou cogeração qualificada. Regulada pela ANEEL.

**Modalidade Tarifária**
Conjunto de tarifas e condições aplicáveis ao fornecimento de energia. Determinado pela tensão de fornecimento e classe do consumidor. Ver B1, B2, B3, B4, A4, etc.

---

## P

**PRODIST (Procedimentos de Distribuição)**
Documento normativo da ANEEL que estabelece as condições técnicas e comerciais para a distribuição de energia elétrica. Define indicadores DEC, FEC, regras de qualidade de tensão, etc.

**PRORET (Procedimentos de Regulação Tarifária)**
Documento normativo da ANEEL que rege os processos de revisão e reajuste tarifário das distribuidoras.

**PIS/COFINS**
Tributos federais incidentes sobre a energia elétrica. Junto com o ICMS, compõem a maior parte da carga tributária da fatura de energia.

---

## R

**Revisão Tarifária Periódica (RTP)**
Processo realizado pela ANEEL a cada 4 ou 5 anos para redefinir a tarifa base da distribuidora, considerando custos prudentes e qualidade do serviço.

---

## S

**SAMP (Sistema de Arrecadação, Medição e Perdas)**
Sistema da distribuidora responsável por integrar dados de medição, faturamento e perdas técnicas e não técnicas.

**Subclasse**
Subdivisão da classe de consumo. Ex: dentro da classe RESIDENCIAL, há a subclasse "Residencial Normal" e "Residencial Baixa Renda".

**Subestação**
Instalação elétrica que transforma a tensão de transmissão (alta tensão) para os níveis de distribuição (média tensão). Ponto de entrega para grandes consumidores industriais.

---

## T

**TE (Tarifa de Energia)**
Componente tarifária que remunera a geração de energia elétrica. Compõe, junto com a TUSD, o valor total pago pelo consumidor.

**TUSD (Tarifa de Uso do Sistema de Distribuição)**
Componente tarifária que remunera o uso da rede de distribuição. Paga por todos os consumidores conectados à rede.

---

## U

**UC (Unidade Consumidora)**
Conjunto de instalações e equipamentos elétricos de um consumidor, ligado ao sistema de distribuição por um único ramal de entrada. Cada UC tem um código único no sistema da distribuidora. Uma pessoa pode ter múltiplas UCs.

**UF (Unidade Federativa)**
Sigla de dois caracteres do estado brasileiro (ex: SP, RJ, MG). Usada no campo `COD_UF` do cadastro.

---

## V

**VRE (Verificação de Regularidade de Entrada)**
Processo de inspeção das instalações do consumidor para verificar conformidade com as normas técnicas.

---

## W

**Watt (W)**
Unidade básica de potência elétrica. 1 W = 1 J/s. No contexto de distribuição, usam-se kW (quilowatt), MW (megawatt) e GW (gigawatt).

---

*Glossário elaborado com base nas normas ANEEL, PRODIST e PRORET. Para termos regulatórios oficiais, consulte sempre a fonte primária em aneel.gov.br.*
