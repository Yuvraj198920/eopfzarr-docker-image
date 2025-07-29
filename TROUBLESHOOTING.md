# EOPF-Zarr Driver Troubleshooting Guide for MyBinder

## MyBinder Spawn Timeout (300 seconds) - URGENT FIX

### Problem
```
Spawn failed: pod did not start in 300 seconds!
Launch attempt failed, retrying...
```

### Root Cause
The container builds successfully but the startup process takes too long, causing MyBinder to timeout.

### **IMMEDIATE SOLUTION**

#### Option 1: Use Simplified Environment (Recommended)
1. **Rename current files** to backup:
   ```bash
   mv environment.yml environment-full.yml
   mv postBuild postBuild-full
   ```

2. **Use simplified versions**:
   ```bash
   mv environment-simple.yml environment.yml
   mv postBuild-simple postBuild
   ```

3. **Commit and push** to trigger new build:
   ```bash
   git add .
   git commit -m "Fix MyBinder timeout with simplified environment"
   git push
   ```

#### Option 2: Remove Heavy Startup Processes
If you want to keep the full environment, make these changes:

1. **Simplify the `start` script**:
   ```bash
   #!/bin/bash
   export GDAL_DRIVER_PATH="/opt/eopf-zarr/drivers"
   exec "$@"
   ```

2. **Remove heavy validation from `postBuild`**:
   - Remove GDAL testing code
   - Remove driver validation
   - Keep only file copying and environment setup

### **Why This Happens**

1. **Heavy startup scripts** - Complex validation during container startup
2. **Resource intensive operations** - GDAL initialization with many drivers
3. **Network timeouts** - Git cloning during startup
4. **Build vs Runtime confusion** - Doing build tasks during startup

## Common Issues and Solutions

### 1. Driver Not Detected After MyBinder Launch

**Symptoms:**
- `gdal.GetDriverByName('EOPFZARR')` returns `None`
- Driver not found in GDAL driver list

**Solutions:**

#### Check Environment Variables
```bash
echo $GDAL_DRIVER_PATH
echo $GDAL_DATA
echo $PROJ_LIB
```

If not set, manually set them:
```bash
export GDAL_DRIVER_PATH="/opt/eopf-zarr/drivers"
export GDAL_DATA="/usr/share/gdal"
export PROJ_LIB="/usr/share/proj"
```

#### Verify Driver File Exists
```bash
ls -la /opt/eopf-zarr/drivers/
file /opt/eopf-zarr/drivers/gdal_EOPFZarr.so
```

#### Force GDAL Registration
```python
import os
os.environ['GDAL_DRIVER_PATH'] = '/opt/eopf-zarr/drivers'

from osgeo import gdal
gdal.AllRegister()
print(f"Total drivers: {gdal.GetDriverCount()}")

# Force load from directory
gdal.DontUseExceptions()
gdal.SetConfigOption('GDAL_DRIVER_PATH', '/opt/eopf-zarr/drivers')
gdal.AllRegister()
```

### 2. Build Failures in MyBinder

**Symptoms:**
- MyBinder build process fails
- CMake or compilation errors

**Solutions:**

#### Check GDAL Development Headers
The build requires GDAL development headers. If using conda environment:
```bash
conda install -c conda-forge libgdal-dev
```

#### Verify Source Repository Access
```bash
git clone https://github.com/EOPF-Sample-Service/GDAL-ZARR-EOPF.git
```

#### Check Build Dependencies
Ensure all required packages are in `environment.yml`:
- cmake
- make  
- compilers
- pkg-config
- libgdal-dev

### 3. Runtime Library Issues

**Symptoms:**
- Driver file exists but fails to load
- Shared library errors

**Solutions:**

#### Check Library Dependencies
```bash
ldd /opt/eopf-zarr/drivers/gdal_EOPFZarr.so
```

#### Verify GDAL Version Compatibility
```python
from osgeo import gdal
print(f"GDAL Version: {gdal.VersionInfo()}")
```

The driver is built against specific GDAL versions. Ensure compatibility.

### 4. Permission Issues

**Symptoms:**
- Cannot access driver directory
- Permission denied errors

**Solutions:**

#### Check File Permissions
```bash
ls -la /opt/eopf-zarr/drivers/
```

#### Set Proper Permissions (if needed)
```bash
chmod 755 /opt/eopf-zarr/drivers/gdal_EOPFZarr.so
```

### 5. Environment Not Persisting

**Symptoms:**
- Environment variables reset between sessions
- Driver works in one cell but not another

**Solutions:**

#### Use IPython Startup Script
The Dockerfile creates `~/.ipython/profile_default/startup/00-eopf-driver.py`:
```python
import os
os.environ["GDAL_DRIVER_PATH"] = "/opt/eopf-zarr/drivers"
os.environ["GDAL_DATA"] = "/usr/share/gdal"
os.environ["PROJ_LIB"] = "/usr/share/proj"

try:
    from osgeo import gdal
    gdal.AllRegister()
    print(f"GDAL initialized with {gdal.GetDriverCount()} drivers")
except Exception as e:
    print(f"Warning: GDAL initialization failed: {e}")
```

#### Set in Each Notebook Cell
Add to the top of notebooks:
```python
import os
os.environ['GDAL_DRIVER_PATH'] = '/opt/eopf-zarr/drivers'
```

### 6. Alternative Driver Detection

If the named driver isn't found, check for the driver functionality:

```python
from osgeo import gdal
gdal.AllRegister()

# List all drivers containing 'zarr' or similar
for i in range(gdal.GetDriverCount()):
    driver = gdal.GetDriver(i)
    desc = driver.GetDescription().lower()
    if 'zarr' in desc or 'eopf' in desc:
        print(f"Found: {driver.GetDescription()}")
```

### 7. MyBinder Specific Considerations

#### Container Build vs Runtime
- MyBinder may use a different build process than local Docker
- The `postBuild` script handles post-installation setup
- The `start` script initializes the runtime environment

#### Resource Limitations
- MyBinder has memory and CPU limits
- Large builds may timeout
- Consider using pre-built images for complex setups

#### Caching Issues
- MyBinder caches builds based on repository state
- Force rebuild by making a small change to `environment.yml` or `Dockerfile`
- Clear cache by pushing a new commit

### 8. Testing and Validation

#### Use the Test Script
```bash
python test-environment.py
```

#### Manual Testing
```python
# Test basic GDAL
from osgeo import gdal
print(f"GDAL: {gdal.VersionInfo()}")

# Test driver loading
import os
os.environ['GDAL_DRIVER_PATH'] = '/opt/eopf-zarr/drivers'
gdal.AllRegister()

# Test file access
import os
print(f"Driver file exists: {os.path.exists('/opt/eopf-zarr/drivers/gdal_EOPFZarr.so')}")
```

#### Debug Output
Enable verbose GDAL output:
```python
import os
os.environ['CPL_DEBUG'] = 'ON'
os.environ['GDAL_DRIVER_PATH'] = '/opt/eopf-zarr/drivers'

from osgeo import gdal
gdal.AllRegister()
```

## Quick Fixes Summary

1. **Set environment variables**: `export GDAL_DRIVER_PATH="/opt/eopf-zarr/drivers"`
2. **Force registration**: `gdal.AllRegister()` after setting env vars
3. **Check file exists**: `ls /opt/eopf-zarr/drivers/gdal_EOPFZarr.so`
4. **Verify permissions**: `chmod 755 /opt/eopf-zarr/drivers/gdal_EOPFZarr.so`
5. **Check GDAL version**: Ensure compatibility between driver and GDAL
6. **Use startup scripts**: Add environment setup to IPython startup
7. **Test systematically**: Use provided test scripts and notebooks

## Still Having Issues?

1. Check the build logs in MyBinder for compilation errors
2. Verify the source repository is accessible
3. Test with a minimal example first
4. Consider using the Docker-based approach instead of conda
5. Check for recent changes in the GDAL-ZARR-EOPF repository
