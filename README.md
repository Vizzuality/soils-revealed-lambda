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

Folder test, contains a JSON data file and a `curl-format.txt`, usefull for testing. In the example bellow we used `service.sh develop` to run a local server on port `8000`.

```bash 
# At project root level
./service.sh develop
```

Testing using curl:

```bash
cd ./test
curl -v -w "@curl-format.txt" -H "Content-Type: application/json" -d @data.json http://localhost:5020/api/v1/analysis
```
