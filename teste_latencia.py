import requests
import time
import statistics

# Configurações do teste
url = "http://localhost:8001/predict"

payload = {
    "texto": "Paciente relata dor torácica aguda e falta de ar. Histórico de hipertensão."
}

headers = {
    "Content-Type": "application/json"
}

num_requests = 100

latencias = []

print(f"Iniciando envio de {num_requests} requisições para {url}...")

# Aquecimento (Warm-up)
requests.post(url, json=payload, headers=headers)

for i in range(num_requests):

    start_time = time.time()

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    end_time = time.time()

    if response.status_code == 200:

        latencia_ms = (end_time - start_time) * 1000
        latencias.append(latencia_ms)

    else:
        print(f"Erro na requisição {i + 1}: {response.status_code} - Detalhes: {response.text}")
        break # Interrompe o teste no primeiro erro para podermos ler a mensagem


# Resultados
if latencias:

    print("\n--- Resultados do Baseline de Latência (Local) ---")

    print(f"Total de requisições bem-sucedidas: {len(latencias)}")

    print(f"Latência Média: {statistics.mean(latencias):.2f} ms")

    print(f"Latência Mediana: {statistics.median(latencias):.2f} ms")

    print(f"Latência Mínima: {min(latencias):.2f} ms")

    print(f"Latência Máxima: {max(latencias):.2f} ms")

    p95 = statistics.quantiles(latencias, n=100)[94]

    print(f"P95 (95% das requisições abaixo de): {p95:.2f} ms")