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
    """Lê o dataset de triagem médica e salva temporariamente para o treinamento."""
    print("Iniciando a leitura do dataset de treino...")
    # Em produção, o caminho apontaria para o medical_tc_train.csv
    # Mock de dados para garantir que a DAG rode sem dependências externas no teste inicial
    dados_mock = pd.DataFrame({
        'texto_laudo': [
            'Paciente apresenta quadro de dor torácica aguda.',
            'Exames de sangue de rotina dentro da normalidade.',
            'Fratura exposta no membro superior direito, sangramento ativo.'
        ],
        'classe_urgencia': [2, 5, 1] 
    })
    
    caminho_tmp = '/tmp/dados_triagem.csv'
    dados_mock.to_csv(caminho_tmp, index=False)
    print(f"Dados consolidados e salvos em {caminho_tmp}")

def treinar_e_salvar_modelo():
    """Treina o modelo de NLP e exporta o artefato."""
    caminho_tmp = '/tmp/dados_triagem.csv'
    df = pd.read_csv(caminho_tmp)
    
    print("Vetorizando os textos (TF-IDF)...")
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(df['texto_laudo'])
    y = df['classe_urgencia']
    
    print("Treinando classificador Random Forest...")
    modelo = RandomForestClassifier(n_estimators=50, random_state=42)
    modelo.fit(X, y)
    
    os.makedirs('/tmp/modelos', exist_ok=True)
    caminho_modelo = '/tmp/modelos/modelo_triagem_v1.pkl'
    joblib.dump({'vetorizador': vectorizer, 'modelo': modelo}, caminho_modelo)
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