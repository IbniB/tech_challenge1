mkdir tech_challenge1
touch tech_challenge1/__init__.py
touch README.md

poetry add fastapi requests pandas beautifulsoup4
poetry add --dev pytest


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

