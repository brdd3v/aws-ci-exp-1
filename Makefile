# Makefile

install:
	pip3 install -r requirements.txt

init:
	terraform init

validate:
	terraform validate

run-localstack:
	docker pull localstack/localstack
	localstack start -d
	echo "Waiting for LocalStack startup..."
	localstack wait -t 30
	echo "Startup complete"

deploy-local:
	tflocal apply --auto-approve

# deploy:
# 	terraform apply --auto-approve

lint:
	python3 -m pylint --disable=R,C *.py tests/*.py --fail-under=8

test:
	python3 -m pytest -vv tests/
