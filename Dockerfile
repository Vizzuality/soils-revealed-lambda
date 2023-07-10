FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV DEBIAN_FRONTEND noninteractive

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client \
    build-essential \
    gdal-bin libgdal-dev proj-bin tini 
WORKDIR /src
RUN mkdir -p /soils

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./requirements.txt /soils/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /soils/requirements.txt

COPY gunicorn.py /soils/gunicorn.py
COPY gunicorn_dev.py /soils/gunicorn_dev.py
COPY soils /soils/soils

WORKDIR /soils

USER www-data
EXPOSE 8000

ENTRYPOINT ["/usr/bin/tini","-g","--"]
CMD ["gunicorn","--config=./gunicorn.py", "soils.main:app"]
