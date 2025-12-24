Pipeline automatizada de análise de gastos financeiros, que coleta faturas em PDF, extrai transações, classifica gastos com Machine Learning supervisionado, solicita validação humana quando necessário, armazena dados históricos em banco de dados e gera um dataset pronto para análise no Power BI.


## PASSOS DO PROJETO
- **Linguagem:** Python
- **Ingestão:** Faturas bancárias baixadas diretamente do gmail
- **Extração:** PDFPLUMBER para extrair os dados do PDF, sendo ajustavél para diferentes layouts de diferentes bancos, linhas quebradas, e formatações irregulares
- **Transformação e Limpeza:** pandas e numpy para padronizar os dados
- **Banco de Dados:** PostgreSQL para armazenar as transições
- **Classificação supervisionada:** scikitlearn e joblib para treinar modelo de predição para automatizar a classificação das categorias 
- **Orquestração:** Apache Airflow
- **Análise e Visualização:** PowerBI

## HOW TO RUN
```bash
git clone https://github.com/danielasteim/financas-pessoais-pipeline.git
cd pipeline-personal-finances
python -m venv venv
venv\Scripts\activate
python main.py ```

## DASHBOARDS VISUALIZATIONS