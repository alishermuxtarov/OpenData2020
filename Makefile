ARGS=$(filter-out $@,$(MAKECMDGOALS))
BRANCH=`git rev-parse --abbrev-ref HEAD`
export DJANGO_SETTINGS_MODULE=config.settings.local


args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

migrate:
	@python manage.py migrate

migrations:
	@python manage.py makemigrations $(ARGS)

run:
	@python manage.py runserver_plus

run_sql:
	@python manage.py runserver_plus --print-sql

celery-cleanup:
	@celery purge -A config -f

celery: celery-cleanup
	@celery -A config worker --loglevel=DEBUG

shell:
	@python manage.py shell_plus || python manage.py shell

shell_sql:
	@python manage.py shell_plus --print-sql

push:
	GIT_SSH_COMMAND='ssh -i opendata2020.uu' git push origin $(BRANCH)

pull:
	@git pull origin $(BRANCH)

ssh-dev:
	@mosh gotlium@193.34.145.57

docs:
	open http://127.0.0.1:8000/api/v1/docs/

pylint:
	$(eval APPS := $(shell [ ! -z "$(ARGS)" ] && echo $(ARGS) || echo "apps" ))
	@pylint --rcfile=.pylintrc --load-plugins pylint_django $(APPS)

test:
	@DJANGO_SETTINGS_MODULE=config.settings.tests python manage.py test $(ARGS)

%:
	@true
