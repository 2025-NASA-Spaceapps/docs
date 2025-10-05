
"""
NASA & NOAA Data Downloader for 'Sharks from Space'
--------------------------------------------------
This module contains ready-to-use functions to access and download satellite data
from NASA OceanColor, PO.DAAC, GHRSST, SMAP, GEBCO, and related sources.
Each function saves the data locally in NetCDF or GeoTIFF format.
"""

import os
import requests
import xarray as xr
import rioxarray as rxr

# ---------------------------------------------------------------------
# 1. PACE (Chlorophyll, Ocean Color)
# ---------------------------------------------------------------------
def download_pace_chlorophyll(start_date, end_date, output_dir="./data/pace"):
    os.makedirs(output_dir, exist_ok=True)
    params = {
        "sensor": "PACE",
        "search": "L3m",
        "dtype": "L3m",
        "sdate": start_date,
        "edate": end_date,
        "subtype": "CHL_chlor_a",
        "results_as_file": "1"
    }
    resp = requests.get("https://oceandata.sci.gsfc.nasa.gov/api/file_search", params=params)
    file_list = resp.text.splitlines()
    for file in file_list[:3]:
        url = f"https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/{file}"
        os.system(f"wget {url} -P {output_dir}")
    print(f"[PACE] Downloaded {len(file_list[:3])} files to {output_dir}")

# ---------------------------------------------------------------------
# 2. MODIS (SST, Chlorophyll)
# ---------------------------------------------------------------------
def download_modis(sensor="modisa", start_date="2024-01-01", end_date="2024-01-07", output_dir="./data/modis"):
    os.makedirs(output_dir, exist_ok=True)
    params = {
        "sensor": sensor,  # 'modisa' for Aqua, 'modist' for Terra
        "search": "L3m",
        "subtype": "CHL_chlor_a",
        "sdate": start_date,
        "edate": end_date,
        "results_as_file": "1"
    }
    resp = requests.get("https://oceandata.sci.gsfc.nasa.gov/api/file_search", params=params)
    file_list = resp.text.splitlines()
    for file in file_list[:3]:
        url = f"https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/{file}"
        os.system(f"wget {url} -P {output_dir}")
    print(f"[MODIS] Downloaded {len(file_list[:3])} files to {output_dir}")

# ---------------------------------------------------------------------
# 3. SWOT (Sea Surface Height)
# ---------------------------------------------------------------------
def get_swot_granule(start_time, end_time, bbox="-80,-40,-10,40"):
    headers = {"Accept": "application/json"}
    params = {
        "short_name": "SWOT_L2_LR_SSH_2",
        "temporal": f"{start_time},{end_time}",
        "bounding_box": bbox,
    }
    resp = requests.get("https://cmr.earthdata.nasa.gov/search/granules.json", params=params, headers=headers)
    data = resp.json()
    if "feed" in data and data["feed"]["entry"]:
        granule_url = data["feed"]["entry"][0]["links"][0]["href"]
        print("[SWOT] Example granule URL:", granule_url)
        return granule_url
    else:
        print("[SWOT] No granule found.")
        return None

# ---------------------------------------------------------------------
# 4. GHRSST (SST)
# ---------------------------------------------------------------------
def download_ghrsst_example(url, output_tif="GHRSST_SST_example.tif"):
    ds = xr.open_dataset(url)
    sst = ds["analysed_sst"].sel(lat=slice(-40, 40), lon=slice(-80, -10))
    sst.rio.to_raster(output_tif)
    print(f"[GHRSST] SST raster saved to {output_tif}")

# ---------------------------------------------------------------------
# 5. SMAP (Salinity)
# ---------------------------------------------------------------------
def download_smap_salinity(url, output_tif="SMAP_SSS_example.tif"):
    ds = xr.open_dataset(url)
    sss = ds["sss_smap"].sel(lat=slice(-30, 30), lon=slice(-80, -10))
    sss.mean(dim="time").rio.to_raster(output_tif)
    print(f"[SMAP] Salinity raster saved to {output_tif}")

# ---------------------------------------------------------------------
# 6. GEBCO (Bathymetry)
# ---------------------------------------------------------------------
def subset_gebco_bathymetry(nc_file="GEBCO_2024.nc", output_tif="GEBCO_Bathymetry.tif"):
    ds = xr.open_dataset(nc_file)
    subset = ds.sel(lat=slice(-40, 40), lon=slice(-80, -10))
    subset["elevation"].rio.to_raster(output_tif)
    print(f"[GEBCO] Bathymetry subset saved to {output_tif}")

# ---------------------------------------------------------------------
# 7. Merge Layers into Unified Dataset
# ---------------------------------------------------------------------
def merge_layers(chl_path, sst_path, ssh_path, output_nc="OceanBase_Core.nc"):
    chl = rxr.open_rasterio(chl_path)
    sst = rxr.open_rasterio(sst_path)
    ssh = rxr.open_rasterio(ssh_path)
    sst_resampled = sst.rio.reproject_match(chl)
    merged = xr.merge([chl, sst_resampled, ssh])
    merged.to_netcdf(output_nc)
    print(f"[MERGE] Combined dataset saved to {output_nc}")
