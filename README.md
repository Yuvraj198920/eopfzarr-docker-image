# EOPF-Zarr GDAL Driver Container

This container provides a complete environment for working with EOPF (European Open Science Platform Framework) Zarr-based Earth Observation data using a custom GDAL driver.

## 🚀 Quick Start with MyBinder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Yuvraj198920/eopfzarr-docker-image/HEAD)

Click the badge above to launch the environment directly in mybinder.org with the EOPF-Zarr driver pre-installed!

## Features

- **Ubuntu 25.04** base with **GDAL 3.10.x**
- **Custom EOPF-Zarr GDAL driver** for reading Zarr-based EO data
- **Complete EOPF Python environment** with geospatial libraries
- **JupyterLab** ready for interactive data analysis
- **MyBinder compatibility** for zero-setup cloud deployment
- **JupyterHub compatibility** for deployment at https://jupyterhub.user.eopf.eodc.eu

## Environment Details

### System Components
- OS: Ubuntu 25.04
- GDAL: 3.10.x (system package)
- Python: 3.13 (system Python)
- Architecture: x86_64

### Python Libraries
- **Core**: numpy, scipy, pandas, matplotlib
- **Geospatial**: gdal, xarray, zarr, dask, geopandas, rasterio, cartopy
- **Jupyter**: jupyterlab, jupyterhub, ipywidgets, notebook
- **Data formats**: netcdf4, h5py

### EOPF-Zarr Driver
- **Location**: `/opt/eopf-zarr/drivers/gdal_EOPFZarr.so`
- **Environment Variable**: `GDAL_DRIVER_PATH=/opt/eopf-zarr/drivers`
- **Functionality**: Enables GDAL to read Zarr-based Earth Observation data

## Usage

### Building the Image
```bash
docker build -f eopf-zarr-driver.dockerfile -t eopf-zarr-driver:latest .
```

### Running Locally
```bash
docker run -p 8888:8888 eopf-zarr-driver:latest
```

Access JupyterLab at: http://localhost:8888

### JupyterHub Deployment
```bash
# Tag for your registry
docker tag eopf-zarr-driver:latest your-registry/eopf-zarr-driver:latest

# Push to registry
docker push your-registry/eopf-zarr-driver:latest
```

## Testing

### MyBinder Testing
After launching the mybinder environment:

1. **Run the validation script**:
   ```bash
   python test-environment.py
   ```

2. **Open the test notebook**:
   Navigate to `examples/test_eopf_driver.ipynb` and run all cells

3. **Manual verification**:
   ```python
   import os
   os.environ['GDAL_DRIVER_PATH'] = '/opt/eopf-zarr/drivers'
   
   from osgeo import gdal
   gdal.AllRegister()
   print(f"GDAL drivers: {gdal.GetDriverCount()}")
   
   # Check for EOPF-Zarr driver
   driver = gdal.GetDriverByName('EOPFZARR')
   if driver:
       print(f"✅ EOPF-Zarr driver: {driver.GetDescription()}")
   ```

### Local Testing
The container includes a built-in test script to verify the environment:

```bash
# Inside the container
python /usr/local/bin/test-environment.py
```

Or from the Jupyter workspace:
```bash
python test-environment.py
```

This script validates:
- GDAL installation and driver count
- EOPF-Zarr driver availability (when built with source)
- Python package environment completeness

## Integration with EOPF Platform

This container is designed to work with:
- **EOPF Sample Notebooks**: https://github.com/EOPF-Sample-Service/eopf-sample-notebooks
- **JupyterHub**: https://jupyterhub.user.eopf.eodc.eu
- **EOPF Framework**: Custom Zarr-based Earth Observation data formats

## Source Code

The EOPF-Zarr driver source code is available at:
https://github.com/EOPF-Sample-Service/GDAL-ZARR-EOPF

## License

This project is licensed under the terms specified in the source repository.

## Maintainers

- EOPF Team
- Original driver development: [Your name/organization]

## Support

For issues related to:
- **Container**: Create an issue in this repository
- **EOPF-Zarr Driver**: Create an issue in the source repository
- **EOPF Platform**: Contact the EOPF team
