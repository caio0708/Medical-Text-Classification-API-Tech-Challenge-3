from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import onnxruntime as rt
import numpy as np

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

# Schemas de entrada e saída de dados
class LaudoMedico(BaseModel):
    texto: str

class ClassificacaoResponse(BaseModel):
    classificacao: int
    tempo_processamento_ms: float

# Inicializa a sessão do ONNX Runtime globalmente
try:
    sess = rt.InferenceSession("modelo_otimizado.onnx", providers=['CPUExecutionProvider'])
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
except Exception as e:
    print(f"Erro ao carregar o modelo ONNX: {e}")

# Middleware para interceptar e medir todas as chamadas
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    method = request.method
    endpoint = request.url.path
    
    # Ignora a rota de métricas para não poluir os dados do Grafana
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
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(latency)
        
    return response

# Rota para expor os dados ao Prometheus
@app.get("/metrics", include_in_schema=False)
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Rota principal de predição
@app.post("/predict", response_model=ClassificacaoResponse)
async def classificar_laudo(laudo: LaudoMedico):
    start_time = time.time()
    
    if not laudo.texto.strip():
        raise HTTPException(status_code=400, detail="O texto do laudo não pode ser vazio.")
    
    try:

            x_input = np.array([laudo.texto], dtype=object).reshape(-1, 1)
            
            pred_onx = sess.run([label_name], {input_name: x_input})[0]
            predicao_real = int(pred_onx[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno de inferência: {e}")
    
    process_time = (time.time() - start_time) * 1000
    
    return ClassificacaoResponse(
        classificacao=predicao_real,
        tempo_processamento_ms=round(process_time, 2)
    )

@app.get("/health")
async def health_check():
    return {"status": "ok"}