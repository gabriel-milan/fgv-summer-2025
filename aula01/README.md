# Aula 01

Slides: https://docs.google.com/presentation/d/1r_-6uFc6sHtl457LrfHIcb6WOOz5mkMyglCqnCVYciE/edit?usp=sharing

## Scripts

- `01_raw.py`: Implementação mais crua possível
- `02_fixed.py`: Conserta erros de diretórios inexistentes
- `03_prefect.py`: Acrescenta orquestração
- `04_random_failure.py`: Acrescenta falha aleatória no download (simulação de ambiente instável para extração de dados)
- `05_retries.py`: Acrescenta reexecução em caso de falha
- `06_dependencies.py`: Acrescenta o encadeamento entre as tarefas

## Leituras extras
- ["The Prefect Hybrid Model"](https://medium.com/the-prefect-blog/the-prefect-hybrid-model-1b70c7fd296)
- [Gerenciamento de estados no Prefect v3](https://docs.prefect.io/v3/develop/manage-states#manage-states)
- [Concorrência e paralelismo no Prefect v3](https://docs.prefect.io/v3/develop/task-runners)

## Tarefas

1. Implementar exemplo com execução paralelismo ou concorrência