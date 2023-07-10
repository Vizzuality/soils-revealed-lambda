# Soils analysis service.

This service supports soils revealed website, being implemented as a subpath.
## Requirements:

- Docker
- Docker-compose

## Getting started:

### Development

```
./service.sh develop
```

Server will run on port: 5020

### Production 

```
./service.sh start
```

Server will run on port: 8000

## Project structure
```
+analysis
    +-----data
    +-----src
        +---main.py
        +---utils.py
        +---validator.py
        +---errors.py
```

## Gunicorn configuration

Gunicorn is configured on file `gunicorn.py`.

## Service work

Example request (also see: [Testing](#testing))

```
POST http://${API_URL}/api/v1/analysis
```

POST body (as JSON):

```json
{"dataset": "experimental",
    "variable": "stocks",
        "years": ["2010", "2017"],
        "depth": "0-30",
        "geometry": {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {},
          "geometry": {
            "type": "Polygon",
            "coordinates": [
              [
                [
                  -59.58984374999999,
                  -31.69078180613681
                ],
                [
                  -59.150390625,
                  -31.69078180613681
                ],
                [
                  -59.150390625,
                  -31.37239910488051
                ],
                [
                  -59.58984374999999,
                  -31.37239910488051
                ],
                [
                  -59.58984374999999,
                  -31.69078180613681
                ]
              ]
            ]
          }
        }
      ]
    }
    }
```

## Testing

Folder test, contains a JSON data files, `curl-format.txt`, and `test_analysis_endpoint.py`, usefull for testing. In the example bellow we used `service.sh develop` to run a local server on port `5020`.

```bash 
# At project root level
./service.sh develop
```

**Testing using curl**:

```bash
cd ./test
curl -v -w "@curl-format.txt" -H "Content-Type: application/json" -d @data.json http://localhost:5020/api/v1/analysis
```

**Testing with pytest**:
To run the tests using `pytest`, follow these steps:
1. Make sure you have `pytest` installed. You can install it using pip:
```shell
pip install pytest
```
2. Open a terminal and navigate to the test folder.
```shell
cd ./test
```
3. Run the following command to execute the tests:
```shell
pytest
```
The tests will be automatically discovered and executed. They will send requests to the analysis endpoint using different payloads and validate the responses.
