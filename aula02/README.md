# Aula 02

Slides: https://docs.google.com/presentation/d/12EgmYY7QomFQsHPfAlsAr-eiANdb_e5DQP9cdPo_quQ/edit?usp=sharing

## Pendências da aula anterior

### Como observar a interface gráfica

1. Executar o servidor do Prefect

```bash
prefect server start
```

2. Em outro terminal, configurar o Prefect para usar o servidor local

```bash
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```

3. Executar seu fluxo normalmente

```bash
python seu_flow.py
```

4. Acessar o endereço http://127.0.0.1:4200 para ver o dashboard

## Arquivos

- `data_generator.py`: Implementação de uma função que gera dados aleatórios
- `gcp.py`: Implementação de funções úteis para interagir com o Google Cloud Platform
- `main.py`: Exemplo da aula

### Reflexões quanto ao exemplo

- Origem: dados gerados aleatoriamente
    - Reprodutível? **Não**
    - Necessita ordenação? **Não**
- Destino: Google Cloud Storage
    - Sobrescritível? **Não** (não temos como sobrescrever somente parte dos dados)
- Pipeline
    - Incremental ou full refresh? **Full refresh**
    - Extração (time ranged, full snapshot, lookback ou streaming): **Full snapshot**
    - Idempotência: **Não** (não existe garantia do mesmo resultado)
    - Self-healing: **Não** (se falhou, falhou)
    - Estrutura (multi-hop, dinâmico, desconectado): **Nenhum** (não estamos fazendo transformações, nem fluxos alternativos, nem triggers ao final do load no destino)


## Leituras extras
- [Design Patterns](https://www.startdataengineering.com/post/design-patterns/) (material de referência para a aula)

## Tarefas

1. Reflita sobre o seu projeto. Decida como será seu pipeline de dados, com base nos prós e contras mencionados na aula e também levando em consideração as restrições impostas pelo seu projeto (e suas bases de dados).