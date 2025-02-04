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
Para ter uma experiência de desenvolvimento mais completa em relação às funcionalidades do dbt, é recomendada a instalação do [VS Code](https://code.visualstudio.com/) junto com a extensão [dbt Power Tools](https://marketplace.visualstudio.com/items?itemName=innoverio.vscode-dbt-power-user).


### 1. Instalação das dependências
1. Instale as bibliotecas python necessárias
```bash
pip install dbt-core dbt-bigquery recce
```

2. Instale os pacotes do dbt, mas antes certifique-se de que está no diretório `aula03_04`
```bash
dbt deps
```

### 2. Configuração da autenticação

1. Salve no diretório de sua preferência a chave de acesso do Google Cloud.


2. No arquivo `./profiles.yml` localizado na raiz do projeto, altere:
    - `dataset` para o número da sua matrícula seguido de `_dev` ou `_prod`, conforme o ambiente de desenvolvimento ou produção.
    - `keyfile` para o path do arquivo de credenciais do Google Cloud.


3. Na linha de comando, execute o comando abaixo para verificar se a chave de acesso está sendo carregada corretamente:

```bash
dbt debug
```

Certifique-se que você está na raiz do projeto (pasta `aula03_04`) e que o arquivo de credenciais está no diretório correto.

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
git checkout -b $BRANCH_NAME
```

2. Para testar suas alterações:
```bash
dbt run
dbt test
```

3. Para visualizar as diferenças entre a branch atual e a branch `main`:
```bash
git checkout main
dbt docs generate --target prod --target-path target-base/

git checkout $BRANCH_NAME
dbt build -s "state:modified+" --defer --state target-base/
dbt docs generate

recce server
```

## Comandos Úteis
- `dbt debug`: Verifica a configuração do projeto
- `dbt compile`: Compila os modelos
- `dbt run`: Compila e executa as transformações
- `dbt test`: Compila e executa os testes
- `dbt build`: Compila, executa as transformações e os testes
- `dbt docs generate`: Gera a documentação
- `dbt docs serve`: Serve a documentação localmente


