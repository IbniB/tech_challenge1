Tech Challenge 1 — API de Livros

Resumo
API pública para consulta e análise de livros a partir de scraping do https://books.toscrape.com. Inclui autenticação JWT, endpoints prontos para ML, monitoramento (logs e métricas) e um pequeno dashboard. Este README segue boas práticas, define critérios claros e traz uma arquitetura técnica e de Git para facilitar colaboração.

Índice
- Visão Geral e Objetivos
- Critérios e Boas Práticas
- Requisitos
- Instalação e Setup
- Execução Local
- Autenticação (JWT)
- Documentação dos Endpoints
- Arquitetura (Aplicação, Dados e Observabilidade)
- Estratégia de Git (Arquitetura de Branches)
- Padrões de Commits (Conventional Commits)
- Contribuição (PRs e Revisões)
- Testes
- Deploy (Render)
- Troubleshooting
- Roadmap

Visão Geral e Objetivos
- Fornecer uma API segura (JWT) para consulta e análise de livros raspados do Books to Scrape.
- Expor dados para uso em Data Science/ML e um dashboard simples de visualização.
- Oferecer observabilidade mínima (logs e métricas Prometheus) e uma estratégia de colaboração via Git.

Critérios e Boas Práticas
- Segurança: todos os endpoints sensíveis exigem Bearer Token; senhas com hash; JWT com expiração.
- Confiabilidade: logs estruturados diários; health-check; métricas para Prometheus.
- Qualidade: testes com Pytest; linters/formatadores (recomendado: black/ruff) — opcional.
- Manutenibilidade: arquitetura modular, convenções de código e commits, documentação dos endpoints.

Requisitos
- Python 3.11+
- Poetry
- SQLite (já embutido; DB local por padrão)

Instalação e Setup
1) Clonar o repositório
   git clone https://github.com/IbniB/tech_challenge1.git
   cd tech_challenge1

2) Instalar dependências
   poetry install

3) Configurar variáveis de ambiente (.env na raiz)
   Exemplo de .env:
   SECRET_KEY=troque-por-uma-chave-secreta
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ENVIRONMENT=development
   DATABASE_URL=sqlite:///./tech_challenge1.db
   DASHBOARD_USER=admin
   DASHBOARD_PASSWORD=admin

Execução Local
- Iniciar API (FastAPI/Uvicorn)
  poetry run uvicorn tech_challenge1.api.main:app --reload
  Swagger/OpenAPI: http://localhost:8000/docs
  Health Check:     GET http://localhost:8000/api/v1/health

- Dashboard (opcional)
  poetry run streamlit run tech_challenge1/scripts/dashboard.py

- Popular CSV localmente (opção 1)
  poetry run python -m tech_challenge1.scripts.scrape
  (o script salva em api/data/livros.csv)

- Popular CSV via API (opção 2)
  - Gere token (login) e chame POST /api/v1/scraping/trigger
  - O arquivo será salvo em data/livros.csv (raiz); mova-o para api/data se for usar os endpoints Books imediatamente

Autenticação (JWT)
- Registro
  POST /api/v1/auth/register
  body (JSON): {"username": "user", "password": "pass"}

- Login (OAuth2PasswordRequestForm)
  POST /api/v1/auth/login
  form-data: username, password
  resposta: {"access_token": "...", "token_type": "bearer"}
  Use o token como Authorization: Bearer <token>

Documentação dos Endpoints
- Health
  GET /api/v1/health — status geral (público)

- Books (protegidos: requer Bearer)
  GET /api/v1/books — lista todos os livros (lidos de api/data/livros.csv)
  GET /api/v1/books/search?title=&category= — busca por título e/ou categoria
  GET /api/v1/books/categories — lista categorias
  GET /api/v1/books/{book_id} — detalhe por índice na lista

- Stats
  GET /api/v1/stats/overview — visão geral (protegido: Bearer)
  GET /api/v1/stats/categories — agregações por categoria (público)
  GET /api/v1/stats/top-rated — top livros por rating (público)
  GET /api/v1/stats/price-range?min=&max= — filtro por preço (público)

- ML (protegidos: Bearer)
  GET /api/v1/ml/features — [price, rating, category, availability]
  GET /api/v1/ml/training-data — dados simulados para treino
  POST /api/v1/ml/predictions — body: {price, rating, category, availability}

- Scraping (protegido: Bearer)
  POST /api/v1/scraping/trigger — dispara scraping em background; salva em data/livros.csv (raiz do projeto)
  Observação importante: os endpoints Books leem api/data/livros.csv. Para popular api/data/livros.csv, use o script local abaixo ou mova o CSV gerado da raiz para api/data.

- Logs
  GET /api/v1/logs/ — últimas 200 linhas do logs/app_YYYY-MM-DD.log

- Métricas Prometheus
  GET /api/v1/metrics — endpoint exposto pelo instrumentator

Arquitetura (Aplicação, Dados e Observabilidade)
- Camadas
  1) Scraping (scripts/scrape.py): coleta e parse com requests + BeautifulSoup.
  2) Processamento: normalização e enriquecimento simples (ex.: coluna id, preço numérico em stats).
  3) API (FastAPI): autenticação JWT, endpoints Books, ML, Stats, Logs, Metrics.
  4) Consumo: Data Science, Dashboard, integrações externas.

- Fluxo de dados (alto nível)
  books.toscrape.com → scrape.py → data/livros.csv → API (Books/Stats/ML) → clientes (DS, Dashboard)

- Observabilidade
  Logs: logs/app_YYYY-MM-DD.log (loguru), expostos via /api/v1/logs/
  Métricas: Prometheus via /api/v1/metrics (latência, throughput, etc.)

Estratégia de Git (Arquitetura de Branches)
- Branches
  main: produção (estável)
  develop: integração (próximo release)
  feature/<nome-curto>: novas funcionalidades originadas de develop
  fix/<issue-curto> ou hotfix/<id>: correções rápidas (hotfix a partir de main)
  release/<versão>: estabilização antes de ir para main

- Fluxo
  1) Crie branch a partir de develop (ou de main para hotfix).
  2) Commits seguindo Conventional Commits (ver abaixo).
  3) Abra Pull Request com descrição, checklist e link para issue.
  4) Revisão e squash-merge em develop; releases são mescladas em main com tag.

Padrões de Commits (Conventional Commits)
- Formato: tipo(escopo opcional): descrição
  Exemplos:
  - feat(auth): adicionar endpoint de registro
  - fix(books): corrigir path do CSV
  - docs(readme): atualizar instruções de deploy
  - refactor(api): extrair middleware de logs
  - test(stats): cobrir price-range com limites

- Tipos comuns: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert

Contribuição (PRs e Revisões)
- Antes de abrir PR:
  - Rodar testes: poetry run pytest
  - Garantir formatação/lint (sugestão): black, ruff
  - Atualizar README quando necessário
- Na PR:
  - Descrever o problema/solução, screenshots (se aplicável)
  - Checklist de testes locais e impacto
  - Referenciar issues (ex.: Closes #123)

Testes
- Executar
  poetry run pytest
- Estrutura
  tests/ contém testes de saúde e pode ser expandido (unitários/integração)

Deploy (Render)
- Pré-requisitos: configurar variáveis de ambiente no painel do Render (mesmos nomes do .env).
- Arquivo render.yaml (já incluso) define build/start. Resumo:
  buildCommand:
    pip install poetry
    poetry config virtualenvs.create false
    poetry install --no-dev
  startCommand:
    uvicorn tech_challenge1.api.main:app --host 0.0.0.0 --port 10000
- Passos:
  - Conecte o repositório ao Render
  - Configure env vars (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, DATABASE_URL, ENVIRONMENT, DASHBOARD_USER, DASHBOARD_PASSWORD)
  - Faça push na branch principal que o Render monitora (ex.: main)

Troubleshooting
- 401 Unauthorized nos endpoints: confirme envio de Authorization: Bearer <token> e que o token não expirou.
- 404 livros.csv: rode POST /api/v1/scraping/trigger (com token) ou o script de scraping localmente.
- Logs não encontrados: o endpoint /api/v1/logs/ lê o arquivo do dia; gere tráfego para criar o arquivo.
- Métricas não aparecem: acesse /api/v1/metrics após ter feito chamadas na API.
- Erros de env: verifique .env e nomes exigidos em tech_challenge1/core/settings.py.

Roadmap
- Integrar dashboard ao deploy
- Painéis Prometheus/Grafana
- CI/CD (GitHub Actions) com testes e lint
- Expandir pipeline ML (feature store, avaliação de modelos)

