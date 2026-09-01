Decisão Arquitetural (Rascunho para o README)

A Etapa 1 exige uma definição textual da estratégia de deploy em nuvem para este cenário de triagem médica. 

Provedor Sugerido: AWS (Amazon Web Services).

Estratégia Real-time vs Batch: Como o sistema é para triagem em um "hospital de referência" e necessita de classificação rápida, a arquitetura deve ser Real-time (tempo real).

Serviço de Deploy: Utilização do AWS ECS (Elastic Container Service) com AWS Fargate para rodar o container Docker criado sem a necessidade de gerenciar servidores subjacentes. 
A API seria exposta via Application Load Balancer (ALB) para distribuir requisições e garantir alta disponibilidade. 
Esta abordagem suporta picos de chamadas (ex: integração contínua do sistema do hospital) e simplifica o acoplamento futuro com o pipeline de CI/CD do GitHub Actions.  

Baseline de latência:
- Requisições: 100
- Sucesso: 100%
- Média: 7,98 ms
- Mediana: 7,45 ms
- Mínima: 2,60 ms
- Máxima: 16,00 ms
- P95: 12,79 ms

---


--- Resultados do Baseline de Latência (Local) ---
Total de requisições bem-sucedidas: 100
Latência Média: 9.50 ms
Latência Mediana: 8.51 ms
Latência Mínima: 0.00 ms
Latência Máxima: 23.18 ms
P95 (95% das requisições abaixo de): 18.85 ms
=========

Medical Text Classification API - Tech Challenge Fase 3
Sistema de triagem automática de laudos médicos desenvolvido para classificar níveis de urgência em tempo real, contemplando pipeline de CI/CD, orquestração de treino, observabilidade com Prometheus/Grafana e otimização de latência com ONNX Runtime

Decisão Arquitetural (Deploy em Nuvem):
Para atender a um hospital de referência com exigência de triagem clínica imediata, a estratégia arquitetural foi desenhada com foco em baixa latência e disponibilidade contínua:

Estratégia Real-time vs Batch: Adotou-se o modelo Real-time via API REST síncrona. O fluxo clínico exige resposta imediata ao submeter um laudo, descartando processamento em lote (batch).

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