mkdir tech_challenge1
touch tech_challenge1/__init__.py
touch README.md

poetry add fastapi requests pandas beautifulsoup4 uvicorn
poetry add --dev pytest
poetry add python-jose[cryptography] passlib[bcrypt]
poetry add sqlalchemy
poetry add python-multipart
poetry add pydantic-settings
poetry add --dev httpx


mkdir api api/routes scripts data tests models utils

poetry lock
poetry install
poetry env info

poetry self add poetry-plugin-shell
poetry shell


git --version
git inti

echo > .gitignore

# Byte-compiled / cache
__pycache__/
*.py[cod]
*.so

# Virtual environments
.venv/
.env
.env.*

# Data/output
*.csv
*.log
*.sqlite3
data/
api/data/

# VSCode/PyCharm
.vscode/
.idea/

# Poetry
poetry.lock

# OS files
.DS_Store
Thumbs.db


git add .
git commit -m "Inicio do projeto"
git remote add origin https://github.com/IbniB/tech_challenge1.git
git branch -M main
git push -u origin main

