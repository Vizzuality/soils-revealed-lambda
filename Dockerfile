FROM python:3.7.5-slim-buster

RUN apt-get update \
      && apt-get install -y --no-install-recommends \
            postgresql-client \
            gdal-bin libgdal-dev && export CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt && rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY entrypoint.sh entrypoint.sh
COPY ./src src

COPY ./gunicorn.py gunicorn.py

EXPOSE 5020
ENTRYPOINT ["./entrypoint.sh"]