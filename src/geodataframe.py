#%%
from imports import * 
#%%
## CONVERT SHAPEFILES TO GEOJSON AND SAVE THEM LOCALLY
# sc = "/Users/Matteo/Xylella-Diffusion/src/data/"
uliveti = fiona.open("/Users/Matteo/Xylella-Diffusion/data/uliveti_puglia.shp")
uliveti_gdf = gpd.GeoDataFrame(
    uliveti,
    crs='EPSG:32633',
    )
uliveti_gdf = uliveti_gdf.drop(columns=['properties'])
uliveti_gdf.to_file("uliveti.geojson") 
url = 'https://github.com/napo/geospatial_course_unitn/raw/master/data/istat/istat_administrative_units_2022.gpkg'
regions = gpd.read_file(url,layer="regions")
puglia = regions[regions['DEN_REG'] == "Puglia"]
municipalities = gpd.read_file(url,layer="municipalities")
puglia_mun = municipalities[municipalities['COD_REG'] == 16]
puglia_mun.to_file("puglia_mun.geojson")
provinces = gpd.read_file(url,layer="provincies")
puglia_prov = provinces[provinces['COD_REG'] == 16]
puglia_prov.to_file("puglia_prov.geojson")
puglia.to_file("puglia.geojson")
#%%