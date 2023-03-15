#%%
from imports import *
#%%
#extract polygon
sc = "/Users/Matteo/Xylella-Diffusion/src/data/"
uliveti = fiona.open("/Users/Matteo/Xylella-Diffusion/data/uliveti_puglia.shp")
#%%
uliveti_gdf = gpd.GeoDataFrame(
    uliveti,
    crs='EPSG:32633',
    )
#save the dataframe
#%%
uliveti_gdf.to_file("uliveti.geojson") 
#%%
url = 'https://github.com/napo/geospatial_course_unitn/raw/master/data/istat/istat_administrative_units_2022.gpkg'
regions = gpd.read_file(url,layer="regions")
puglia = regions[regions['DEN_REG'] == "Puglia"]
#%% #extract municipalities and provinces
municipalities = gpd.read_file(url,layer="municipalities")
puglia_mun = municipalities[municipalities['COD_REG'] == 16]
provinces = gpd.read_file(url,layer="provincies")
puglia_prov = provinces[provinces['COD_REG'] == 16]
#%%
#plot all the trees
ax = puglia.to_crs(epsg=4326).plot(edgecolor='k', facecolor='none', figsize=(15, 10))
uliveti_gdf.to_crs(epsg=4326).plot(ax=ax,color="green")
#add a title
plt.title("Olive trees In Puglia")
#%% #plot provinces according to the number of trees
olives_prov = gpd.sjoin(puglia.to_crs(epsg=4326), 
                          uliveti_gdf.to_crs(epsg=4326), how='inner', predicate='intersects', lsuffix='provinces_', rsuffix='ulives')
k = olives_prov.groupby(['COD_PROV']).index_ulives.count()
puglia_prov['olives'] = puglia_prov['COD_PROV'].map(k)
puglia_prov.to_crs(epsg=4326).plot(column='olives', cmap='Greens', edgecolor = "k",figsize=(15, 10), legend=True)
#add a title
plt.title("Number of olive trees in Puglia - Provinces")
#%% #plot municipalities according to the number of trees
olives_mun = gpd.sjoin(puglia_mun.to_crs(epsg=4326),
                          uliveti_gdf.to_crs(epsg=4326), how='inner', predicate='intersects', lsuffix='municipalities_', rsuffix='ulives')
k = olives_mun.groupby(['PRO_COM']).index_ulives.count()
puglia_mun['olives'] = puglia_mun['PRO_COM'].map(k)
puglia_mun.to_crs(epsg=4326).plot(column='olives', cmap='Greens', edgecolor = "k",figsize=(15, 10), legend=True)
#add a title
plt.title("Number of olive trees in Puglia - Municipalities")
#%% #plot provinces according to the number of trees scaled for the area of the province
olives_prov = gpd.sjoin(puglia.to_crs(epsg=4326),
                          uliveti_gdf.to_crs(epsg=4326), how='inner', predicate='intersects', lsuffix='provinces_', rsuffix='ulives')
k = olives_prov.groupby(['COD_PROV']).index_ulives.count()
puglia_prov['olives'] = puglia_prov['COD_PROV'].map(k)
puglia_prov['olives_scaled'] = puglia_prov['olives']/puglia_prov['SHAPE_AREA']
puglia_prov.to_crs(epsg=4326).plot(column='olives_scaled', cmap='Greens', edgecolor = "k",figsize=(15, 10), legend=True)
plt.title("Density of olive trees in Puglia - Provinces")

#%% #plot municipalities according to the number of trees scaled for the area of the municipality
olives_mun = gpd.sjoin(puglia_mun.to_crs(epsg=4326),
                          uliveti_gdf.to_crs(epsg=4326), how='inner', predicate='intersects', lsuffix='municipalities_', rsuffix='ulives')
k = olives_mun.groupby(['PRO_COM']).index_ulives.count()
puglia_mun['olives'] = puglia_mun['PRO_COM'].map(k)
puglia_mun['olives_scaled'] = puglia_mun['olives']/puglia_mun['Shape_Area']
puglia_mun.to_crs(epsg=4326).plot(column='olives_scaled', cmap='Greens', edgecolor = "k",figsize=(15, 10), legend=True)
plt.title("Density of olive trees in Puglia - Municipalities")

#%%

#sample 1000 trees
uliveti_gdf_sample = uliveti_gdf.sample(1000)

#create a dataframe with all distances
df = pd.DataFrame(columns=['source','target','distance']) 

#%%
#iterate over all the trees
for i in range(0,len(uliveti_gdf_sample)):
      for j in range(i+1,len(uliveti_gdf_sample)):
            #calculate the distance between the two trees
            dist = uliveti_gdf_sample.iloc[i]['geometry'].distance(uliveti_gdf_sample.iloc[j]['geometry'])
            #add the distance to the dataframe
            df = df.append({'source':uliveti_gdf_sample.iloc[i]["id"],'target':uliveti_gdf_sample.iloc[j]["id"],'distance':dist},ignore_index=True)
      print(i)
    
# %%
#save the dataframe
df.to_csv("distances.csv")
# %%