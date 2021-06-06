FROM python:3.8.10-slim-buster@sha256:0ffccea3f91806abb0a76eced3da5db52f77fd52aa926a3abd1a6bd275ec334c
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update \
      && apt-get install -y --no-install-recommends \
         postgresql-client \
         build-essential \
         gdal-bin libgdal-dev libtbb2 tini 
WORKDIR /src
RUN mkdir -p /soils

COPY soils /soils/soils
COPY requirements.txt /soils/requirements.txt
COPY gunicorn.py /soils/gunicorn.py


WORKDIR /soils
RUN pip install -r requirements.txt

# Clean up
RUN pip cache purge \ 
    && apt remove -y build-essential \ 
    && apt -y autoremove \ 
    && rm -rf /var/lib/apt/lists/*

USER www-data
EXPOSE 8000

ENTRYPOINT ["/usr/bin/tini","-g","--"]
CMD ["gunicorn","--config=./gunicorn.py", "soils:app"]
