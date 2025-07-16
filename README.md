Tech Challenge 1 - API de Livros

API pública para consulta e análise de livros, baseada em scraping de https://books.toscrape.com. Implementa autenticação JWT, endpoints ML-ready e monitoramento.

🔐 Desafio 1: API & Autenticação

POST /api/v1/auth/login: Gera token de acesso (Bearer).

POST /api/v1/auth/refresh: Renova token de acesso.

POST /api/v1/scraping/trigger (Admin): Inicia scraping de novos dados (protegido).

🤖 Desafio 2: Pipeline ML-Ready

GET /api/v1/ml/features: Retorna lista de features (price, rating, category, availability).

GET /api/v1/ml/training-data: Dataset completo para treinamento (JSON).

POST /api/v1/ml/predictions: Recebe JSON com features e retorna predição.

📊 Desafio 3: Monitoramento & Analytics

Logs estruturados: Gravados em logs/app_YYYY-MM-DD.log, expostos em GET /api/v1/logs.

Métricas Prometheus: Expostas em GET /api/v1/metrics.

Dashboard Streamlit: Frontend simples para visualização de dados e métricas (scripts/dashboard.py).

🚀 Instalação & Setup

# Clonar o repositório
git clone https://github.com/IbniB/tech_challenge1.git
cd tech_challenge1

# Instalar dependências
poetry install

# Configurar variáveis de ambiente
cp .env.example .env  # ou crie .env manualmente
# Ajuste SECRET_KEY, DATABASE_URL, DASHBOARD_USER e DASHBOARD_PASSWORD

⚙️ Executando Localmente

# Iniciar API
uvicorn tech_challenge1.api.main:app --reload

# Acessar Swagger UI
en http://localhost:8000/docs

# Executar Dashboard Streamlit
poetry run streamlit run tech_challenge1/scripts/dashboard.py

🗂 Estrutura do Projeto

tech_challenge1/
├── api/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── books.py
│   │   ├── ml.py
│   │   ├── stats.py
│   │   ├── metrics.py
│   │   └── logs.py
│   └── main.py
├── core/
│   ├── settings.py
│   └── security.py
├── db/
│   └── database.py
├── models/
│   └── book_model.py
├── scripts/
│   └── dashboard.py
├── utils/
│   └── logging.py
├── tests/
│   └── (Pytest files)
├── data/
│   └── (datasets)
├── pyproject.toml
├── README.md
└── .env

🏗️ Arquitetura

+-------------------+
| Scraping (BS4)    |
+-------------------+
        ↓
+-------------------+
| Processamento     |
| - Limpeza         |
| - Feature Eng.    |
+-------------------+
        ↓
+-------------------+
| API FastAPI       |
| - Auth            |
| - Endpoints ML    |
| - Trigger Admin   |
+-------------------+
        ↓
+-------------------+
| Consumo externo   |
| - Data Scientist  |
| - Dashboard       |
+-------------------+

☁️ Deploy no Render

Crie um novo serviço Web no Render.

Use este arquivo render.yaml:

services:
  - type: web
    name: tech-challenge1-api
    runtime: python
    region: oregon
    plan: free

    buildCommand: |
      pip install poetry
      poetry config virtualenvs.create false
      poetry install --no-dev

    startCommand: uvicorn tech_challenge1.api.main:app --host 0.0.0.0 --port 10000

    envVars:
      - key: SECRET_KEY
      - key: ALGORITHM
      - key: ACCESS_TOKEN_EXPIRE_MINUTES
      - key: DATABASE_URL
      - key: ENVIRONMENT
      - key: DASHBOARD_USER
      - key: DASHBOARD_PASSWORD

git push render main

✅ Testes

poetry run pytest

🛠️ Próximos Passos

Integrar frontend do Dashboard diretamente no Render ou hospedar separadamente.

Aprimorar métricas com painel Prometheus/Grafana.

Adicionar CI/CD para deploy automático.

Expandir pipeline ML: fine-tuning, comparação de modelos.

