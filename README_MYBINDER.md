# MyBinder Configuration for EOPF-Zarr Driver

This repository is configured for deployment on [mybinder.org](https://mybinder.org) with the EOPF-Zarr GDAL driver.

## Quick Start

Click this button to launch the environment in mybinder:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Yuvraj198920/eopfzarr-docker-image/HEAD)

## What's Included

- **EOPF-Zarr GDAL Driver**: Custom driver for reading Zarr-based Earth Observation data
- **Complete Python Environment**: All necessary geospatial libraries (GDAL, xarray, zarr, dask, etc.)
- **JupyterLab**: Interactive environment for data analysis
- **Test Notebook**: Pre-configured notebook to validate the driver installation

## Files for MyBinder

- `environment.yml` - Conda environment specification
- `Dockerfile` - Custom Docker image with EOPF-Zarr driver
- `postBuild` - Post-build script to configure the environment
- `start` - Startup script to initialize the driver
- `test-environment.py` - Validation script

## Testing the Installation

After launching mybinder, you can test the installation in several ways:

### 1. Run the Test Script
Open a terminal and run:
```bash
python test-environment.py
```

### 2. Open the Test Notebook
Navigate to `examples/test_eopf_driver.ipynb` and run the cells to validate the installation.

### 3. Manual Testing
In a Python cell or terminal:
```python
import os
os.environ['GDAL_DRIVER_PATH'] = '/opt/eopf-zarr/drivers'

from osgeo import gdal
gdal.AllRegister()
print(f"GDAL drivers available: {gdal.GetDriverCount()}")

# Check for EOPF-Zarr driver
driver = gdal.GetDriverByName('EOPFZARR')
if driver:
    print(f"EOPF-Zarr driver found: {driver.GetDescription()}")
else:
    print("EOPF-Zarr driver not found by name")
```

## Troubleshooting

### Driver Not Found
If the EOPF-Zarr driver is not detected:

1. **Check Environment Variables**:
   ```bash
   echo $GDAL_DRIVER_PATH
   echo $GDAL_DATA
   ```

2. **Verify Driver File**:
   ```bash
   ls -la /opt/eopf-zarr/drivers/
   ```

3. **Check GDAL Registration**:
   ```python
   import os
   os.environ['GDAL_DRIVER_PATH'] = '/opt/eopf-zarr/drivers'
   from osgeo import gdal
   gdal.AllRegister()
   ```

### Build Issues
If the mybinder build fails:

1. Check the build logs for compilation errors
2. Verify the GDAL-ZARR-EOPF repository is accessible
3. Ensure all dependencies are available in conda-forge

### Driver Loading Issues
If the driver compiles but doesn't load:

1. Check library dependencies with `ldd`
2. Verify GDAL version compatibility
3. Check file permissions on the driver file

## Source Code

The EOPF-Zarr driver source code is available at:
https://github.com/EOPF-Sample-Service/GDAL-ZARR-EOPF

## Expected Behavior

In a successful deployment:

- The environment should build without errors
- The driver file `gdal_EOPFZarr.so` should exist in `/opt/eopf-zarr/drivers/`
- GDAL should load with 100+ drivers available
- The test script should pass all or most tests
- The EOPF-Zarr driver should be detectable (either by name or as a related driver)

## Deployment Options

### Standard MyBinder
Uses the `environment.yml` file for a conda-based build.

### Docker-based MyBinder  
Uses the `Dockerfile` for a custom container build (recommended for this driver).

### Hybrid Approach
Uses `environment.yml` for package installation and `postBuild` for driver compilation.

## Support

For issues with:
- **MyBinder deployment**: Check the build logs and this README
- **EOPF-Zarr driver**: Create an issue in the source repository
- **GDAL integration**: Verify GDAL version compatibility

## Environment Details

- **Base**: jupyter/base-notebook or Ubuntu 22.04
- **Python**: 3.9+
- **GDAL**: 3.4-3.7 (compatible versions)
- **Key Libraries**: xarray, zarr<3, dask, rasterio, geopandas
- **Build Tools**: cmake, make, compilers, pkg-config
