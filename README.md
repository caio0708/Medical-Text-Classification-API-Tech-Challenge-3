### Medical Text Classification API - Tech Challenge Fase 3
Sistema de **triagem automática de laudos médicos** desenvolvido para classificar níveis de urgência em tempo real.

O projeto contempla uma arquitetura completa de produção, incluindo:

- API REST para classificação de laudos;
- Pipeline de CI/CD;
- Orquestração de treinamento;
- Observabilidade com Prometheus e Grafana;
- Inferência de Machine Learning otimizada com ONNX Runtime;
- Containerização com Docker;
- Arquitetura preparada para deploy em nuvem utilizando AWS.

## Arquitetura de Deploy em Nuvem

Para atender a um hospital de referência com exigência de **triagem clínica imediata**, a arquitetura foi projetada com foco em **baixa latência, disponibilidade contínua e escalabilidade**.

### Estratégia Real-time vs. Batch

Foi adotado o modelo **Real-time**, utilizando uma API REST síncrona.

O fluxo clínico exige uma resposta imediata após o envio de um laudo para classificação. Dessa forma, o processamento em lote (**Batch**) não atende ao requisito de resposta imediata.

Provedor de Nuvem: AWS (Amazon Web Services).

Orquestração de Containers: Utilização do AWS ECS (Elastic Container Service) com AWS Fargate, permitindo gerenciar o container Docker sem a necessidade de provisionar ou administrar instâncias de servidores subjacentes.

Balanceamento e Escalabilidade: A API é exposta através de um Application Load Balancer (ALB) para distribuir o tráfego de forma equilibrada, garantindo alta disponibilidade e absorvendo picos de requisições provenientes de sistemas integrados do hospital. Esta estrutura acopla-se de forma fluida ao pipeline de CI/CD do GitHub Actions.

## Comparativo de Latência (Baseline vs. Otimizado)

Os testes de latência foram executados em processo utilizando o script `comparar_latencia.py`, realizando 200 execuções com 10 interações de aquecimento (*warmup*), comparando diretamente o modelo serializado do scikit-learn (`.pkl`) contra o modelo otimizado com ONNX Runtime (`.onnx`).

### Resultados de Desempenho

| Métrica de Latência | Modelo Original (scikit-learn/.pkl) | Modelo Otimizado (ONNX Runtime) |
|---|---:|---:|
| Execuções | 200 | 200 |
| Latência Média | 4,238 ms | **0,562 ms** |
| Latência Mediana | 4,420 ms | **0,555 ms** |
| Latência Mínima | 3,262 ms | **0,534 ms** |
| Latência Máxima | 6,434 ms | **0,676 ms** |
| Percentil 95 (P95) | 4,869 ms | **0,601 ms** |

### Resumo Comparativo
O modelo convertido para **ONNX Runtime** apresentou um ganho expressivo de performance, sendo **86,7% mais rápido em média** que o modelo original em scikit-learn, garantindo a baixa latência exigida para o sistema de triagem clínica em tempo real.