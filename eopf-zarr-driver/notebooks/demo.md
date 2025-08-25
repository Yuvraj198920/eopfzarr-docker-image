# EOPF-Zarr Driver Demo

Welcome to the EOPF-Zarr driver demonstration!

## Getting Started

This notebook demonstrates how to use the EOPF-Zarr GDAL driver to access remote Zarr datasets.

### Example Usage

```python
import os
import rasterio
from osgeo import gdal

# IMPORTANT: Set GDAL driver path for BinderHub compatibility
os.environ['GDAL_DRIVER_PATH'] = '/opt/eopf-zarr/drivers'

# Register all GDAL drivers including EOPF-Zarr
gdal.AllRegister()

# Verify EOPF-Zarr driver is available
driver = gdal.GetDriverByName('EOPFZARR')
if driver:
    print(f"✓ EOPF-Zarr driver found: {driver.GetDescription()}")
else:
    print("✗ EOPF-Zarr driver not found")
    print("Available drivers:", [gdal.GetDriver(i).GetDescription() for i in range(min(10, gdal.GetDriverCount()))])

# Example remote Zarr URL
url = "EOPFZARR:'/vsicurl/https://storage.sbg.cloud.ovh.net/v1/AUTH_8471d76cdd494d98a078f28b195dace4/sentinel-1-public/demo_product/grd/S01SIWGRH_20240201T164915_0025_A146_S000_5464A_VH.zarr'"

# Open with rasterio
try:
    with rasterio.open(url) as src:
        print(f"Dataset shape: {src.shape}")
        print(f"Dataset CRS: {src.crs}")
        print(f"Dataset bounds: {src.bounds}")
except Exception as e:
    print(f"Error opening dataset: {e}")
```

### Testing EOPF-Zarr Functionality

Run the built-in test suite:

```python
exec(open('/usr/local/bin/test-environment.py').read())
```
