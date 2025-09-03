# FastAPI + MySQL — Docker Compose

Projeto de **containerização completa com Docker Compose**

## 1) Projeto ✅
**Projeto:** API de transações da DimDim (FastAPI) + Banco MySQL (CRUD simples).  

### Arquitetura atual (antes da containerização)
```mermaid
flowchart LR
    U[Usuário] -->|HTTP| App[FastAPI na máquina do dev]
    App -->|Driver| MySQL[MySQL instalado localmente]
```
**Pontos fracos:** configuração manual, dependências locais, difícil replicar ambiente.

### Arquitetura futura (com Docker Compose)
```mermaid
flowchart LR
    U[Usuário] -->|HTTP:8000| API[Container FastAPI]
    API -->|TCP:3306| DB[(Container MySQL)]
    subgraph Docker Host
      API --- DB
      subgraph Compose Network (app-net)
      end
      subgraph Volumes
        V1[(mysql-data)]
      end
    end
```
**Benefícios:** reprodutibilidade, isolamento, facilidade de subir/parar, padronização, IaC. Mais economia e eficiência para a DimDim.

## 2) Análise da Arquitetura ✅
- **Serviços do projeto:**
  1. `api` — FastAPI (Python 3.12) — imagem oficial `python:3.12-slim` (Dockerfile)  
  2. `db` — MySQL 8.0 — imagem oficial `mysql:8.0`
- **Dependências:** `api` depende de `db` (conexão TCP 3306). No Compose, `depends_on` com `service_healthy` garante ordem correta.
- **Estratégia de containerização:**
  - **API:** Dockerfile com usuário não-root, healthcheck HTTP, `uvicorn` como entrypoint.
  - **DB:** imagem oficial MySQL + `init.sql` montado via volume para criar schema/tabela/seed.

## 3) Implementação Docker Compose ✅
Arquivo: [`docker-compose.yml`](./docker-compose.yml)

- **Serviços definidos:** `api`, `db`
- **Redes:** `app-net` (bridge)
- **Volumes:** `mysql-data` (persistência) + `./initdb` (scripts de init)
- **Variáveis de ambiente:** via `.env`
- **Política de restart:** `on-failure`
- **Portas expostas:** `8000:8000` (API) e `3306:3306` (DB — opcional; remova caso não precise acesso externo)
- **Health checks:**
  - `api`: `curl http://localhost:8000/health`
  - `db`: `mysqladmin ping`
- **Usuário sem privilégios:** definido no `Dockerfile` da API (user `appuser`).

## 4) Como rodar (Deploy passo a passo) ✅
### Pré-requisitos
- Docker Desktop **ou** Docker Engine (Compose v2)
- Portas livres: 8000 (API) e opcional 3306 (MySQL)

### Passos
```bash
cp .env.example .env

nano .env  

docker compose up -d --build

docker compose ps
docker compose logs -f api 
docker compose logs -f db

curl http://localhost:8000/health  # {"status":"ok"}
```

### Testes de CRUD
```bash
# LIST
curl -s http://localhost:8000/transactions | jq .

# CREATE
curl -s -X POST http://localhost:8000/transactions   -H "Content-Type: application/json"   -d '{"descricao":"Compra supermercado","valor":150.75}' | jq .

# UPDATE
curl -s -X PUT http://localhost:8000/transactions/1   -H "Content-Type: application/json"   -d '{"descricao":"Compra supermercado - ALTERADO","valor":151.00}' | jq .

# DELETE
curl -s -X DELETE http://localhost:8000/transactions/1 -w "\nStatus: %{http_code}\n" -o /dev/null
```

### Conferindo no Banco
```bash
docker compose exec db mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} -e "USE ${MYSQL_DATABASE}; SELECT * FROM transactions;"
```

## Comandos essenciais do Docker Compose ✅
```bash
docker compose up -d --build         # subir
docker compose ps                    # listar
docker compose logs -f api           # logs app
docker compose logs -f db            # logs banco
docker compose exec db bash          # entrar no container do banco
docker compose down -v               # remover tudo
docker system prune -a -f --volumes  # limpar laboratório por completo
```

## Estrutura de Pastas
```
transactions-dimdim/
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ dependencies.py
│  ├─ common/
│  │  ├─ __init__.py
│  │  ├─ config.py
│  │  ├─ crud.py
│  │  ├─ database.py
│  │  ├─ models.py
│  │  └─ schemas.py
│  └─ routers/
│     ├─ __init__.py
│     ├─ health.py
│     └─ transactions.py
├─ initdb/
│  └─ init.sql
├─ .env.example
├─ docker-compose.yml
├─ Dockerfile
├─ requirements.txt
└─ README.md
```
