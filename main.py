from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Inicialização da API
app = FastAPI(
    title="Medical Text Classification API",
    description="API de triagem automática de laudos médicos para urgência/classificação.",
    version="2.0.0"
)

# Definição das Métricas do Prometheus
REQUEST_COUNT = Counter(
    'api_requests_total',
    'Total de requisições processadas pela API',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'api_request_latency_seconds',
    'Latência das requisições em segundos',
    ['method', 'endpoint']
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

# Middleware para interceptar e medir todas as chamadas
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    method = request.method
    endpoint = request.url.path
    
    # Ignora a rota de métricas para não poluir os dados
    if endpoint == "/metrics":
        return await call_next(request)
    
    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception as e:
        status_code = 500
        raise e
    finally:
        latency = time.time() - start_time
        # Registra a contagem e o tempo de resposta
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(latency)
        
    return response

# Rota para expor os dados ao Prometheus
@app.get("/metrics", include_in_schema=False)
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Schema de entrada de dados
class LaudoMedico(BaseModel):
    texto: str

# Schema de saída de dados
class ClassificacaoResponse(BaseModel):
    classificacao: int
    tempo_processamento_ms: float

def carregar_modelo():
    return None

modelo = carregar_modelo()

@app.post("/predict", response_model=ClassificacaoResponse)
async def classificar_laudo(laudo: LaudoMedico):
    start_time = time.time()
    
    if not laudo.texto.strip():
        raise HTTPException(status_code=400, detail="O texto do laudo não pode ser vazio.")
    
    predicao_simulada = 1 
    
    process_time = (time.time() - start_time) * 1000
    
    return ClassificacaoResponse(
        classificacao=predicao_simulada,
        tempo_processamento_ms=round(process_time, 2)
    )

@app.get("/health")
async def health_check():
    return {"status": "ok"}