# Aulas 03 e 04 - dbt

Este projeto é baseado no exemplo [jaffle-shop](https://github.com/dbt-labs/jaffle-shop/) e tem como objetivo praticar o uso do dbt (data build tool) para transformação de dados.

Slides da aula:

- [Aula 03](https://docs.google.com/presentation/d/12TiOXYbH-kf4qj1PrcAH_ugihK2_Qsv3xED4LN7nkUM/edit?usp=sharing)

## Índice

1. [Setup](#setup)
2. [Pre-commit and SQLFluff](#pre-commit-and-sqlfluff)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Desenvolvimento](#desenvolvimento)
5. [Comandos Úteis](#comandos-úteis)

## Setup

### IDE e extensões
Para ter uma experiência de desenvolvimento mais completa em relação às funcionalidades do dbt, é recomendada a instalação do [VSCODE](https://code.visualstudio.com/) junto com a extensão [dbt Power Tools](https://marketplace.visualstudio.com/items?itemName=innoverio.vscode-dbt-power-user).


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

## Estrutura do Projeto
```
jaffle_shop/
  ├── models/
  │   ├── staging/
  │   ├── intermediate/
  │   └── marts/
  ├── analyses/
  ├── data-tests/
  ├── macros/
  └── seeds/
```

## Desenvolvimento
1. Antes de começar a desenvolver, certifique-se de que está na branch correta:
```bash
git checkout -b feature/sua-feature
```

2. Para testar suas alterações:
```bash
dbt run
dbt test
```

## Comandos Úteis
- `dbt run`: Executa as transformações
- `dbt test`: Executa os testes
- `dbt docs generate`: Gera a documentação
- `dbt docs serve`: Serve a documentação localmente
- `dbt debug`: Verifica a configuração do projeto

