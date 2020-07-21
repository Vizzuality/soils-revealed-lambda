<!--
title: 'AWS Python Rest API for soils'
description: 'AWS Python Rest API with for soils on the fly analysis'
layout: Doc
framework: v1
platform: AWS
language: python
authorLink: 'https://github.com/vizzuality'
authorName: 'Vizzuality'
authorAvatar: ''
-->

# soils-revealed-lambda
Lambda Function for calculations for Soils Revealed
Dont forget to configure the requierment variables like aws credentials

## Deploy the Serverless API to AWS
This will depend on aws.

1. Install Serverless

    ```
    npm install -g serverless
    ```

2. Install `serverless-python-requirements`

    ```
    npm i --save serverless-python-requirements
    ```

3. Define necessary environment variables

    set up `.env` file

4. Develop and test your function locally

    ```
    make test
    ```
    or 

    ```
    serverless invoke local --function main.analysis --path test/data.json
    ```

5. Deploy the API

    ```
    sls deploy
    ```
    or 

    ```
    make deploy
    ```

    Your results should look something like this:
    ```
    Serverless: Stack update finished...
    Service Information
    service: soils
    stage: dev
    region: us-east-1
    stack: soils-dev
    resources: 12
    api keys:
    None
    endpoints:
    POST - https://330sknmxi0.execute-api.us-east-1.amazonaws.com/dev/hello
    functions:
    analysis: soils-dev-analysis
    layers:
    pythonRequirements: arn:aws:lambda:us-east-1:480627813539:layer:soils-dev-python-requirements:4
    Serverless: Removing old service artifacts from S3...
    Serverless: Run the "serverless" command to setup monitoring, troubleshooting and testing.
    ```

## Test the API by Creating and Querying items

Substitute your endpoints into these curl commands to test the Create, Read, and Delete operations


### POST

```
curl --request POST \
  --url https://330sknmxi0.execute-api.us-east-1.amazonaws.com/dev/hello \
  --header 'content-type: application/json'
```

#### Expected Response

200 status

```
{
  "_id": "c6f03ca0-f792-11e9-9534-260a4b91bfe9",
  "data": {
    "attribute_1": "Pet",
    "attribute_2": "Rock"
  }
}
```