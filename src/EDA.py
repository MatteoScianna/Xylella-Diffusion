#%%
from imports import *

#%% #plot olive groves distribution
puglia = gpd.read_file("/Users/Matteo/Xylella-Diffusion/data/puglia.geojson")
uliveti_gdf = gpd.read_file("/Users/Matteo/Xylella-Diffusion/data/uliveti.geojson")
ax = puglia.to_crs(epsg=4326).plot(edgecolor='k', facecolor='none', figsize=(15, 10))
uliveti_gdf.to_crs(epsg=4326).plot(ax=ax,color="green")
ax.axis('off')
plt.title("Olive groves In Puglia")
plt.savefig("/Users/Matteo/Xylella-Diffusion/final/img/olive_groves_map.png", dpi=300,transparent=False, facecolor="white")
#%% #plot provinces according to the number of groves
puglia_prov = gpd.read_file("/Users/Matteo/Xylella-Diffusion/data/puglia_prov.geojson")
olives_prov = gpd.sjoin(puglia_prov.to_crs(epsg=4326), 
                          uliveti_gdf.to_crs(epsg=4326), how='inner', predicate='intersects', lsuffix='provinces_', rsuffix='ulives')
k = olives_prov.groupby(['COD_PROV']).index_ulives.count()
puglia_prov['olives'] = puglia_prov['COD_PROV'].map(k)
ax = puglia_prov.to_crs(epsg=4326).plot(column='olives', cmap='Greens', edgecolor = "k",figsize=(15, 10), legend=True)
ax.axis('off')
plt.title("Number of olive groves in Puglia - Provinces")
plt.savefig("/Users/Matteo/Xylella-Diffusion/final/img/olive_groves_provinces.png", dpi=300,transparent=False, facecolor="white")
   



#%% #plot municipalities according to the number of groves
puglia_mun = gpd.read_file("/Users/Matteo/Xylella-Diffusion/data/puglia_mun.geojson")
olives_mun = gpd.sjoin(puglia_mun.to_crs(epsg=4326),
                          uliveti_gdf.to_crs(epsg=4326), how='inner', predicate='intersects', lsuffix='municipalities_', rsuffix='ulives')
k = olives_mun.groupby(['PRO_COM']).index_ulives.count()
puglia_mun['olives'] = puglia_mun['PRO_COM'].map(k)
ax = puglia_mun.to_crs(epsg=4326).plot(column='olives', cmap='Greens', edgecolor = "k",figsize=(15, 10), legend=True)
#add a title
ax.axis('off')
plt.title("Number of olive groves in Puglia - Municipalities")
plt.savefig("/Users/Matteo/Xylella-Diffusion/final/img/olive_groves_municipalities.png", dpi=300,transparent=False, facecolor="white")

#%% #plot provinces according to the number of groves scaled for the area of the province
olives_prov = gpd.sjoin(puglia_prov.to_crs(epsg=4326),
                          uliveti_gdf.to_crs(epsg=4326), how='inner', predicate='intersects', lsuffix='provinces_', rsuffix='ulives')
k = olives_prov.groupby(['COD_PROV']).index_ulives.count()
puglia_prov['olives'] = puglia_prov['COD_PROV'].map(k)
puglia_prov['olives_scaled'] = puglia_prov['olives']/puglia_prov['SHAPE_AREA']
ax = puglia_prov.to_crs(epsg=4326).plot(column='olives_scaled', cmap='Greens', edgecolor = "k",figsize=(15, 10), legend=True)
ax.axis('off')
plt.title("Density of olive groves in Puglia - Provinces")
plt.savefig("/Users/Matteo/Xylella-Diffusion/final/img/olive_groves_provinces_scaled.png", dpi=300,transparent=False, facecolor="white")

#%% plot municipalities according to the number of groves scaled for the area of the municipality (fixed and dynamic) 
# scaled for the area of the municipality
olives_mun = gpd.sjoin(puglia_mun.to_crs(epsg=4326),
                          uliveti_gdf.to_crs(epsg=4326), how='inner', predicate='intersects', lsuffix='municipalities_', rsuffix='ulives')
k = olives_mun.groupby(['PRO_COM']).index_ulives.count()
puglia_mun['olives'] = puglia_mun['PRO_COM'].map(k)
puglia_mun[r'olives per km^2'] = (puglia_mun['olives']*1000000)/puglia_mun['Shape_Area']
puglia_mun1 = puglia_mun[['olives',r'olives per km^2','COMUNE',"geometry"]]
ax = puglia_mun1.to_crs(epsg=4326).plot(column=r'olives per km^2', cmap='Greens', edgecolor = "k",figsize=(15, 10), legend=False)
#description of the legend
vmin, vmax = puglia_mun1[r'olives per km^2'].min(), puglia_mun1[r'olives per km^2'].max()
sm = plt.cm.ScalarMappable(cmap='Greens', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = plt.colorbar(sm)
cbar.set_label(r'olives per $km^2$')
#change position of the label of the colorbar
cbar.ax.yaxis.set_label_position('left')
#increase font of the title of the colorbar
ax.axis('off')
plt.title("Density of olive groves in Puglia - Municipalities")
plt.savefig("/Users/Matteo/Xylella-Diffusion/final/img/olive_groves_municipalities_scaled.png", dpi=300,transparent=False, facecolor="white")
map = folium.Map(location=[40.5, 17.5], zoom_start=7, tiles='cartodbpositron')
puglia_mun1.explore(column=r'olives per km^2', m= map,cmap='viridis_r',legend=False)
map.save("olives_mun.html")
# %%
