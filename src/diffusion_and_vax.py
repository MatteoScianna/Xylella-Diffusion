#%% imports
from imports import *
# %%
################### MULTI-FACTOR-BASED VACCINATION #################
# %% read files

uliveti = gpd.read_file("/Users/Matteo/Xylella-Diffusion/data/uliveti.geojson")
uliveti_gallipoli = uliveti.to_crs(epsg =4326)[uliveti.to_crs(epsg =4326).intersects(puglia_mun.to_crs(epsg =4326)[puglia_mun.to_crs(epsg =4326)["COMUNE"] == "Gallipoli"].iloc[0].geometry)] 
niter = 100
MAT_4 = np.zeros((niter, len(uliveti)))
MAT_VAX = np.zeros((niter, len(uliveti)))
tot_inf = np.zeros(niter)
tot_vax = np.zeros(niter)

#%% #Parameter Setting
niter = 100

B = 14.069
A = 3
max_area = uliveti.area.max()
iter = 0
alpha = 0
att_level = 1
conservatorism = 0.1
d = 6
p = 0.2

#%% #simulations
while iter < niter:
    print("iter: "+str(iter))
    infected_points = {}
    vax_points =[]
    uliveto = uliveti_gallipoli.sample(1)
    infected_points[uliveto.index[0]] = np.exp(-B)
    t = 0
    while t<5:
        print("time: "+str(t))
        infected_points1 = infected_points.copy()

        #Eradication
        for index, value in infected_points1.items():
            uliveti_short = uliveti[uliveti.distance(uliveti.iloc[index].geometry) < 2000]
            uliveti_short_vax = uliveti_short[uliveti_short.index.isin(vax_points)]
            beta = uliveti_short_vax.shape[0]/uliveti_short.shape[0]
            if (1/3)*beta+(1/3)*att_level+(1/3)*value > conservatorism:
                vax_points.append(index)
                #print("eradicating uliveto "+str(index))
                infected_points.pop(index)

        #Short-range diffusion
        for index, value in infected_points1.items():
            area = uliveti[uliveti.index == index].area.iloc[0]/max_area
            k = area+alpha*(1-area)
            infected_points[index] = (1-k)*(value*(1/(1-k)))**np.exp(-A)
            uliveti_short = uliveti[uliveti.distance(uliveti.iloc[index].geometry) < 2000]
            uliveti_short = uliveti_short[~uliveti_short.index.isin(infected_points1.keys())]
            uliveti_short["distance"] = uliveti_short.distance(uliveti.iloc[index].geometry)
            for index1, row in uliveti_short.iterrows():
                if np.exp(-row["distance"]/100) > 0.2:
                    infected_points[index1] = np.exp(-B)

        #long-range diffusion
        for index, value in infected_points1.items():
            if value > p:
                n = np.random.randint(1, d)
                for i in range(n):
                    x, y = np.random.multivariate_normal([0, 0], [[20, 0], [0, 20]])
                    dist = np.sqrt(x**2 + y**2)
                    uliveti_short = uliveti[uliveti.distance(uliveti.iloc[index].geometry)/1000 - dist < 0.01]
                    uliveto1 = uliveti_short[~uliveti_short.index.isin(infected_points.keys())].sample(1) if not uliveti_short[~uliveti_short.index.isin(infected_points.keys())].empty else pd.DataFrame()    
                    if not uliveto1.empty:
                        infected_points[uliveto1.index[0]] = np.exp(-B)
                    else:
                        print("no uliveto found")
                        pass
        #update self level of infection
        for index, value in infected_points.items():
            #update matrices
            if t == 4:
                MAT_4[iter][index] = value
                MAT_VAX[iter][index] = 1 if index in vax_points else 0
    
        print("total infected: "+str(len(infected_points)))
        print("total vaccinated: "+str(len(vax_points)))
        t += 1
    tot_inf[iter] = len(infected_points)
    tot_vax[iter] = len(vax_points)
    iter += 1



#%%
##### BETWEENNESS CENTRALITY BASED VACCINATION #######

#%% Read data

df = pd.read_csv("/Users/Matteo/Xylella-Diffusion/data/distances.csv",header= None)
df.columns = ['source', 'target', 'distance']
df = df[df['distance'] <= 1000]
df['source'] = df['source'].astype(str)
df['target'] = df['target'].astype(str)
puglia_prov = gpd.read_file("/Users/Matteo/Xylella-Diffusion/data/puglia_prov.geojson")
#remove from df the edges that are not in the uliveti_lecce
uliveti_lecce = uliveti.to_crs(epsg=4326)[uliveti.to_crs(epsg=4326).intersects(puglia_prov.to_crs(epsg=4326).geometry.iloc[0])] 
df1 = df[df['source'].isin(uliveti_lecce.id) & df['target'].isin(uliveti_lecce.id)]
#%% #create a network from the dataframe and compute betweenness centrality
G = nx.from_pandas_edgelist(df1, source='source', target='target', edge_attr='distance')
betw = nx.betweenness_centrality(G)
betw = {k: v/max(betw.values()) for k, v in betw.items()}
betw = {int(k):v for k,v in betw.items()}

#%% Plot olive groves in Lecce province according to their betweenness centrality  
fig, ax = plt.subplots(figsize=(10,10))   
ax.axis("off")
plt.title("Betweenness centrality of olive groves in the province of Lecce"+"\n"+"Network radius = 1 km")
puglia_prov.to_crs(epsg=4326).plot(ax=ax, color="white", edgecolor="black")
uliveti_lecce['betw'] = uliveti_lecce.id.map(betw)
uliveti_lecce.to_crs(epsg=4326).plot(ax=ax, column='betw', cmap='viridis_r', markersize=1,legend=False)
sm = plt.cm.ScalarMappable(cmap="viridis_r", norm=plt.Normalize(vmin=0, vmax=1))
sm._A = []
cax = fig.add_axes([ax.get_position().x1-0.55,ax.get_position().y0+0.01,0.02,ax.get_position().height/3])
cbar = plt.colorbar(sm, ax=ax, orientation="vertical",cax = cax)
cbar.ax.set_ylabel('Betweenness Centrality', rotation=0,loc = 'bottom',labelpad=1)
cbar.ax.yaxis.set_label_coords(2.6,0.05)
cbar.ax.set_yticklabels([' ','0.2', '0.4', '0.6', '0.8', '1'])
#save
plt.savefig("/Users/Matteo/Xylella-Diffusion/img/betw_lecce.png", dpi=300, bbox_inches='tight')


#%% Simulate diffusion with betweenness centrality based vaccination
niter = 100
MAT_4 = np.zeros((niter, len(uliveti)))
MAT_VAX = np.zeros((niter, len(uliveti)))
B = 14.069
A = 3
max_area = uliveti.area.max()
iter = 0
alpha = 0
vax_radius = 2000
max_vax = 5
p = 0.2
d = 6
while iter < niter:
    print("iter: "+str(iter))
    infected_points = {}
    vax_points =[]
    uliveto = uliveti_gallipoli.sample(1)
    infected_points[uliveto.index[0]] = np.exp(-B)
    t = 0
    while t<5:
        print("time: "+str(t))
        infected_points1 = infected_points.copy()

        #vaccination
        print("eradication")
        for index, value in infected_points1.items():
            uliveti_short = uliveti[uliveti.distance(uliveti.iloc[index].geometry) < vax_radius]
            uliveti_short = uliveti_short[~uliveti_short.index.isin(vax_points)]
            uliveti_short = uliveti_short[~uliveti_short.index.isin(infected_points.keys())]
            uliveti_short["betw"] = uliveti_short.index.map(betw)
            uliveti_short = uliveti_short.sort_values(by="betw", ascending=False)
            n_vax = rand.randint(1, max_vax)   
            if len(uliveti_short) >= n_vax:
                vax_points.extend(uliveti_short.index[:n_vax])
            else:
                vax_points.extend(uliveti_short.index)            

        print("short-range diffusion")
        for index, value in infected_points1.items():
            area = uliveti[uliveti.index == index].area.iloc[0]/max_area
            k = area+alpha*(1-area)
            infected_points[index] = (1-k)*(value*(1/(1-k)))**np.exp(-A)
            uliveti_short = uliveti[uliveti.distance(uliveti.iloc[index].geometry) < 2000]
            uliveti_short = uliveti_short[~uliveti_short.index.isin(vax_points)]
            uliveti_short = uliveti_short[~uliveti_short.index.isin(infected_points1.keys())]
            uliveti_short["distance"] = uliveti_short.distance(uliveti.iloc[index].geometry)
            for index1, row in uliveti_short.iterrows():
                if np.exp(-row["distance"]/100) > 0.2:
                    infected_points[index1] = np.exp(-B)
                    print("infecting uliveto " + str(index1))

        #long-range diffusion#
        print("long-range diffusion")
        print("total infected: "+str(len(infected_points1)))
        for index, value in infected_points1.items():
            print("index: "+str(index),"value: "+str(value))
        for index, value in infected_points1.items():
            if value > p:
                n = np.random.randint(1, d)
                print("total dispersal for ulivo "+str(index)+" = " + str(n))
                for i in range(n):
                    x, y = np.random.multivariate_normal([0, 0], [[20, 0], [0, 20]])
                    dist = np.sqrt(x**2 + y**2)
                    uliveti_short = uliveti[uliveti.distance(uliveti.iloc[index].geometry)/1000 - dist < 0.01]
                    uliveto1 = uliveti_short[~uliveti_short.index.isin(infected_points.keys())].sample(1) if not uliveti_short[~uliveti_short.index.isin(infected_points.keys())].empty else pd.DataFrame()
                    if not uliveto1.empty:
                        infected_points[uliveto1.index[0]] = np.exp(-B)
                        print("infecting uliveto " + str(uliveto1.index[0]))
                    else:
                        print("no uliveto found")

        #update self level of infection
        for index, value in infected_points.items():
            if t == 4:
                MAT_4[iter][index] = value
                MAT_VAX[iter][index] = 1 if index in vax_points else 0
        print("total infected: "+str(len(infected_points)+len(vax_points)))
        t += 1
    iter += 1
