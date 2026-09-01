from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

# Inicialização da API
app = FastAPI(
    title="Medical Text Classification API",
    description="API de triagem automática de laudos médicos para urgência/classificação.",
    version="1.0.0"
)

# Schema de entrada de dados
class LaudoMedico(BaseModel):
    texto: str

# Schema de saída de dados
class ClassificacaoResponse(BaseModel):
    classificacao: int
    tempo_processamento_ms: float

# Simulação de carregamento do modelo (Substitua por joblib.load('modelo.pkl'))
def carregar_modelo():
    # Exemplo: pipeline = joblib.load("modelo_tfidf_rf.pkl")
    return None

modelo = carregar_modelo()

@app.post("/predict", response_model=ClassificacaoResponse)
async def classificar_laudo(laudo: LaudoMedico):
    start_time = time.time()
    
    if not laudo.texto.strip():
        raise HTTPException(status_code=400, detail="O texto do laudo não pode ser vazio.")
    
    # TODO: Substituir pela inferência real: prediction = modelo.predict([laudo.texto])[0]
    # Retornando classe simulada (1 a 5, baseada no dataset sugerido)
    predicao_simulada = 1 
    
    process_time = (time.time() - start_time) * 1000
    
    return ClassificacaoResponse(
        classificacao=predicao_simulada,
        tempo_processamento_ms=round(process_time, 2)
    )

@app.get("/health")
async def health_check():
    return {"status": "ok"}