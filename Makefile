include ./Makefile.variables.mk

HERE := $(PROJECT_DIR)
VENV := $(VENV_DIR)
PYTHONPATH := ${HERE}/src
TEST_PARAMS := --verbosity 2 --pythonpath "${PYTHONPATH}"
PSQL_PARAMS := --host=localhost --username=anastasiataranova --password
SRC_DIR = $(HERE)/src
SLS_SRC_DIR = $(HERE)/serverless/src


ifeq ($(ENV_FOR_DYNACONF), travis)
	RUN :=
	TEST_PARAMS := --failfast --keepdb --verbosity 1 --pythonpath "${PYTHONPATH}"
	PSQL_PARAMS := --host=localhost --username=postgres --no-password
else ifeq ($(ENV_FOR_DYNACONF), heroku)
	RUN :=
endif


MANAGE := ${PY} src/manage.py


.PHONY: format
format:
	$(call log, formatting code)
	${RUN} isort --virtual-env "${VENV}" "${SRC_DIR}"
	${RUN} black "${SRC_DIR}"


.PHONY: createsuperuser
createsuperuser:
	${MANAGE} createsuperuser


.PHONY: run
run:
	$(call log, starting local server)
	${MANAGE} runserver


.PHONY: beat
beat:
	$(call log, starting beat)
	PYTHONPATH=${PYTHONPATH} \
	${RUN} celery worker \
		--app periodic.app -B \
		--config periodic.celeryconfig \
		--workdir "${SRC_DIR}" \
		--loglevel=info


.PHONY: docker
docker: wipe
	docker-compose build


.PHONY: docker-run
docker-run: docker
	docker-compose up


.PHONY: static
static:
	$(call log, collecting static)
	${MANAGE} collectstatic --noinput --clear -v0


.PHONY: migrations
migrations:
	${MANAGE} makemigrations

.PHONY: lambda
lambda:
	(cd serverless && sls deploy)


.PHONY: lambda-clean
lambda-clean:
	rm -rf serverless/.serverless


.PHONY: lambda-remove
lambda-remove:
	(cd serverless && sls remove)



.PHONY: migrate
migrate:
	$(call log, applying migrations)
	${MANAGE} migrate


.PHONY: su
su:
	${MANAGE} createsuperuser


.PHONY: sh
sh:
	${MANAGE} shell


.PHONY: test
test:
	ENV_FOR_DYNACONF=test \
	${RUN} coverage run \
		src/manage.py test ${TEST_PARAMS} \
			apps \
			project \

	${RUN} coverage report
	${RUN} isort --virtual-env "${VENV}" --check-only "${SRC_DIR}"
	${RUN} isort --virtual-env "${VENV}" --check-only "${SLS_SRC_DIR}"
	${RUN} black --check "${SRC_DIR}"
	${RUN} black --check "${SLS_SRC_DIR}"


.PHONY: report
report:
	${RUN} coverage html --directory="${HERE}/htmlcov${HERE}/htmlcov" --fail-under=0
	open "${HERE}/htmlcov/index.html"


.PHONY: venv
venv:
	$(call log, installing packages for venv)
	@$(PIPENV_INSTALL) --dev


.PHONY: clean
clean:
	${RUN} coverage erase
	rm -rf htmlcov
	find . -type d -name "__pycache__" | xargs rm -rf
	rm -rf ./.static/


.PHONY: clean-docker
clean-docker:
	docker-compose stop || true
	docker-compose down || true
	docker-compose rm --force || true
	docker system prune --force


.PHONY: wipe
wipe: clean clean-docker lambda-clean


.PHONY: resetdb
resetdb:
	psql ${PSQL_PARAMS} \
		--dbname=postgres \
		--echo-all \
		--file="${HERE}"/ddl/reset_db.sql \
		--no-psqlrc \
		--no-readline \


.PHONY: initdb
initdb: resetdb migrate

