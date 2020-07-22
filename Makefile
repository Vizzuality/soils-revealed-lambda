# Utility commands for rebuilding && testing functions

install:
	npm install

deploy:
	serverless deploy

test:
	serverless invoke local --function analysis --path test/data.json

deploy-local:
	serverless deploy --stage local --region us-east-1
	serverless invoke -f analysis --stage local --path test/data.json

up-local:
	docker-compose up -d

down-local:
	docker-compose down

.PHONY: install deploy test deploy-local up-local down-local