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

Comparativo de Latência (Baseline vs. Otimizado)
Os testes de carga foram executados simulando 100 requisições concorrentes em ambiente containerizado local. O escopo compara a API inicial (mock) com a API executando inferência real de Machine Learning otimizada via ONNX Runtime:

### Comparativo de Latência

A tabela abaixo apresenta o comparativo de desempenho entre a API Mockada (Baseline) e o Modelo Otimizado utilizando ONNX, considerando 100 requisições realizadas para cada abordagem.

| Métrica de Latência | Baseline (API Mockada) | Modelo Otimizado (ONNX) |
|---|---:|---:|
| Requisições Bem-Sucedidas | 100 (100%) | 100 (100%) |
| Latência Média | 7,98 ms | 9,50 ms |
| Latência Mediana | 7,45 ms | 8,51 ms |
| Latência Mínima | 2,60 ms | 0,00 ms |
| Latência Máxima | 16,00 ms | 23,18 ms |
| Percentil 95 (P95) | 12,79 ms | 18,85 ms |

O modelo otimizado com ONNX entrega inferências complexas de NLP (TF-IDF + Random Forest) mantendo a latência na faixa de milissegundos, atendendo com folga aos requisitos de sistemas clínicos críticos.