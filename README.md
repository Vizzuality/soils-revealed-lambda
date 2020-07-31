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
POST http://${API_URL}/api/v1/analysis?dataset_type=experimental-dataset&group=stocks
```

POST body (as JSON):

```json
{
  "dataset_type": "experimental-dataset",
  "group": "stocks",
  "years": [
    "1982",
    "2017"
  ],
  "depth": "0-30",
  "variable": "stocks",
  "nBinds": 80,
  "bindsRange": [
    -50,
    50
  ],
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
                -63.34716796874999,
                -34.234512362369856
              ],
              [
                -64.22607421875,
                -35.17380831799957
              ],
              [
                -63.896484375,
                -35.78217070326606
              ],
              [
                -63.34716796874999,
                -35.88905007936092
              ],
              [
                -62.86376953124999,
                -35.46066995149529
              ],
              [
                -62.51220703125,
                -35.08395557927643
              ],
              [
                -62.49023437499999,
                -34.57895241036947
              ],
              [
                -63.34716796874999,
                -34.234512362369856
              ]
            ]
          ]
        }
      }
    ]
  }
}
```
