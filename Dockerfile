FROM continuumio/miniconda3:4.8.2

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --fix-missing \
      && apt-get install -y --no-install-recommends \
            gdal-bin libgdal-dev \
            libglib2.0-0 libxext6 libsm6 libxrender1

RUN mkdir -p /soils

COPY soils /soils/soils
COPY requirements.txt /soils/requirements.txt
COPY entrypoint.sh /soils/entrypoint.sh
COPY gunicorn.py /soils/gunicorn.py
COPY dev_server.py /soils/dev_server.py

WORKDIR /soils

RUN conda install --force-reinstall -y -q -c conda-forge --file requirements.txt

ENTRYPOINT ["/soils/entrypoint.sh"]