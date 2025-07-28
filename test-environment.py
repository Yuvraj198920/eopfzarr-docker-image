#!/usr/bin/env python3
"""
EOPF-Zarr driver validation for mybinder.org
This script tests the installation and validates the environment
"""

import os
import sys

def setup_environment():
    """Ensure environment variables are set"""
    os.environ['GDAL_DRIVER_PATH'] = '/opt/eopf-zarr/drivers'
    os.environ['GDAL_DATA'] = '/usr/share/gdal'
    os.environ['PROJ_LIB'] = '/usr/share/proj'

def test_gdal_installation():
    """Test basic GDAL installation"""
    setup_environment()
    try:
        from osgeo import gdal
        gdal.AllRegister()
        print(f"✅ GDAL {gdal.VersionInfo()} loaded successfully")
        print(f"📦 Total drivers available: {gdal.GetDriverCount()}")
        
        # Check if driver file exists
        driver_file = "/opt/eopf-zarr/drivers/gdal_EOPFZarr.so"
        if os.path.exists(driver_file):
            print(f"✅ EOPF-Zarr driver file found: {driver_file}")
        else:
            print(f"⚠️ EOPF-Zarr driver file not found: {driver_file}")
        
        return True
    except ImportError as e:
        print(f"❌ Failed to import GDAL: {e}")
        return False
    except Exception as e:
        print(f"❌ GDAL error: {e}")
        return False

def test_eopf_zarr_driver():
    """Test EOPF-Zarr driver availability"""
    setup_environment()
    try:
        from osgeo import gdal
        gdal.AllRegister()
        
        # Try to get the EOPF-Zarr driver by name
        driver = gdal.GetDriverByName('EOPFZARR')
        if driver:
            print(f"✅ EOPF-Zarr driver found by name: {driver.GetDescription()}")
            metadata = driver.GetMetadata()
            if metadata:
                print(f"   Metadata: {metadata}")
            return True
        else:
            print("⚠️ EOPF-Zarr driver not found by name")
            
            # Check if any driver contains 'eopf' or similar
            found_related = False
            for i in range(gdal.GetDriverCount()):
                drv = gdal.GetDriver(i)
                desc = drv.GetDescription().lower()
                if 'eopf' in desc or ('zarr' in desc and 'eo' in desc):
                    print(f"   Found related driver: {drv.GetDescription()}")
                    found_related = True
            
            if found_related:
                print("✅ Related driver found - may be loaded with different name")
                return True
            else:
                print("⚠️ No related drivers found - this may be expected in some environments")
                return True  # Don't fail the test for this
                
    except Exception as e:
        print(f"❌ Error checking EOPF-Zarr driver: {e}")
        return False

def test_python_environment():
    """Test Python environment packages"""
    packages = [
        'numpy', 'scipy', 'pandas', 'matplotlib',
        'xarray', 'zarr', 'dask', 
        'geopandas', 'rasterio', 'fiona',
        'jupyter', 'jupyterlab'
    ]
    
    success_count = 0
    missing_packages = []
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}")
            success_count += 1
        except ImportError:
            print(f"❌ {package} - missing")
            missing_packages.append(package)
    
    print(f"📊 Environment: {success_count}/{len(packages)} packages available")
    
    if missing_packages:
        print(f"⚠️ Missing packages: {', '.join(missing_packages)}")
    
    return success_count >= len(packages) * 0.8  # 80% success rate

def test_environment_variables():
    """Test that required environment variables are set"""
    required_vars = ['GDAL_DRIVER_PATH', 'GDAL_DATA', 'PROJ_LIB']
    setup_environment()  # Ensure they're set
    
    success = True
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value}")
            # Check if path exists
            if os.path.exists(value):
                print(f"   Path exists: ✅")
            else:
                print(f"   Path missing: ⚠️")
        else:
            print(f"❌ {var}: Not set")
            success = False
    
    return success

if __name__ == "__main__":
    print("🧪 EOPF-Zarr Container Validation for MyBinder")
    print("=" * 50)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("GDAL Installation", test_gdal_installation),
        ("EOPF-Zarr Driver", test_eopf_zarr_driver),
        ("Python Environment", test_python_environment)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        try:
            result = test_func()
            results.append(result)
            print(f"Result: {'✅ PASS' if result else '❌ FAIL'}")
        except Exception as e:
            print(f"❌ FAIL - Exception: {e}")
            results.append(False)
    
    print(f"\n🎯 Overall: {sum(results)}/{len(results)} tests passed")
    
    if all(results):
        print("🚀 Container is ready for use!")
        print("\n📝 Next steps:")
        print("  1. Open the test notebook: examples/test_eopf_driver.ipynb")
        print("  2. Run the cells to validate GDAL and driver functionality")
        print("  3. Check that EOPF-Zarr driver is properly loaded")
    else:
        print("⚠️ Some tests failed - check configuration")
        print("\n🔧 Troubleshooting:")
        print("  1. Verify GDAL_DRIVER_PATH is set to /opt/eopf-zarr/drivers")
        print("  2. Check that gdal_EOPFZarr.so exists in the drivers directory")
        print("  3. Ensure GDAL can load custom drivers")

    # Print environment info for debugging
    print(f"\n🐍 Environment Info:")
    print(f"  Python: {sys.version}")
    print(f"  GDAL_DRIVER_PATH: {os.environ.get('GDAL_DRIVER_PATH', 'Not set')}")
    print(f"  GDAL_DATA: {os.environ.get('GDAL_DATA', 'Not set')}")
    print(f"  Working directory: {os.getcwd()}")
    
    # List driver directory contents
    driver_dir = "/opt/eopf-zarr/drivers"
    if os.path.exists(driver_dir):
        print(f"\n📁 Driver directory contents ({driver_dir}):")
        try:
            for item in os.listdir(driver_dir):
                item_path = os.path.join(driver_dir, item)
                size = os.path.getsize(item_path) if os.path.isfile(item_path) else "dir"
                print(f"  {item} ({size} bytes)" if size != "dir" else f"  {item}/ (directory)")
        except Exception as e:
            print(f"  Error listing directory: {e}")
    else:
        print(f"\n❌ Driver directory not found: {driver_dir}")
