import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import StringTensorType
import joblib
import os

# 1. Carregamento dos dados reais (medical_tc_train.csv)
print("Carregando dataset...")
df = pd.read_csv('data/medical_tc_train.csv')
X = df['medical_abstract'].values
y = df['condition_label'].values

# 2. Criação e Treinamento do Pipeline OTIMIZADO
print("Treinando modelo (TF-IDF Otimizado + Random Forest Balanceado)...")
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))),
    ('clf', RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42, n_jobs=-1))
])
pipeline.fit(X, y)

# Garante que a pasta de destino existe
os.makedirs('models', exist_ok=True)

# Salva o modelo original (Scikit-Learn) para comparação de latência
joblib.dump(pipeline, 'models/modelo_original.pkl')

# 3. Conversão para ONNX
print("Convertendo para ONNX...")
initial_type = [('texto_entrada', StringTensorType([None, 1]))]
onnx_model = convert_sklearn(pipeline, initial_types=initial_type, target_opset=12)

# Salva o modelo otimizado
with open("models/modelo_otimizado.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

print("Modelos salvos com sucesso!")