# Use the local eopf-zarr-driver as base
# Replace this with your actual registry URL when published
# e.g., FROM ghcr.io/your-username/eopf-zarr-driver:latest
FROM eopf-zarr-driver:latest

# Ensure GDAL driver path is set for BinderHub
ENV GDAL_DRIVER_PATH=/opt/eopf-zarr/drivers

# Set environment for jovyan user (BinderHub default user)
USER root
RUN echo 'export GDAL_DRIVER_PATH=/opt/eopf-zarr/drivers' >> /home/jovyan/.bashrc && \
    echo 'export GDAL_DRIVER_PATH=/opt/eopf-zarr/drivers' >> /home/jovyan/.profile

USER ${NB_UID}
