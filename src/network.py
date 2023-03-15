#%%
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random as rand

#%%
#load the dataframe with the distances
df = pd.read_csv("/Users/Matteo/Xylella-Diffusion/data/distances.csv",header= None)
#change the name of the columns
#%%
df.columns = ['source', 'target', 'distance']
#mean of the distances
#filter dataset with only rows with distance <= 1 km
df1 = df[df['distance'] <= 3000]

#%%
#create a network from the dataframe
G = nx.from_pandas_edgelist(df1, source='source', target='target', edge_attr='distance')
#save the network
#nx.write_gexf(G, "/Users/Matteo/Xylella-Diffusion/data/network.gexf")
#%%
#calculate average edge length
max_edge_length = max(list(nx.get_edge_attributes(G,'distance').values()))
#%%
#evolution of the size of the largest connected component
S = []
alpha = np.linspace(0,max_edge_length,100)
for i in alpha:
    #create a new graph with edges shorter than i
    G1 = G.copy()
    G1.remove_edges_from([e for e in G1.edges if G1.edges[e]['distance'] > i])
    #calulate the size of the largest connected component
    largest_cc = max(nx.connected_components(G1), key=len)
    S.append(len(largest_cc)/len(G.nodes))
#plot evolution of the size of the largest connected component
plt.plot([i/1000 for i in alpha] ,S)
plt.xlabel("radius of the circle (km)")
plt.ylabel("size of the largest connected component")
plt.show()

# %%
ax = puglia.to_crs(epsg=4326).plot(edgecolor='k', facecolor='none', figsize=(15, 10))
deg = dict(G.degree)
deg = {str(k): v for k, v in deg.items()}
uliveti_gdf['degree'] = uliveti_gdf.id.map(deg)
uliveti_gdf.to_crs(epsg=4326).plot(ax=ax, column='degree', cmap='viridis_r', markersize=1)
sm = plt.cm.ScalarMappable(cmap='viridis_r', norm=plt.Normalize(vmin=0, vmax=uliveti_gdf['degree'].max()))
sm._A = []
plt.colorbar(sm)
plt.show()
#increase the quality of the map to better zoom in


#%%
#same as before, but color according to betweenness centrality
bet = nx.betweenness_centrality(G, weight='distance')
bet = {str(k): v for k, v in bet.items()}
uliveti_gdf['betweenness'] = uliveti_gdf.id.map(bet)
ax = puglia.to_crs(epsg=4326).plot(edgecolor='k', facecolor='none', figsize=(15, 10))
uliveti_gdf.to_crs(epsg=4326).plot(ax=ax, column='betweenness', cmap='inferno', markersize=1)
#add legend to the map
sm = plt.cm.ScalarMappable(cmap='inferno', norm=plt.Normalize(vmin=0, vmax=uliveti_gdf['betweenness'].max()))
sm._A = []
plt.colorbar(sm)
plt.show()

#%%
beta = 1
gamma = 0.2
S = []
I = []
R = []
S.append(len(G.nodes)-1)
I.append(1)
R.append(0)
list_nodes = list(G.nodes)
infected = [rand.choice(list_nodes)]
recovered = []
susceptible = [list_nodes[i] for i in range(len(list_nodes)) if i not in infected]
dark_red = (0.8,0,0,1)
#create vector for green color
green = (0,0.8,0,1)
#create vector for grey color
grey = (0.8,0.8,0.8,1)

#%%
matrix = np.zeros((len(G.nodes), len(G.nodes)))
t = 0
uliveti_gdf['status'] = 0
#%%
#import listedcolormap
from matplotlib.colors import ListedColormap
while len(infected)>0:
    #add to the matrix the status of the nodes
    #add 1 to the infected nodes
    for node in infected:
        matrix[t][node] = 1
        uliveti_gdf.loc[uliveti_gdf['id'] == str(node), 'status'] = 1
    #add 2 to the recovered nodes
    for node in recovered:
        matrix[t][node] = 2
        uliveti_gdf.loc[uliveti_gdf['id'] == str(node), 'status'] = 2
    print("time: "+str(t))
    print("S: "+str(len(susceptible)))
    print("I: "+str(len(infected)))
    print("R: "+str(len(recovered)))
    ax = puglia.to_crs(epsg=4326).plot(edgecolor='k', facecolor='none', figsize=(15, 10))
    tab20c = plt.cm.get_cmap('tab20c', 20)
    colors = [green, dark_red, grey]
    cmap = ListedColormap(colors)
    uliveti_gdf.to_crs(epsg=4326).plot(ax=ax, column='status', cmap=cmap, markersize=1)
    #show the map with high quality
    plt.savefig("map"+str(t)+".png", dpi=300)
    plt.show()
    #add new infected nodes
    inf1 = infected.copy() #to avoid changing the list while iterating
    for node in inf1:
        for neighbor in G.neighbors(node):
            if neighbor in susceptible:
                if rand.random() < beta:
                    infected.append(neighbor)
                    susceptible.remove(neighbor)
    for node in inf1:
        if rand.random() < gamma:
            recovered.append(node)
            infected.remove(node)
    #update lists
    S.append(len(susceptible))
    I.append(len(infected))
    R.append(len(recovered))
    t += 1

#%%
#plot only map with infected nodes
#update status of the nodes
uliveti_gdf.loc[uliveti_gdf['id'] == "1"]



#%%
#create vector for dark red color
dark_red = np.array([0.8,0,0,1])
#create vector for green color
green = np.array([0,0.8,0,1])
#create vector for grey color
grey = np.array([0.8,0.8,0.8,1])


#%%
# image resolution
dpi=200

# For each step of the matrix 
for i in range(len(matrix)):
 
    # Turn interactive plotting off
    plt.ioff()

    # initialize a figure
    fig = plt.figure(figsize=(680/dpi, 480/dpi), dpi=dpi)
    
    # Find the subset of the dataset for the current year
    subsetData = matrix[i]

    # Build the scatterplot
    plt.scatter(
        x=subsetData['lifeExp'], 
        y=subsetData['gdpPercap'], 
        s=subsetData['pop']/200000 , 
        c=subsetData['continent'].cat.codes, 
        cmap="Accent", alpha=0.6, edgecolors="white", linewidth=2)
    
    # Add titles (main and on axis)
    plt.yscale('log')
    plt.xlabel("Life Expectancy")
    plt.ylabel("GDP per Capita")
    plt.title("Year: "+str(i) )
    plt.ylim(0,100000)
    plt.xlim(30, 90)
    
    # Save it & close the figure
    filename='/Users/yan.holtz/Desktop/Gapminder_step'+str(i)+'.png'
    plt.savefig(fname=filename, dpi=96)
    plt.gca()
    plt.close(fig)


#select row in uliveti gdf with id = 1
uliveti_gdf[uliveti_gdf['id'] == 1]

#%% 
#plot colormap with three colors for the three status
#%%
#initialize the list of colors
colors = []
#iterate over the nodes
for node in G.nodes:
    #if node is susceptible
    if node in susceptible:
        colors.append('grey')
    #if node is infected
    elif node in infected:
        colors.append('red')
    #if node is recovered
    else:
        colors.append('green')
#%%



# %%
