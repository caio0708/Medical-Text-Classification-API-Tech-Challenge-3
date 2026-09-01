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