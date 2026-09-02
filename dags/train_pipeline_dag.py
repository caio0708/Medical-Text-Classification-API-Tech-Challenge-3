from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Configurações padrão da DAG
default_args = {
    'owner': 'equipe-dados',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

def ler_dados_csv():
    """Lê o dataset de triagem médica diretamente do arquivo CSV e salva temporariamente para o treinamento[cite: 1]."""
    print("Iniciando a leitura do dataset de treino...")
    caminho_csv = 'data/medical_tc_train.csv'
    
    # Lê o dataset real em vez de usar mocks
    df = pd.read_csv(caminho_csv)
    
    caminho_tmp = '/tmp/dados_triagem.csv'
    df.to_csv(caminho_tmp, index=False)
    print(f"Dados consolidados de {caminho_csv} e salvos em {caminho_tmp}")

def treinar_e_salvar_modelo():
    """Treina o modelo de NLP otimizado e exporta o artefato."""
    from sklearn.pipeline import Pipeline
    
    caminho_tmp = '/tmp/dados_triagem.csv'
    df = pd.read_csv(caminho_tmp)
    
    print("Treinando Pipeline (TF-IDF + Random Forest Balanceado)...")
    
    # Cria o pipeline idêntico ao exigido pelo conversor ONNX
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))),
        ('clf', RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42, n_jobs=-1))
    ])
    
    # Treinamento com as colunas corretas
    pipeline.fit(df['medical_abstract'].astype(str), df['condition_label'])
    
    # Salva na pasta mapeada para o Windows (/opt/airflow/models sincroniza com ./models)
    os.makedirs('/opt/airflow/models', exist_ok=True)
    caminho_modelo = '/opt/airflow/models/modelo_original.pkl'
    joblib.dump(pipeline, caminho_modelo)
    print(f"Modelo treinado e salvo com sucesso em {caminho_modelo}")

# Definição da DAG
with DAG(
    'pipeline_treinamento_triagem',
    default_args=default_args,
    description='Pipeline automatizado para treino do modelo de classificação médica',
    schedule_interval='@weekly',
    catchup=False,
) as dag:

    # Task 1: Ler CSV de dados
    task_leitura = PythonOperator(
        task_id='ler_csv_dados',
        python_callable=ler_dados_csv,
    )

    # Task 2: Treinar e salvar o modelo
    task_treinamento = PythonOperator(
        task_id='treinar_salvar_modelo',
        python_callable=treinar_e_salvar_modelo,
    )

    # Ordem de execução
    task_leitura >> task_treinamento