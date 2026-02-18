# Projeto Datathon - Associação Passos Mágicos

Este projeto contém uma aplicação Streamlit para análise de dados educacionais e predição de risco de defasagem dos alunos da Associação Passos Mágicos (2022-2024).

## 📁 Conteúdo do Pacote

- `app_v2.py`: Código principal da aplicação Streamlit.
- `prepare_data.py`: Script para consolidar e limpar os dados das 3 abas do Excel.
- `requirements.txt`: Lista de dependências necessárias.
- `data_consolidated.csv`: Base de dados limpa e consolidada.
- `BASEDEDADOSPEDE2024-DATATHON.xlsx`: Arquivo Excel original com as 3 abas.

## 🚀 Como Executar Localmente

### 1. Pré-requisitos
Certifique-se de ter o Python instalado (recomendado 3.9 ou superior).

### 2. Instalação das Dependências
Abra o terminal na pasta do projeto e execute:
```bash
pip install -r requirements.txt
```

### 3. Execução da Aplicação
Para iniciar a aplicação Streamlit, execute:
```bash
streamlit run app_v2.py
```

## 📊 Estrutura da Aplicação
A aplicação está dividida em 4 seções principais:
1. **Home**: Visão geral e KPIs de impacto.
2. **Análise Exploratória**: Detalhes sobre IAN, IDA, Engajamento e evolução temporal.
3. **Predição de Risco**: Simulador com modelo de Machine Learning.
4. **Insights Estratégicos**: Análise do Ponto de Virada e recomendações.

---
Desenvolvido para o Datathon Fase 5 - Case Passos Mágicos.
