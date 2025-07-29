# EOPF-Zarr GDAL Driver for MyBinder
# 
# This Dockerfile is specifically designed for mybinder.org deployment
# It builds the EOPF-Zarr GDAL driver and ensures proper driver registration

FROM jupyter/base-notebook:ubuntu-22.04

# Switch to root for system installations
USER root

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV GDAL_DRIVER_PATH="/opt/eopf-zarr/drivers"
ENV GDAL_DATA="/usr/share/gdal"
ENV PROJ_LIB="/usr/share/proj"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Build tools
    build-essential \
    cmake \
    git \
    pkg-config \
    # GDAL and geospatial libraries
    gdal-bin \
    libgdal-dev \
    gdal-data \
    proj-bin \
    proj-data \
    libproj-dev \
    # Python development
    python3-dev \
    # Additional utilities
    curl \
    wget \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create directory structure for EOPF-Zarr driver
RUN mkdir -p /opt/eopf-zarr/drivers /opt/eopf-zarr/build

# Clone and build EOPF-Zarr driver
WORKDIR /opt/eopf-zarr
RUN git clone https://github.com/EOPF-Sample-Service/GDAL-ZARR-EOPF.git source \
    && cd source \
    && git checkout main

# Build the EOPF-Zarr GDAL driver
WORKDIR /opt/eopf-zarr/build
RUN cmake ../source \
    && make -j$(nproc) \
    && cp gdal_EOPFZarr.so /opt/eopf-zarr/drivers/gdal_EOPFZarr.so \
    && chmod 755 /opt/eopf-zarr/drivers/gdal_EOPFZarr.so

# Set proper permissions for the driver directory
RUN chown -R $NB_UID:$NB_GID /opt/eopf-zarr \
    && chmod -R 755 /opt/eopf-zarr

# Install Python packages using mamba (faster than conda)
RUN mamba install -y -c conda-forge \
    # Core scientific computing
    numpy \
    scipy \
    pandas \
    matplotlib \
    # Geospatial stack
    gdal>=3.4 \
    xarray \
    "zarr<3" \
    dask \
    geopandas \
    rasterio \
    fiona \
    shapely \
    pyproj \
    cartopy \
    # Data formats
    netcdf4 \
    h5py \
    # Jupyter ecosystem
    jupyterlab \
    ipywidgets \
    ipykernel \
    && mamba clean -a -y

# Create a script to properly initialize the EOPF-Zarr driver
RUN echo '#!/bin/bash' > /usr/local/bin/init-eopf-driver.sh \
    && echo 'export GDAL_DRIVER_PATH="/opt/eopf-zarr/drivers"' >> /usr/local/bin/init-eopf-driver.sh \
    && echo 'export GDAL_DATA="/usr/share/gdal"' >> /usr/local/bin/init-eopf-driver.sh \
    && echo 'export PROJ_LIB="/usr/share/proj"' >> /usr/local/bin/init-eopf-driver.sh \
    && echo 'python3 -c "from osgeo import gdal; gdal.AllRegister(); print(f\"GDAL drivers: {gdal.GetDriverCount()}\")"' >> /usr/local/bin/init-eopf-driver.sh \
    && chmod +x /usr/local/bin/init-eopf-driver.sh

# Copy test environment script
COPY test-environment.py /usr/local/bin/test-environment.py
RUN chmod +x /usr/local/bin/test-environment.py

# Create environment activation script
RUN echo 'export GDAL_DRIVER_PATH="/opt/eopf-zarr/drivers"' >> /etc/environment \
    && echo 'export GDAL_DATA="/usr/share/gdal"' >> /etc/environment \
    && echo 'export PROJ_LIB="/usr/share/proj"' >> /etc/environment

# Switch back to notebook user
USER $NB_UID

# Set up the conda environment with GDAL driver path
RUN echo 'export GDAL_DRIVER_PATH="/opt/eopf-zarr/drivers"' >> ~/.bashrc \
    && echo 'export GDAL_DATA="/usr/share/gdal"' >> ~/.bashrc \
    && echo 'export PROJ_LIB="/usr/share/proj"' >> ~/.bashrc

# Create a startup script for Jupyter
RUN mkdir -p ~/.ipython/profile_default/startup/ \
    && echo 'import os' > ~/.ipython/profile_default/startup/00-eopf-driver.py \
    && echo 'os.environ["GDAL_DRIVER_PATH"] = "/opt/eopf-zarr/drivers"' >> ~/.ipython/profile_default/startup/00-eopf-driver.py \
    && echo 'os.environ["GDAL_DATA"] = "/usr/share/gdal"' >> ~/.ipython/profile_default/startup/00-eopf-driver.py \
    && echo 'os.environ["PROJ_LIB"] = "/usr/share/proj"' >> ~/.ipython/profile_default/startup/00-eopf-driver.py \
    && echo 'try:' >> ~/.ipython/profile_default/startup/00-eopf-driver.py \
    && echo '    from osgeo import gdal' >> ~/.ipython/profile_default/startup/00-eopf-driver.py \
    && echo '    gdal.AllRegister()' >> ~/.ipython/profile_default/startup/00-eopf-driver.py \
    && echo '    print(f"GDAL initialized with {gdal.GetDriverCount()} drivers")' >> ~/.ipython/profile_default/startup/00-eopf-driver.py \
    && echo 'except Exception as e:' >> ~/.ipython/profile_default/startup/00-eopf-driver.py \
    && echo '    print(f"Warning: GDAL initialization failed: {e}")' >> ~/.ipython/profile_default/startup/00-eopf-driver.py

# Set working directory
WORKDIR /home/$NB_USER
