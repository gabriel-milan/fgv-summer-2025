# Aulas 03 e 04 - dbt



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
3. Obtenha o arquivo de credenciais do Google Cloud `rj-sms-dev-dbt.json`.
4. Copie o arquivo `./profiles.yml` para o diretório de sua preferência.
 5. Na cópia do arquivo `profiles.yml` altere o path da chave `keyfile` no profile `dev` para onde está armazenada suas credenciais do Google Cloud.
 6. Crie uma variável de ambiente `DBT_PROFILES_DIR` apontando para o diretório onde está a cópia do `profiles.yml` 

    **ex.** DBT_PROFILES_DIR='/Users/foo/.credentials/'


### 3. Configuração do ambiente de dev
7. Crie uma variável de ambiente `DBT_USER` com o nome de usuário de sua preferência 
8. Dê privilegio de execução para o script `./recce.sh`
    - **Linux e MacOS**: `chmod +x recce.sh`
    - **Windows**: Não precisa
