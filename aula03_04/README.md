# Aulas 03 e 04 - dbt

Projeto desenvolvido para a disciplina `Construção de Infraestrutura de Nuvem para Construção de Pipes de Dados` da Escola de Matemática Aplicada da Fundação Getulio Vargas (EMAp-FGV), ministrada pelos professores Thiago Trabach e Gabriel Milan.

Este projeto é baseado no exemplo [jaffle-shop](https://github.com/dbt-labs/jaffle-shop/) e tem como objetivo praticar o uso do dbt (data build tool) para transformação de dados.



## Indíce

1. [Setup](#-setup)

2. [Pre-commit and SQLFluff](#-pre-commit-and-sqlfluff)

## Setup
### 1. Instalação das dependências
1. Instale as bibliotecas python necessárias
```bash
pip install dbt-core dbt-bigquery recce
```
Caso esteja usando o uv, pode usar o comando:
```bash
uv sync
```

2. Instale os pacotes do dbt, mas antes certifique-se de que está no diretório da aula 03
```bash
dbt deps
```

### 2. Configuração da autenticação
1. Salve no diretório de sua preferência a chave de acesso do Google Cloud `emap-summer-2025-matricula.json`.
2. No arquivo `./profiles.yml` localizado na raiz do projeto, altere:
    - `dataset` para o número da sua matrícula seguido de `_dev` ou `_prod`, conforme o ambiente de desenvolvimento ou produção.
    - `keyfile` para o path do arquivo de credenciais do Google Cloud.

