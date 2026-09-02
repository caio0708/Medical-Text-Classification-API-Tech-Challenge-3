"""Compara a latência de inferência do modelo original (scikit-learn/.pkl)
com o modelo otimizado (ONNX Runtime), em processo, para uma comparação
justa (sem overhead de rede/HTTP).

Uso:
    python comparar_latencia.py
"""
import statistics
import time
import warnings

import joblib
import numpy as np
import onnxruntime as rt
from sklearn.exceptions import InconsistentVersionWarning

# Ignorar avisos de versão do scikit-learn na desserialização
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

MODELO_ORIGINAL_PATH = "models/modelo_original.pkl"
MODELO_ONNX_PATH = "models/modelo_otimizado.onnx"
NUM_EXECUCOES = 200
WARMUP = 10

TEXTO_TESTE = (
    "Paciente relata dor torácica aguda e falta de ar. "
    "Histórico de hipertensão."
)


def medir_latencias(func_inferencia, num_execucoes: int, warmup: int) -> list:
    """Executa a função de inferência N vezes e retorna a lista de latências em ms."""
    for _ in range(warmup):
        func_inferencia()

    latencias_ms = []
    for _ in range(num_execucoes):
        inicio = time.perf_counter()
        func_inferencia()
        fim = time.perf_counter()
        latencias_ms.append((fim - inicio) * 1000)
    return latencias_ms


def imprimir_resultados(nome: str, latencias_ms: list) -> None:
    p95 = statistics.quantiles(latencias_ms, n=100)[94]
    print(f"\n--- {nome} ---")
    print(f"Execuções: {len(latencias_ms)}")
    print(f"Latência Média: {statistics.mean(latencias_ms):.3f} ms")
    print(f"Latência Mediana: {statistics.median(latencias_ms):.3f} ms")
    print(f"Latência Mínima: {min(latencias_ms):.3f} ms")
    print(f"Latência Máxima: {max(latencias_ms):.3f} ms")
    print(f"P95: {p95:.3f} ms")


def main() -> None:
    print("Carregando modelo original (scikit-learn)...")
    pipeline_original = joblib.load(MODELO_ORIGINAL_PATH)

    print("Carregando modelo otimizado (ONNX Runtime)...")
    sessao_onnx = rt.InferenceSession(
        MODELO_ONNX_PATH, providers=["CPUExecutionProvider"]
    )
    input_name = sessao_onnx.get_inputs()[0].name
    label_name = sessao_onnx.get_outputs()[0].name

    def inferir_original():
        pipeline_original.predict([TEXTO_TESTE])

    def inferir_onnx():
        # Força o array a ter 2 dimensões (coluna única) para satisfazer o Rank 2 esperado pelo ONNX
        x_input = np.array([TEXTO_TESTE], dtype=object).reshape(-1, 1)
        sessao_onnx.run([label_name], {input_name: x_input})

    latencias_original = medir_latencias(inferir_original, NUM_EXECUCOES, WARMUP)
    latencias_onnx = medir_latencias(inferir_onnx, NUM_EXECUCOES, WARMUP)

    imprimir_resultados("Modelo Original (scikit-learn/.pkl)", latencias_original)
    imprimir_resultados("Modelo Otimizado (ONNX Runtime)", latencias_onnx)

    media_original = statistics.mean(latencias_original)
    media_onnx = statistics.mean(latencias_onnx)
    ganho_pct = (1 - media_onnx / media_original) * 100

    print("\n--- Resumo Comparativo ---")
    if ganho_pct > 0:
        print(f"O modelo ONNX é {ganho_pct:.1f}% mais rápido em média.")
    else:
        print(f"O modelo ONNX é {abs(ganho_pct):.1f}% mais lento em média.")


if __name__ == "__main__":
    main()