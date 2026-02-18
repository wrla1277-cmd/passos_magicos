# Métricas e Composição do INDE: Associação Passos Mágicos

Com base no documento "PEDE - Pontos Importantes", foram extraídas as fórmulas e pesos oficiais que compõem o Índice de Desenvolvimento Educacional (INDE):

## 1. Composição do INDE
O INDE é calculado de forma diferente dependendo da fase do aluno:

### Fases 0 a 7
**Fórmula:** `INDE = IAN*0.1 + IDA*0.2 + IEG*0.2 + IAA*0.1 + IPS*0.1 + IPP*0.1 + IPV*0.2`

### Fase 8
**Fórmula:** `INDE = IAN*0.1 + IDA*0.4 + IEG*0.2 + IAA*0.1 + IPS*0.2`

## 2. Detalhamento dos Indicadores
- **IAN (Adequação de Nível):** Baseado na defasagem (D = Fase Efetiva - Fase Ideal).
  - `D >= 0`: 10 pontos (Em fase)
  - `0 > D >= -2`: 5 pontos (Moderada)
  - `D < -2`: 2,5 pontos (Severa)
- **IDA (Desempenho Acadêmico):** Média aritmética das notas de Matemática, Português e Inglês.
- **IEG (Engajamento):** Média de pontuação de tarefas (casa, acadêmicas, voluntariado).
- **IAA (Autoavaliação):** Média das respostas do questionário de autoavaliação (0 a 10).
- **IPS (Psicossocial):** Média das avaliações feitas por psicólogos.
- **IPP (Psicopedagógico):** Média das avaliações sobre aspectos pedagógicos.
- **IPV (Ponto de Virada):** Análise longitudinal de progresso acadêmico, engajamento e emocional.

## 3. Classificação por Pedras (Conceito INDE)
- **Quartzo:** INDE entre 3,0 e 6,1
- **Ágata:** INDE entre 6,1 e 7,2
- **Ametista:** INDE entre 7,2 e 8,2
- **Topázio:** INDE entre 8,2 e 9,4

## 4. Implicações para o Projeto
- O modelo de ML deve priorizar o IPV como um dos principais preditores de sucesso, dado seu peso de 20% nas fases iniciais.
- A aplicação Streamlit deve permitir a simulação do INDE com base nesses pesos oficiais.
- O Storytelling deve destacar a transição entre as pedras como marcos de evolução do aluno.
