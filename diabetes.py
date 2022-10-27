from datetime import datetime, timedelta
from textwrap import dedent

#importando bibliotecas do airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import dag, task
from airflow.models.baseoperator import chain

#Importando as bibliotecas necessárias
import sys
import os
import mlflow
import mlflow.sklearn
from urllib.parse import urlparse

#Manipulação de dados
import pandas as pd

# Pré-Processamento
from sklearn.preprocessing import StandardScaler

# Criação do modelo
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

#Métricas
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

#Ignorar avisos de atualização, etc
import warnings
warnings.filterwarnings("ignore")

#Gráficos
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

import logging
#Importação das bibliotecas para processamento do dataframe


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    # Em caso de erros, tente rodar novamente apenas 1 vez.
    'retries': 1,
    # Tente novamente após 30 segundos depois do erro.
    'retry_delay': timedelta(seconds=30)
}

@dag(schedule_interval=None, start_date=datetime(2021, 1, 1), catchup=False, tags=['example'])
# (star_date):start_date seja um valor anterior ao dia presente, já que o mesmo executa o DAG do dia anterior no dia atual
# Execute uma vez só (schedule_interval)
# Se mudar (schedule_interval) para “@daily” fará com que o DAG seja executada diariamente!
def Diabetes2():
    """
    Flow para apredizagem de maquina sobre o dataset housing
    """
    @task()
    def start():
       logging.basicConfig(level=logging.WARN)
       logger = logging.getLogger(__name__)

       mlflow.set_tracking_uri('http://localhost:5000')
       #mlflow.set_tracking_uri('mysql://root:root@localhost:3306/mlflow')
       mlflow.set_experiment(experiment_name='Diabetes_Classification')

       tags = {
                "Projeto": "Live MLflow",
                "team": "Data Hackers",
                "dataset": "Diabetes"
            }          

    @task()
    def treino():

        tags = {
                "Projeto": "Live MLflow",
                "team": "Data Hackers",
                "dataset": "Diabetes"
            } 
        def metricas(y_test, y_predict):
            acuracia = accuracy_score(y_test, y_predict)
            precision = precision_score(y_test, y_predict)
            recall = recall_score(y_test, y_predict)
            f1 = f1_score(y_test, y_predict)
            return acuracia, precision, recall, f1

        def matriz_confusao(y_test, y_predict):
            matriz_conf = confusion_matrix(y_test.values.ravel(), y_predict)
            fig = plt.figure()
            ax = plt.subplot()
            sns.heatmap(matriz_conf, annot=True, cmap='Blues', ax=ax);

            ax.set_xlabel('Valor Predito');
            ax.set_ylabel('Valor Real'); 
            ax.set_title('Matriz de Confusão'); 
            ax.xaxis.set_ticklabels(['0', '1']);
            ax.yaxis.set_ticklabels(['0', '1']);
            plt.close()
            return fig
        def modelo():
            #Criação do modelo
            max_depth = int("2")
            balanced = int("3")
            balanced = "balanced" if balanced == 1 else None
            clf = RandomForestClassifier(random_state=42, class_weight=balanced, max_depth=max_depth)
            clf.fit(x_train, y_train)
            return clf

        def previsao(x_test, modelo):
            y_pred = modelo.predict(x_test)
            return y_pred
   
        warnings.filterwarnings("ignore")

        df = pd.read_csv("/home/mancave/Downloads/dag/diabetes.csv")

        train, test = train_test_split(df, random_state=2)
        x_train = train.drop(columns=["Outcome"])
        x_test = test.drop(columns=["Outcome"])
        y_train = train[["Outcome"]]
        y_test = test[["Outcome"]]

        with mlflow.start_run(run_name='RandomForestClassifier'):
            warnings.filterwarnings("ignore")
            #Registro das tags
            mlflow.set_tags(tags)

            #Criação do modelo
            max_depth = int("2")
            balanced = int("3")
            balanced = "balanced" if balanced == 1 else None
            clf = RandomForestClassifier(random_state=2, class_weight=balanced, max_depth=max_depth)
            clf.fit(x_train, y_train)
            
            #Predição dos valores de testes
            y_pred = clf.predict(x_test)
            
            #Métricas
            acuracia, precision, recall, f1 = metricas(y_test, y_pred)
            print("Acurácia: {}\nPrecision: {}\nRecall: {}\nF1-Score: {}".
                format(acuracia, precision, recall, f1))

            #Matriz de confusão
            matriz_conf = matriz_confusao(y_test, y_pred)
            temp_name = "confusion-matrix.png"
            matriz_conf.savefig(temp_name)
            mlflow.log_artifact(temp_name, "confusion-matrix-plots")
            try:
                os.remove(temp_name)
            except FileNotFoundError as e:
                print(f"{temp_name} file is not found")

            #Registro dos parâmetros e das métricas
            mlflow.log_param("balanced", balanced)
            mlflow.log_param("max_depth", max_depth)
            mlflow.log_metric("Acuracia", acuracia)
            mlflow.log_metric("Precision", precision)
            mlflow.log_metric("Recall", recall)
            mlflow.log_metric("F1-Score", f1)

            #Registro do modelo
            mlflow.sklearn.log_model(clf, "model")
            
    @task()
    def search_runs():
        
         run_id = mlflow.search_runs(filter_string='tags.mlflow.runName = "RandomForestClassifier"').iloc[0].run_id   

    @task()
    def register_model():
        run_id = mlflow.search_runs(filter_string='tags.mlflow.runName = "RandomForestClassifier"').iloc[0].run_id  
        from mlflow.tracking import MlflowClient
        from mlflow.store.artifact.runs_artifact_repo import RunsArtifactRepository
        client = MlflowClient()
        model_name = "RandomForestClassifier" # "tfkerascifar10" # Precisou alterar o nome do modelo, pois pode ser que esse nome já foi utilizado em algum teste com usuário que tem permissão maior e não conseguimos sobrescrever

        runs_uri = "runs:/{}/models".format(run_id)
        result = mlflow.register_model(runs_uri, model_name)
        result     

    @task()
    def best_run():
        mlflow.search_runs(filter_string='tags.mlflow.runName = "RandomForestClassifier"',search_all_experiments= True,order_by=['metrics.acc DESC'])  
        best_run = mlflow.search_runs(filter_string='tags.mlflow.runName = "RandomForestClassifier"',search_all_experiments= True,order_by=['metrics.acc DESC']).iloc[0]      
    
         
    
    #t1 >> start() >> criar_diretorio() >> [[drop_train() >> search_runs()], best_run()]
 
    chain(start(),treino(),search_runs(),register_model(),best_run())
dag = Diabetes2()