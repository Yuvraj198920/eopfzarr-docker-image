ARG BASE_CONTAINER=ghcr.io/dask/dask-notebook:2025.5.0-py3.11
FROM $BASE_CONTAINER

USER root
RUN apt-get update && \
    apt-get install -y \
    s3fs \
    s3cmd \
    openssh-client && \
    apt-get clean -y

USER ${NB_UID}

COPY environment.yml /tmp/environment.yml

RUN mamba env update -n base --file /tmp/environment.yml \
    && mamba clean --all --yes \
    && find /opt/conda/ -type f,l -name '*.a' -delete \
    && find /opt/conda/ -type f,l -name '*.pyc' -delete \
    && find /opt/conda/ -type f,l -name '*.js.map' -delete \
    && find /opt/conda/lib/python*/site-packages/bokeh/server/static -type f,l -name '*.js' -not -name '*.min.js' -delete \
    && rm -rf /opt/conda/pkgs \
    && cd /home/jovyan \
    && git clone git@github.com:EOPF-Sample-Service/eopf-sample-notebooks.git

RUN rm -rf /home/jovyan/examples
