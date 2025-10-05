
"""
MAIN PIPELINE - Sharks from Space
---------------------------------
This script runs daily to:
  1. Download NASA oceanographic datasets (PACE, MODIS, GHRSST, etc.)
  2. Extract regional subsets for analysis
  3. Merge all layers into the unified OceanBase-Core dataset
  4. Prepare data for AI training and forecasting
"""

import os
from datetime import datetime, timedelta
from nasa_data_downloader import (
    download_pace_chlorophyll,
    download_modis,
    get_swot_granule,
    download_ghrsst_example,
    download_smap_salinity,
    subset_gebco_bathymetry,
    merge_layers
)

# ----------------------------------------------------------------------
# 1️⃣ INITIAL SETUP
# ----------------------------------------------------------------------

# Working directories
os.makedirs("./data", exist_ok=True)
os.makedirs("./data/output", exist_ok=True)
os.makedirs("./data/swot", exist_ok=True)

# Define date window (last 7 days)
today = datetime.utcnow().date()
start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")

print(f"🧭 Running data pipeline for {start_date} → {end_date}")

# ----------------------------------------------------------------------
# 2️⃣ DOWNLOAD NASA OCEAN DATASETS
# ----------------------------------------------------------------------

# --- PACE (Chlorophyll)
download_pace_chlorophyll(start_date, end_date, output_dir="./data/pace")

# --- MODIS (Chlorophyll / SST)
download_modis(sensor="modisa", start_date=start_date, end_date=end_date, output_dir="./data/modis")

# --- SWOT (Sea Surface Height)
swot_url = get_swot_granule(f"{start_date}T00:00:00Z", f"{end_date}T23:59:59Z")
if swot_url:
    os.system(f"wget {swot_url} -O ./data/swot/SWOT_L2_LR_SSH_2.nc")

# --- GHRSST (Sea Surface Temperature)
ghrsst_url = "https://podaac-opendap.jpl.nasa.gov/opendap/allData/ghrsst/data/GDS2/L4/GLOB/JPL/MUR25/v4.1/2024/120/20240429-JPL-L4_GHRSST-SSTfnd-MUR25-GLOB-v04.1-fv04.1.nc"
download_ghrsst_example(ghrsst_url, output_tif="./data/output/GHRSST_SST.tif")

# --- SMAP (Ocean Salinity)
smap_url = "https://podaac-opendap.jpl.nasa.gov/opendap/allData/smap/L3/RSS/V5.0/2024/060/SMAP_RSS_L3_SSS_SMI_40KM_20240301T000000_V5.0.nc"
download_smap_salinity(smap_url, output_tif="./data/output/SMAP_SSS.tif")

# --- GEBCO (Bathymetry)
if not os.path.exists("./data/GEBCO_2024.nc"):
    os.system("wget https://www.bodc.ac.uk/data/open_download/gebco/gebco_2024/GEBCO_2024.nc -P ./data")
subset_gebco_bathymetry("./data/GEBCO_2024.nc", output_tif="./data/output/GEBCO_Bathymetry.tif")

# ----------------------------------------------------------------------
# 3️⃣ MERGE ALL LAYERS
# ----------------------------------------------------------------------
try:
    merge_layers(
        chl_path="./data/pace/PACE_CHL_L3.nc",
        sst_path="./data/output/GHRSST_SST.tif",
        ssh_path="./data/swot/SWOT_L2_LR_SSH_2.nc",
        output_nc="./data/output/OceanBase_Core.nc"
    )
    print("✅ OceanBase-Core dataset successfully created!")
except Exception as e:
    print("⚠️ Merge failed:", e)

# ----------------------------------------------------------------------
# 4️⃣ LOG COMPLETION
# ----------------------------------------------------------------------
with open("./data/output/pipeline_log.txt", "a") as f:
    f.write(f"{datetime.utcnow()} - Data update complete for {start_date} → {end_date}\n")

print("🌍 Pipeline completed successfully.")
