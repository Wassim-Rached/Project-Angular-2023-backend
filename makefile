# start
start-dev:
	ENV=DEVELOPMENT python manage.py runserver 

start-prod:
	ENV=PRODUCTION python manage.py runserver 

# migrate
m-dev:
	ENV=DEVELOPMENT python manage.py migrate

m-prod:
	ENV=PRODUCTION python manage.py migrate 

# makemigrations
mm:
	ENV=DEVELOPMENT python manage.py makemigrations

# collect statistics
collect-static:
	python manage.py collectstatic --no-input

# package management 
pip-install-prod:
	pip install -r requirements.prod.txt

pip-install-dev:
	pip install -r requirements.dev.txt

# deployment
production-ready-start:
	ENV=PRODUCTION gunicorn core.wsgi:application

