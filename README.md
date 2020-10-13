# Soils analysis service.

## Requirements:

- Docker
- Docker compose

## Getting started:

### Development

```
./service.sh develop
```

### Production 

```
./service.sh start
```

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

## Service work

Example request

```
POST http://${API_URL}/api/v1/analysis
```

POST body (as JSON):

```json
{
    "dataset": "experimental",
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
