# EOPF-Zarr GDAL Driver - Simplified Docker Image
# Based on Jupyter minimal-notebook for JupyterHub compatibility
ARG REGISTRY=quay.io
ARG OWNER=jupyter
ARG BASE_IMAGE=$REGISTRY/$OWNER/minimal-notebook
FROM $BASE_IMAGE

LABEL maintainer="EOPF Sample Service"
LABEL description="EOPF-Zarr GDAL Driver with Jupyter base, GDAL, and EOPF Python environment"
LABEL version="3.0.0"

USER root

# Install GDAL and system dependencies
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    git \
    cmake \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL driver path
ENV GDAL_DRIVER_PATH=/opt/eopf-zarr/drivers

# Create driver directory and build EOPF-Zarr driver
RUN mkdir -p /opt/eopf-zarr/drivers && \
    git clone --depth 1 https://github.com/EOPF-Sample-Service/GDAL-ZARR-EOPF.git /tmp/eopf-zarr && \
    cd /tmp/eopf-zarr && \
    mkdir build && cd build && \
    cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
        -DGDAL_ROOT=/usr && \
    make -j$(nproc) && \
    cp gdal_EOPFZarr.so /opt/eopf-zarr/drivers/ && \
    rm -rf /tmp/eopf-zarr

# Set driver path in multiple locations for BinderHub compatibility
RUN echo 'export GDAL_DRIVER_PATH=/opt/eopf-zarr/drivers' >> /etc/environment && \
    echo 'export GDAL_DRIVER_PATH=/opt/eopf-zarr/drivers' >> /etc/bash.bashrc && \
    echo 'export GDAL_DRIVER_PATH=/opt/eopf-zarr/drivers' >> /etc/profile

USER $NB_UID

# Set environment variables for the jovyan user
RUN echo 'export GDAL_DRIVER_PATH=/opt/eopf-zarr/drivers' >> /home/jovyan/.bashrc && \
    echo 'export GDAL_DRIVER_PATH=/opt/eopf-zarr/drivers' >> /home/jovyan/.profile

# Create a startup script to ensure GDAL driver is properly loaded
RUN mkdir -p /home/jovyan/.jupyter && \
    echo 'import os' > /home/jovyan/.jupyter/jupyter_notebook_config.py && \
    echo 'os.environ["GDAL_DRIVER_PATH"] = "/opt/eopf-zarr/drivers"' >> /home/jovyan/.jupyter/jupyter_notebook_config.py && \
    echo 'c.NotebookApp.tornado_settings = {"headers": {"Content-Security-Policy": "frame-ancestors \'self\' *"}}' >> /home/jovyan/.jupyter/jupyter_notebook_config.py

# Create a test script to verify driver installation
RUN echo '#!/usr/bin/env python3' > /usr/local/bin/test-eopf-driver.py && \
    echo 'import os' >> /usr/local/bin/test-eopf-driver.py && \
    echo 'import sys' >> /usr/local/bin/test-eopf-driver.py && \
    echo 'os.environ["GDAL_DRIVER_PATH"] = "/opt/eopf-zarr/drivers"' >> /usr/local/bin/test-eopf-driver.py && \
    echo 'try:' >> /usr/local/bin/test-eopf-driver.py && \
    echo '    from osgeo import gdal' >> /usr/local/bin/test-eopf-driver.py && \
    echo '    gdal.AllRegister()' >> /usr/local/bin/test-eopf-driver.py && \
    echo '    driver = gdal.GetDriverByName("EOPFZARR")' >> /usr/local/bin/test-eopf-driver.py && \
    echo '    if driver:' >> /usr/local/bin/test-eopf-driver.py && \
    echo '        print(f"✓ EOPF-Zarr driver found: {driver.GetDescription()}")' >> /usr/local/bin/test-eopf-driver.py && \
    echo '        print(f"✓ Driver path: {os.environ.get(\\"GDAL_DRIVER_PATH\\", \\"Not set\\")}")' >> /usr/local/bin/test-eopf-driver.py && \
    echo '    else:' >> /usr/local/bin/test-eopf-driver.py && \
    echo '        print("✗ EOPF-Zarr driver not found")' >> /usr/local/bin/test-eopf-driver.py && \
    echo '        print(f"Available drivers: {[gdal.GetDriver(i).GetDescription() for i in range(gdal.GetDriverCount())]}")' >> /usr/local/bin/test-eopf-driver.py && \
    echo 'except Exception as e:' >> /usr/local/bin/test-eopf-driver.py && \
    echo '    print(f"Error testing GDAL: {e}")' >> /usr/local/bin/test-eopf-driver.py && \
    chmod +x /usr/local/bin/test-eopf-driver.py

# Install Python packages with GDAL driver path set
RUN export GDAL_DRIVER_PATH=/opt/eopf-zarr/drivers && \
    pip install --no-cache-dir \
    GDAL==$(gdal-config --version) \
    --no-binary=rasterio rasterio \
    xarray \
    zarr \
    dask \
    geopandas \
    fiona \
    shapely \
    matplotlib \
    netcdf4 \
    h5py
