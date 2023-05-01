# Xylella-Diffusion  - Network and Geospatial analysis of xylella fastidiosa diffusion in Apulia

# Abstract

The impact of the diffusion of Xylella Fastidiosa in Italy and, more in general, in Europe, has been under the spotlight of many different works. The diffusion of this bacterium in Apulia has been a strong damage for the region under many different point of view, since olive trees represent a both source of attraction for tourism and a fundamental asset for one of the main economic incomes for the region: the production of olive oil. 

CAMBIA Hence, this project has two main goals: the first one is to provide a visual descriptive analysis of the distribution of olive trees in Apulia; the second is to build different simulation scenarios for the diffusion of Xylella fastidiosa between olive groves, analyze different vaccinations strategies and provide some possible scenarios on how to reduce the impact of a possible epidemic. 

# Introduction (Historical)

Xylella fastidiosa is a Gram-negative bacterium that infects a broad range of plant species, causing significant economic losses worldwide. In recent years, the bacterium has emerged as a major threat to olive trees in the Apulia region of Italy. Since its first detection in the region in 2013, Xylella fastidiosa has caused extensive damage, leading to the uprooting of millions of trees and threatening the livelihoods of farmers and agricultural communities.
CONTINUE

# Dataset 

The most important tool that has been exploited in this work is a geodataset with locations of different olive groves, naturally fundamental in order to be able to both perform epidemic scenarios taking into account actual distances between elements and produce visual content as maps for the diffusion. Obatining this dataset was no easy though. The italian portal for the evolution of the Xylella Emergency **[7]** confirms the precesence of such a dataset on the website but actually there is no evidence of such a dataset really existing. Hence, the material was obtained directly by asking to Dr. Giovanni Strona, one of the authors of **[4]**, a paper with a focus similar to the one of this work, which mentioned and exploited the geodataset of the Puglia Portal. Dr. Strona, whom I really have to thank for the kindness and the availability, provided a shapefile with information regarding the position of 61036 olive groves in Apulia. Each row contains an id of the bunch and a geometry consisting in a multipolygon of the interested area. Every analysis which will be presented further is made starting from this geodataset. 


# Exploratory Data Analysis

## Map of the olive trees in Apulia 


![alt text](https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/map.png)

Furthermore, we can show some interesting relations between olive bunches and municipalities. In the two following choropleths municipalities are colored according to the number of olive bunches they contain (left) and the density of olive bunches on their territory (right), i.e. $\frac{num.olives}{area}$. 
Below, a dynamic plot for the density of olive trees per municipality.


<img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/olive_trees_xmun.png" width="500" height="400" /> <img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/olive_trees_xmun_scaled.png" width="500" height="400" />
<img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/olives_mun.html" width="500" height="400">

# Network Definition

## Degree 

From the geodataframe containing the geometries of different bunches, it is possible to define a network where each node is an olive bunch and two nodes share an edge if the corresponding olive bunches lay at a distance lower than a given threshold. To do so, for each pair of polygons the distance have been calculated considering the nearest points between the two. The two pictures below show an example of this process for the olive bunches in the municipality of Lecce. From a randomly chosen target olive bunch, the first choropleth shows the distance of other bunches in the same municipality colored according to their distance. The .gif map shows instead the neighbors of the target olive bunch for different increasing thresholds in meters. 

![alt text](https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/lecce_dist.png)
![alt text](https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/neighbors.gif)

This process is performed for every couple of olive bunches in the dataset, assigning to it a distance.  
From that, an edgelist is defined in the classical "source-target-distance" way.
In the plot below, the histogram for the degree distribution of the network is presented.

![alt text](https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/degree_distribution.png)

We can then have a more visual idea of the distribution of the nodes in the space, together with their degree. 
In the following plot, olive bunches are highlighted according to their degree centrality, in a network with threshold equal to 1 km. 

![alt text](https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/degree.png)

The degree of a node could be a useful quantity do determine bunches to vaccinate at priori in order to avoid a massive spread of a disease. There are of course other important quantities, the other one on which we'll focus here is the betweeness centrality of nodes. 

## Betweeness centrality

While for degree centrality the procedure was quite fast, the size of the network made it almost impossible to obtain the betweeness centrality of each olive bunch in the geodataframe. From this, the idea was to create a new network where nodes are municipalities of Apulia region and two nodes, intuitively, share a common edge if they share a common border. First, it was needed to determine, given two municipalities, if they actually were neighbors. Below, an example 

![alt text](https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/intersection_ex.png)

From this, it was easy to create another "source-target" edgelist and define the network of municipalities. 
Having sharply reduced the number of nodes in the network, it is way more agile to calculate the betweeness centrality of each node. Below, a choroplet of the municipalities coloured according to their betweeness centrality. 

![alt text](https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/betweenness_centrality_munic.png)

# Models for Epidemic Diffusion

As already mentioned before, grasping and modelling the evolution of Xylella diffusion is a difficult process for several reasons, the main one resulting in the vector of diffusion being an insect, resulting in a huge level of unpredictability and uncertainty. Nonetheless, several works tried to obtain reliable and realistic models for the diffusion of the epidemic. Here, two main frameworks are presented. 

##  Spatially-Explicit Simulation Model

This model follows the already existing work presented in **[1]** with one substantial differenct: while in the cited paper the main unit of work were grid cells of 1 $km^2$ in which the targed region was divided, here we refer directly to the actual olive groves to perform the simulation. Hence, the evolution of the epidemic diffusion, on a yearly temporal scale, is divided into three different phases.

### Self level of infection 

To model the local infection growth of a single olive grove, a discrete variant of Gompertz equation is considered, as

$N_{t+1}(x,y) = K(x,y)(\frac{N_{t}(x,y)}{K(x,y)})^{e^{-A}}$     **(1)**

where $N_0$ = e^{-B}$, $(x,y)$ refers to the target olive grove and $K(x,y) = \Phi(x,y)+a(1-\Phi(x,y))$ is the olive grove infection carrying capacity, where $\Phi(x,y)$ is simply the area of the olive grove, and $a \in [0, 1]$ is the carrying capacity in nonolive grove habitat, relative to that in olive groves. $A$ and $B$ are constants related to the rate of population growth and the initial proportion of plants infected, fixed at $A=3$ and $B=14.069$, as done in **[1]**. 
Intuitively, according to these equations, starting from a given self level of infection, each year an infected olive grove increases its level of infection $N_{t}$ according to its area, in a resulting value between zero and one. Self level of infection is fundamental for the diffusion of the epidemic to other olive groves, as exposed in the next section. 

### Dispersal

Analyzing the actual diffusion of Xylella in Apulia region, it can be inferred that there has been a conjunction of local low-range dispersal and long-range dispersal, resulting in what is referred to as stratified dispersal **[8]**. 

#### Short-range dispersal

The short-distance dispersal is here modelled with a 2D deterministic exponential kernel, with a mean dispersal distance of $\beta = 100m$, given by

$\hat{k}(x,y) = exp(\frac{-((x-\hat{x})^2+(y-\hat{y})^2)^{1/2}}{\beta})$      **(2)**

In practice, what happens in a simulation scenario is that given an infected olive grove $(\hat{x},\hat{y})$, all olive groves with \hat{k} \geq p$ gets infected. In the work, $p$ is set equal to $0.2$. 

#### Long-range dispersal 

Modelling long-range dispersal is a more difficult challenge, since lots of external factors, such as wind and cars, may contribute to the long-distance diffusion of the epidemic. Here, an isotropic stochastic dispersal is proposed. To each olive grove a weighted probability of generating a random disperser is assigned, given by $\roN_{t}}(x,y)$, where $\ro \in [0,1]$. Hence, groves with a higher level of self infection will have a higher probability of generating a random dispersal. From this, if $\roN_{t}(x,y) \geq q$, a random number of dispersers $M \in {1,...,M_{max}}$ infect $M$ olive groves according to a 2D Gaussian distribution $N(0,d)$. 
Constants are fixed as $\ro = 1, q = 0.2, M_{max} = 5$ and $d=20km$.

To summarize the whole process, at time $t$ all infected olive groves increase their self level of infection according to equation **(1)**, then for each infected olive grove those neighbors in an average distance of $100 m$ are infected according to equation **(2)** and only for those with a self level of infection greater than a threshold $p$, $M$ disperser**$^1$** infect random susceptible olive groves according to the 2D Gaussian distribution. 

**$^1$** Note that since the number of disperser for each olive grove is random, the long range diffusion process is completely stochastic.


## Evolution of SIR model 

Now it is time to simulate the possible spread of an epidemic. In this first scenario, a classical SIR model has been chosen, with not a priori vaccination. At each step of the process, a choropleth is procuced highlighting susceptible, infected, and removed nodes. At the end of the project, all these frames are put together in the .gif file you can see below.  

![alt text](https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/spread1.gif)

# Vaccination Strategies

## Degree-based Vaccination
One possible way to vaccinate nodes is according to their degree. In particular, we start removing from the graph nodes with higher degree and we go on until all nodes are removed. We are interested in the evolution of the size of the giant component of the graph according to different percentages of nodes removed in this way. 
This process is shown in the plots below, respectively with a simple scatterplot and with a map, where nodes in red are the ones belonging to the giant component. 
<img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/evolution_S_degree.png" width="500" height="400" /> <img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/biggest_comp.gif" width="500" height="400" />

# Simulations and Results

# Conclusion and Further Works

# References

**[1]** White, Steven M., et al. "Modelling the spread and control of Xylella fastidiosa in the early stages of invasion in Apulia, Italy." Biological Invasions 19 (2017): 1825-1837

**[2]** White, Steven M., et al. "Estimating the epidemiology of emerging Xylella fastidiosa outbreaks in olives." Plant Pathology 69.8 (2020): 1403-1413.

**[3]** Brunetti, Matteo, et al. "A mathematical model for Xylella fastidiosa epidemics in the Mediterranean regions. Promoting good agronomic practices for their effective control." Ecological Modelling 432 (2020): 109204.

**[4]** Strona, Giovanni, Corrie Jacobien Carstens, and Pieter SA Beck. "Network analysis reveals why Xylella fastidiosa will persist in Europe." Scientific Reports 7.1 (2017): 71.

**[5]** M. RAMAZZOTTI, “Insights on a founder effect: the case of <em>Xylella fastidiosa</em> in the Salento area of Apulia, Italy”, Phytopathol. Mediterr., vol. 57, no. 1, pp. 8–25, Feb. 2018.

**[6]** Ali, Beshir M., Wopke van der Werf, and Alfons Oude Lansink. "Assessment of the environmental impacts of Xylella fastidiosa subsp. pauca in Puglia." Crop Protection 142 (2021): 105519.

**[7]** http://www.emergenzaxylella.it/portal/portale_gestione_agricoltura

**[8]** Shigesada, Nanako, Kohkichi Kawasaki, and Yasuhiko Takeda. "Modeling stratified diffusion in biological invasions." The American Naturalist 146.2 (1995): 229-251.
