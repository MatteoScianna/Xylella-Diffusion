# Xylella-Diffusion  - Network and Geospatial analysis of xylella fastidiosa diffusion in Apulia

# Abstract

The impact of the diffusion of Xylella Fastidiosa in Italy and, more in general, in Europe, has been under the spotlight of many different works. --Quick recap of the evolution of xylella in puglia, number of trees dead and evolution in production of olive oil. 
This project has two main goals: the first one is to provide a visual descriptive analysis of the distribution of olive trees in Apulia; the second is to build a simulation for the diffusion of Xylella fastidiosa between olive trees, analyze different vaccinations strategies and provide some possible scenarios on how to reduce the impact of a possible epidemic. 

# Introduction (Historical)

blablabla

# Dataset 

How was the dataset obtained, what does it contain. 

# Exploratory Data Analysis

## Map of the olive trees in Apulia 

The geodataframe contains information regarding the position of 61036 olive bunches in Apulia. Each row contains an id of the bunch and a geometry consisting in a multipolygon of the interested area. The following plot shows the distribution of olive bunches in Apulia. 

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

# Epidemic Models

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

[1] White, Steven M., et al. "Modelling the spread and control of Xylella fastidiosa in the early stages of invasion in Apulia, Italy." Biological Invasions 19 (2017): 1825-1837

[2] White, Steven M., et al. "Estimating the epidemiology of emerging Xylella fastidiosa outbreaks in olives." Plant Pathology 69.8 (2020): 1403-1413.

[3] Brunetti, Matteo, et al. "A mathematical model for Xylella fastidiosa epidemics in the Mediterranean regions. Promoting good agronomic practices for their effective control." Ecological Modelling 432 (2020): 109204.

[4] Strona, Giovanni, Corrie Jacobien Carstens, and Pieter SA Beck. "Network analysis reveals why Xylella fastidiosa will persist in Europe." Scientific Reports 7.1 (2017): 71.


