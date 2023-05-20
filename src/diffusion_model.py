#%%
from imports import *
#%% data loading
puglia_mun = gpd.read_file("/Users/Matteo/Xylella-Diffusion/data/puglia_mun.geojson")
uliveti = gpd.read_file("/Users/Matteo/Xylella-Diffusion/data/uliveti.geojson")
puglia_prov = gpd.read_file("/Users/Matteo/Xylella-Diffusion/data/puglia_prov.geojson")
#%%
######## DIFFUSION MODEL ##########
#%% Implementation of the diffusion model 
uliveti_gallipoli = uliveti.to_crs(epsg =4326)[uliveti.to_crs(epsg =4326).intersects(puglia_mun.to_crs(epsg =4326)[puglia_mun.to_crs(epsg =4326)["COMUNE"] == "Gallipoli"].iloc[0].geometry)] 
MAT_4 = np.zeros((niter, len(uliveti)))
#parameters 
niter = 100
B = 14.069
A = 3
d = 6
t_max = 5
max_area = uliveti.area.max()
iter = 0
alpha = 0
p = 0.2

#simulations
while iter < niter:
    print("iter: "+str(iter))
    infected_points = {}
    uliveto = uliveti_gallipoli.sample(1)
    infected_points[uliveto.index[0]] = np.exp(-B)
    t = 0
    while t<t_max:
        print("time: "+str(t))
        #short-range diffusion#
        infected_points1 = infected_points.copy()
        print("short-range diffusion")
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
                #for each random number
                for i in range(n):
                    #print(i)
                    #generate a random point in a 2d gaussian distribution with mean 0 and standard deviation 20km 
                    x, y = np.random.multivariate_normal([0, 0], [[20, 0], [0, 20]])
                    #get distance between (x,y) and (0,0)
                    dist = np.sqrt(x**2 + y**2)
                    #get uliveto with distance from uliveto closest to dist 
                    uliveti_short = uliveti[uliveti.distance(uliveti.iloc[index].geometry)/1000 - dist < 0.01]
                    #select a random uliveto from uliveti_short
                    #filter for only non infected uliveti
                    uliveto1 = uliveti_short[~uliveti_short.index.isin(infected_points.keys())].sample(1) if not uliveti_short[~uliveti_short.index.isin(infected_points.keys())].empty else pd.DataFrame()
                    #if uliveto is not empty
                    if not uliveto1.empty:
                        #add uliveto to infected_points
                        infected_points[uliveto1.index[0]] = np.exp(-B)
                        print("infecting uliveto " + str(uliveto1.index[0]))
                    else:
                        print("no uliveto found")

        #update self level of infection
        for index, value in infected_points.items():
            #update matrices
            if t == t_max-1:
                MAT_4[iter][index] = value
        print("total infected: "+str(len(infected_points)))
        t += 1
    iter += 1

#%%
##### Plot of the averaged results #####
#%% create a nex array A where A[i] is the mean of MAT_4[j][i] for j in range(0,100)
A = np.zeros(len(uliveti))
for i in range(0, len(uliveti)):
    A[i] = np.mean(MAT_4[:,i])
# %% Add new column for infection level
uliveti_infected = uliveti.copy()
uliveti_infected["infected"] = A
uliveti_infected = uliveti_infected[uliveti_infected.infected > 0]
# %% Plot
puglia_prov = puglia_prov[puglia_prov["DEN_PROV"].isin(["Lecce"])]
fig, ax = plt.subplots(figsize=(10,10))   
ax.axis("off")
plt.title("Diffusion of Xylella Fastidiosa in Puglia after 5 years"+"\n"+"Average over 100 iterations of the model")
puglia_prov.to_crs(epsg=4326).plot(ax=ax, color="white", edgecolor="black")
uliveti_infected.to_crs(epsg=4326).plot(ax=ax, column="infected", cmap="inferno_r", legend=False)
sm = plt.cm.ScalarMappable(cmap="inferno_r", norm=plt.Normalize(vmin=0, vmax=1))
sm._A = []
cax = fig.add_axes([ax.get_position().x1-0.55,ax.get_position().y0+0.01,0.02,ax.get_position().height/3])
cbar = plt.colorbar(sm, ax=ax, orientation="vertical",cax = cax)
cbar.ax.set_ylabel('Self level of infection', rotation=0,loc = 'bottom',labelpad=1)
cbar.ax.yaxis.set_label_coords(2.6,0.05)
cbar.ax.set_yticklabels([' ','0.2', '0.4', '0.6', '0.8', '1'])
plt.savefig("diffusion_5years.png", dpi=300, bbox_inches="tight", transparent=False,facecolor="white")