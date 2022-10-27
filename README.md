# Integração do Mlflow com Airflow em máquina local.

Utilizando o conjunto de dados scikit-learn "diabetes" e prevê a métrica de progressão (uma medida quantitativa da progressão da doença após um ano) com base no IMC, pressão arterial e outras medidas!


# Airflow

O Airflow é uma plataforma para criar, agendar e monitorar de forma programática fluxos de trabalho. Use o Airflow para criar fluxos de trabalho como gráficos acíclicos direcionados (DAGs) de tarefas.

# Recomendo seguir alguns tutoriais para entender melhor o Airflow e suas funcionalidades:

* [Aplicar Ciência de Dados — Tuan Vu](https://www.applydatascience.com/year-archive/)
* [Impressionante fluxo de ar Apache](https://github.com/jghoman/awesome-apache-airflow)
* [Guias do Apache Airflow](https://www.astronomer.io/guides/)
* [Apache Airflow: The Hands-On Guide](https://www.udemy.com/course/the-ultimate-hands-on-course-to-master-apache-airflow/)(Este é pago na Udemy, é altamente recomendável comprar e concluir este curso)
* [Documentação oficial do fluxo de ar](https://airflow.apache.org/docs/stable/)

O Airflow fornece aos operadores muitas tarefas comuns, incluindo:

* **BashOperator** — executa um comando bash
* **PythonOperator** — chama uma função Python arbitrária
* **EmailOperator** — envia um e-mail
* **SimpleHttpOperator** — envia uma solicitação HTTP
* **MySqlOperator, SqliteOperator, PostgresOperator, MsSqlOperator, OracleOperator, JdbcOperator, etc.** — executa um comando SQL
* **Sensor** — um Operador que espera (polls) por um determinado tempo, arquivo, linha do banco de dados, chave S3, etc…


# MLFlow

O mlFlow é uma estrutura que oferece suporte ao ciclo de vida de aprendizado de máquina. Isso significa que ele possui componentes para monitorar seu modelo durante o treinamento e execução, capacidade de armazenar modelos, carregar o modelo no código de produção e criar um pipeline.
O que exatamente ele pode rastrear:

* **Parâmetros** — Parâmetros de entrada de valor-chave de sua escolha. Tanto as chaves quanto os valores são strings.
exemplo — mlflow.log_parameter('alpha',alpha_val_of_regression)

* **Métricas** — Métricas de valor-chave em que o valor é numérico. Cada métrica pode ser atualizada ao longo da execução (por exemplo, para rastrear como a função de perda do seu modelo está convergindo), e o MLflow registrará e permitirá que você visualize o histórico completo da métrica.
exemplo — mlflow.log_metric('rmse', rmse_value_of_model_train)

* **Artefatos** — Arquivos de saída em qualquer formato. Por exemplo, você pode gravar imagens (por exemplo, PNGs), modelos (por exemplo, um modelo scikit-learn em conserva) ou até mesmo arquivos de dados (por exemplo, um arquivo parquet) como artefatos.
exemplo — mlflow.sklearn.log_model('Ridge', model_ridge)

# Tutoriais do mlflow você encontra:
* [Documentação oficial](https://mlflow.org/docs/0.5.0/index.html)
* [Medium](https://towardsdatascience.com/manage-your-machine-learning-lifecycle-with-mlflow-part-1-a7252c859f72)
* [Databricks](https://docs.databricks.com/_static/notebooks/mlflow/mlflow-quick-start-training.html)

# Para instalar:
> **$ pip install mlflow**

# para visualização: 

De um novo terminal digite: 
> **$ mlflow ui**

Codigo em eterna* construção....
