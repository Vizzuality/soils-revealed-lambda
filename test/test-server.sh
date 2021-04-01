#!/bin/bash
# Testing gunicorn instance running on localhost:8000
# docker build -t soils-analysis .
# docker run -p8000:8000 soil-analysis start

<<<<<<< HEAD
curl -v -w "@curl-format.txt" -H "Content-Type: application/json" -d @data2.json http://localhost:8000/api/v1/analysis
=======
curl -v -w "@curl-format.txt" -H "Content-Type: application/json" -d @data.json http://localhost:8000/api/v1/analysis
>>>>>>> fc207bf... Missing libtbb.so.2
