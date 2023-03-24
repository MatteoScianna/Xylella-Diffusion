# Xylella-Diffusion  - Network and Geospatial analysis of xylella fastidiosa diffusion in Apulia

This project has two main goals: the first one is to provide a visual descriptive analysis of the distribution of olive trees in Apulia; the second is to build a simulation for the diffusion of Xylella fastidiosa between olive trees, analyse different vaccinations strategies and understand how to reduce the impact of a possible epidemic. 

## Map of the olive trees in Apulia 

The geodataframe contains information regarding the position of 61036 olive bunches in Apulia. Each row contains an id of the bunch and a geometry consisting in a multipolygon of the interested area. The following plot shows the distribution of olive bunches in Apulia. 

![alt text](https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/map.png)

Furthermore, we can show some interesting relations between olive bunches and municipalities. In the two following choropleths municipalities are colored according to the number of olive bunches they contain (left) and the density of olive bunches on their territory (right), i.e. $\frac{n_olives}{area}$. 


<img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/olive_trees_xmun.png" width="400" height="400" /> <img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/olive_trees_xmun_scaled.png" width="400" height="400" />

## Degree 

From the geodataframe containing the geometries of different bunches, it is possible to define a network where each node is an olive bunch and two nodes share an edge if the corresponding olive bunches lay at a distance lower than a given threshold. To do so, for each pair of polygons the distance have been calculated considering the nearest points between the two. From that, an edgelist is defined in the classical "source-target-distance" way.
In the following plot, olive bunches are highlighted according to their degree centrality, in a network with threshold equal to 1 km. 

![alt text](https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/degree.png)

The degree of a node could be a useful quantity do determine bunches to vaccinate at priori in order to avoid a massive spread of a disease. There are of course other important quantities, the other one on which we'll focus here is the betweeness centrality of nodes. 

## Betweeness centrality

While for degree centrality the procedure was quite fast, the size of the network made it almost impossible to obtain the betweeness centrality of each olive bunch in the geodataframe. From this, the idea was to create a new network where nodes are municipalities of Apulia region and two nodes, intuitively, share a common edge if they share a common border. First, it was needed to determine, given two municipalities, if they actually were neighbors. Below, an example 

![alt text](https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/intersection_ex.png)

From this, it was easy to create another "source-target" edgelist and define the network of municipalities. 
Having sharply reduced the number of nodes in the network, it is way more agile to calculate the betweeness centrality of each node. Below, a choroplet of the municipalities coloured according to their betweeness centrality. 

![alt text](https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/betweenness_centrality_munic.png)

## Evolution of SIR model 

Now it is time to simulate the possible spread of an epidemic. In this first scenario, a classical SIR model has been chosen, with not a priori vaccination. At each step of the process, a choropleth is procuced highlighting susceptible, infected, and removed nodes. At the end of the project, all these frames are put together in the .gif file you can see below.  

![alt text](https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/spread1.gif)
