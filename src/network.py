#%%
from imports import *
#%% Read Files
puglia_mun = gpd.read_file("/Users/Matteo/Xylella-Diffusion/final/data/puglia_mun.geojson")
uliveti_gdf = gpd.read_file("/Users/Matteo/Xylella-Diffusion/final/data/uliveti.geojson")
puglia = gpd.read_file("/Users/Matteo/Xylella-Diffusion/final/data/puglia.geojson")
### Here we show an example of the neighbors of a given olive grove
#%% Focus on single municipality
olives_mun = gpd.sjoin(puglia_mun.to_crs(epsg=4326),
                          uliveti_gdf.to_crs(epsg=4326), how='inner', predicate='intersects', lsuffix='municipalities_', rsuffix='ulives')
#extract rows in olives_mun for lecce municipality
k = olives_mun[olives_mun['COMUNE'] == "Lecce"]
#extract rows in uliveti with id in k
uliveti_mun = uliveti_gdf[uliveti_gdf['id'].isin(k['id'])]

#%% plot Lecce municipality with olive groves inside it 
ax = puglia_mun.to_crs(epsg=4326)[puglia_mun['COMUNE'] == "Lecce"].plot(edgecolor='k', facecolor='none', figsize=(15, 10))
uliveti_mun.to_crs(epsg=4326).plot(ax=ax, color='green', markersize=1,edgecolor='black', facecolor='none')
ax.set_axis_off()
#title
ax.set_title('Lecce municipality with olive groves')
#save figure
ax.figure.savefig('/Users/Matteo/Xylella-Diffusion/img/lecce.png', dpi=300)
#%% #select a random grove and plot all its neighbors according to the distance
ulivo = uliveti_mun.iloc[79]
uliveti_mun['distance'] = uliveti_mun['geometry'].apply(lambda x: ulivo["geometry"].distance(x))

ax = puglia_mun.to_crs(epsg=4326)[puglia_mun['COMUNE'] == "Lecce"].plot(edgecolor='k', facecolor='none', figsize=(15, 10))
uliveti_mun.to_crs(epsg=4326).plot(ax = ax, edgecolor = "k", column='distance', cmap='YlGn_r', figsize=(15, 10), legend=False)
uliveti_mun[uliveti_mun["id"] == ulivo["id"]].to_crs(epsg=4326).plot(ax=ax, color='red', markersize=100)
sm = plt.cm.ScalarMappable(cmap='YlGn_r',norm = plt.Normalize(vmin=0, vmax= uliveti_mun['distance'].max()))
sm._A = []
cbar = ax.figure.colorbar(sm)
ax.set_axis_off()
cbar.ax.set_title('Distance from target olive grove (m)', loc='center')
ax.set_title("Distance between target olive grove and "+"\n"+"other olive groves in Lecce municipality")
ax.figure.savefig('/Users/Matteo/Xylella-Diffusion/final/img/lecce_dist.png', dpi=300,transparent=False,facecolor='white')

#%% Now we create the frames for different radius
A = [0,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,11000,12000,13000,14000,15000]
for alpha in A:
    uliveti_mun['color'] = uliveti_mun['distance'].apply(lambda x: 'green' if x < alpha else 'gray')
    #plot ulivo and uliveti_bari colored by distance
    ax = puglia_mun.to_crs(epsg=4326)[puglia_mun['COMUNE'] == "Lecce"].plot(edgecolor='k', facecolor='none', figsize=(15, 10))
    #plot uliveti colored by the color set in color "column"
    uliveti_mun.to_crs(epsg=4326).plot(ax = ax, edgecolor = "k", column='color', cmap = cmap, figsize=(15, 10))
    uliveti_mun[uliveti_mun["id"] == ulivo["id"]].to_crs(epsg=4326).plot(ax=ax, color='red', markersize=100)
    #remove axes
    ax.set_axis_off()
    #add title 
    ax.set_title("Olive trees in Lecce municipality with distance less than "+ str(alpha) +  " m from the target olive tree")
    ax.figure.savefig('/Users/Matteo/Xylella-Diffusion/final/img/neig'+str(alpha)+'.png', dpi=300,transparent = False, facecolor='white')


####### PROPER NETWORK CREATION
#%% Network building
df = pd.read_csv("/Users/Matteo/Xylella-Diffusion/data/distances.csv",header= None)
df.columns = ['source', 'target', 'distance']
df = df[df['distance'] <= 1000]
df['source'] = df['source'].astype(str)
df['target'] = df['target'].astype(str)
G = nx.from_pandas_edgelist(df, source='source', target='target', edge_attr='distance')
#%% Plot of the degree distribution
deg = dict(G.degree)
deg = list(deg.values())
plt.hist(deg, bins=100)
plt.xlabel("degree")
plt.ylabel("count")
plt.axvline(np.mean(deg), color='r', linestyle='dashed', linewidth=1)
plt.text(0.6, 0.8, r'$<k>=%.2f$' % np.mean(deg), fontsize=15, transform=plt.gcf().transFigure)
plt.title("Degree distribution")
plt.savefig("/Users/Matteo/Xylella-Diffusion/final/img/degree_distribution.png")
#%% Here we plot all the groves colored according to their degree
ax = puglia.to_crs(epsg=4326).plot(edgecolor='k', facecolor='none', figsize=(15, 10))
deg = dict(G.degree)
deg = {str(k): v for k, v in deg.items()}
uliveti_gdf['degree'] = uliveti_gdf.id.map(deg)
uliveti_gdf.to_crs(epsg=4326).plot(ax=ax, column='degree', cmap='viridis_r', markersize=1)
sm = plt.cm.ScalarMappable(cmap='viridis_r', norm=plt.Normalize(vmin=0, vmax=uliveti_gdf['degree'].max()))
sm._A = []
plt.colorbar(sm)
#save figure
ax.set_axis_off()
ax.figure.savefig('/Users/Matteo/Xylella-Diffusion/final/img/degree.png', dpi=300,transparent=False,facecolor='white')


####### BETWEENNESS CENTRALITY OF MUNICIPALITIES
#%% example of intersection between municipalities
puglia_mun = gpd.read_file("/Users/Matteo/Xylella-Diffusion/final/data/puglia_mun.geojson")
municipality_1 = puglia_mun[puglia_mun['COMUNE'] == "Otranto"]["geometry"]
municipality_2 = puglia_mun[puglia_mun['COMUNE'] == "Giurdignano"]["geometry"]
print(municipality_1.iloc[0].intersects(municipality_2.iloc[0]))
ax = municipality_1.to_crs(epsg=4326).plot(edgecolor='k', facecolor='lightblue', figsize=(15, 10))
municipality_2.to_crs(epsg=4326).plot(ax=ax,facecolor = "lightgreen", edgecolor='k')
intersection = municipality_1.iloc[0].intersection(municipality_2.iloc[0])
intersection = gpd.GeoDataFrame(geometry=[intersection], crs=puglia_mun.crs)
intersection.to_crs(epsg=4326).plot(ax=ax,color="red")
ax.axis("off")
plt.title("Intersection between Otranto Municipality (blue) and Giurdignano Municipality (green)")
plt.savefig("/Users/Matteo/Xylella-Diffusion/final/img/intersection.png")

#%% New edgelist
#Now we want to create a graph where the nodes are the municipalities 
# and the edges are the intersections between municipalities
edgelist = []
for i in range(len(puglia_mun)):
    print(i)
    for j in range(len(puglia_mun)):
        if puglia_mun.iloc[i].geometry.intersects(puglia_mun.iloc[j].geometry):
            edgelist.append([puglia_mun.iloc[i].PRO_COM, puglia_mun.iloc[j].PRO_COM])
            print(j)
edgelist = pd.DataFrame(edgelist, columns=["source", "target"])
edgelist = edgelist.drop_duplicates()

#%% create a graph from the edgelist and calculate betweenness
G = nx.from_pandas_edgelist(edgelist, source="source", target="target")
betweenness_centrality = nx.betweenness_centrality(G)
puglia_mun['betweenness_centrality'] = puglia_mun['PRO_COM'].map(betweenness_centrality)

#%% #plot municipalities according to the betweenness centrality
puglia_mun.to_crs(epsg=4326).plot(column='betweenness_centrality', cmap='viridis_r', edgecolor = "k",figsize=(15, 10), legend=False)
sm = plt.cm.ScalarMappable(cmap='viridis_r', norm=plt.Normalize(vmin=0, vmax=puglia_mun['betweenness_centrality'].max()))
sm._A = []
plt.colorbar(sm)
plt.axis("off")
plt.title("Betweenness centrality of municipalities in Puglia")
plt.savefig("/Users/Matteo/Xylella-Diffusion/final/img/betweenness_centrality_munic.png", dpi=300)
