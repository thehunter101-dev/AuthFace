cd auth-backend
poetry run python manage.py &

cd ..
cd auth-frontend
poetry run python main.py &