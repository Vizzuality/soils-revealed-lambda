FROM python:3.8.1-slim-buster
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH
RUN apt-get update \
      && apt-get install -y --no-install-recommends \
            postgresql-client \
            gdal-bin libgdal-dev libtbb2 tini && export CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt && rm -rf /var/lib/apt/lists/*
RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 git mercurial subversion && \
    apt-get clean
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy
RUN conda update -n base conda
WORKDIR /src
RUN mkdir -p /soils

COPY soils /soils/soils
COPY requirements.txt /soils/requirements.txt
COPY entrypoint.sh /soils/entrypoint.sh
COPY gunicorn.py /soils/gunicorn.py
COPY gunicorn_dev.py /soils/gunicorn_dev.py

WORKDIR /soils

RUN conda install --force-reinstall -y -q -c conda-forge --file requirements.txt

USER www-data
EXPOSE 8000

ENTRYPOINT ["/usr/bin/tini","-g","--"]
CMD ["gunicorn","--config=./gunicorn.py", "soils:app"]
