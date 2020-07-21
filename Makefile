# Utility commands for rebuilding && testing functions

install:
	npm i --save serverless-python-requirements

deploy:
	serverless deploy

test:
	serverless invoke local --function analysis --path test/data.json

.PHONY: install deploy test