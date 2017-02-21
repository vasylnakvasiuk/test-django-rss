run:
	./manage.py runserver
make:
	./manage.py makemigrations
migrate:
	./manage.py migrate
super:
	./manage.py createsuperuser
shell:
	./manage.py shell_plus
celery:
	celery -A rss.celery worker --loglevel=info

.PHONY: run make migrate super shell celery
