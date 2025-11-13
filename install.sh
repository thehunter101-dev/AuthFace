python -m venv .entorno
source .entrono/bin/activate
pip install poetry

cd auth-backend
poetry install

cd ..
cd auth-frontend
poetry install
deactivate