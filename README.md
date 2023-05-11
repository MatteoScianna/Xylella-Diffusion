# Xylella-Diffusion  - Network and Geospatial analysis of xylella fastidiosa diffusion in Apulia

# Abstract

The impact of the diffusion of Xylella Fastidiosa in Italy and, more in general, in Europe, has been under the spotlight of many different works. The diffusion of this bacterium in Apulia has been a strong damage for the region under many different point of view, since olive trees represent a both source of attraction for tourism and a fundamental asset for one of the main economic incomes for the region: the production of olive oil. 

Understanding the theory behind the diffusion of such a disease may be useful for many different purposes: first of all, since the epidemic is still on, a better knowledge of its diffusion process may lead to better containment methods, in order to avoid the disease to infect and destroy trees in such a deliberate and unopposed way as it happened in the first stage of the contagion; furthermore, it is obvious how epidemiology is a topic of current interest during these recent years, and hence the study and the master of such a disease may be very useful for future epidemics and pandemics.

Hence, this project has several goals: The first is to provide a visual descriptive analysis of the distribution of olive groves in Apulia, highlighting differences in density and amount of trees in different part of the regions and exploiting the network analysis framework in order to address different olive groves and parts of the territory with potentially useful metrics; secondly, two different approaches for the simulation of the diffusion of Xylella Fastidiosa are presented, both based on previous works and with strong differences between them, always with a strong focus on visual representation and geospatial plots. Finally, different potential control strategies are considered, with a focus on their feasibility and their actual impact. 

# Introduction
Xylella fastidiosa is a bacterium that has caused a devastating epidemic in the Apulia region of southern Italy, with significant impacts on the local economy and agricultural sector. Since its first detection in the region in 2013, Xylella fastidiosa has caused extensive damage, leading to the uprooting of millions of trees and threatening the livelihoods of farmers and agricultural communities. 

In order to grasp completely the massive diseases caused by the diffusion of such an epidemic in Apulia, it is necessary to stress that olive farming in the southern province of Puglia accounts for about 40% of Italy’s olive oil production and is of major importance for the regional economy **[11]**. Furthermore, olive trees represent a strong symbol for the identity of the region and its people, with an important aesthetic and touristic value and culturale heritage. Because the landscape is dominated by centennial olive trees and a significant part of the olive crops is associated with family-based agriculture activities, the impact of the epidemic had extreme negative implications not only to olive producers and/or olive industry but has threatened the entire local economy, and the symbolic crop and landscape symbol of this territory. 

Indeed, the local nursery industry has suffered severe economic impacts as a result of the strict restrictions on the marketing and movement of plants for planting produced in the infected areas. Although, the infections have been found to be confined in the southern part of the Apulian region, with the rest of the national territory declared Xylella Fastidiosa free, the whole national nursery industry was affected by the unjustified limitations to importation imposed by some countries concerned about the potential risks of buying plants from Italy. As such, the true economic estimation of the overall damage suffered as a consequence of this Xylella Fastidiosa epidemic is overwhelming and difficult to accurately determine **[10]**.
Without dwelling too much into phitosanitary and epidemiological details, we refer to **[6]** for an exhaustive discussion of the losses in terms of provisioning and cultural services, supporting services and impact in ecosystems, environment and biodiversity. 

Before to go deeper into the actual work, in order to provide a visual idea of the impact of Xylella Fastidiosa on at least the landscape of the territory, the picture below shows the Giant of Alliste monumental olive tree before and after having been infected by Xylella Fastidiosa. Photo by Donato Boscia. 


<img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/Ulivo_Malato.png"> 

# Dataset 

The milestone and first tool that has been exploited in this work is a geodataset with locations of different olive groves, naturally fundamental in order to be able to both perform epidemic scenarios taking into account actual distances between elements and produce visual content as maps for the diffusion. Obatining this dataset was no easy though. The italian portal for the evolution of the Xylella Emergency **[7]** confirms the presence of such a dataset on the website but there is actually no evidence of it really existing. 
Hence, the material was obtained by asking directly to Dr. Giovanni Strona, one of the authors of **[4]**, a paper where analysis similar to the ones presented in this work are performed, which mentioned and exploited the geodataset of the Puglia Portal. Dr. Strona, whom I really have to thank for the kindness and the availability, provided me with a shapefile with information regarding the position of 61036 olive groves in Apulia. Each row contains an id of the grove and a geometry consisting in a multipolygon of the interested area. Every analysis which will be presented further is made starting from this geodataset. 
Of course, since we are dealing not with olive trees but with groves, all analysis performed and methods proposed will be inevitabily a little approximate. Nonetheless, also comparing with other works focusing on the same topic, this situation allows to perform a quite realistic and punctual analysis and simulation of the phenomenon. 

# Exploratory Data Analysis

The goal of this section is to provide a visual descriptive analysis of the dataset and the distribution of olive groves in Apulia region. Starting from a general view of the distribution of the groves in the region, together with their density inside different provinces and municipalities, we'll then focus on a network view of the dataset, in order to extract more information and look at it under a different lens. 

## Map of the olive groves in Apulia 

This first plot shows simply the distribution of the olive groves (green) in Apulia region. Even if of course this map does not provide any other intrinsic information, I think it is a good starting point also in order to have a clear idea of the magnitude of the phenomenon: the region is widely populated by olive trees in almost every part of it, and so it is immediate to understand how much this epidemic is not a finite and limitated phenomenon, but risks to damage and compromise the whole area of Apulia. 

![alt text](https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/map.png)

Furthermore, we can show some interesting relations between olive groves and municipalities. 
In the two following choropleths municipalities are colored according to the number of olive bunches they contain (left) and the density of olive bunches on their territory (right), i.e. $\frac{num.olives}{area}$. 

In the img folder, the file olives_mun.html contains the dynamic version of the second plot, where municipalities are colored according to the density of olive groves and for each municipality it is possible to see the number of the olive groves it contains and its density. 


<img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/olive_trees_xmun.png" width="500" height="400" /> <img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/olive_trees_xmun_scaled.png" width="500" height="400" />

Looking at these two plots, it is immediate to understand, or at least have a confirmation, of why the epidemic of Xylella Fastidiosa spread in the way it had. Of course it is obvious that municipalities with larger area, in a cultural and economic system strongly based on the presence of olive trees, will contain more groves, but when it comes to the density, except for a few municipalities near Bari, the highest levels are in the Salento subregion (southern part of the region, comprehending the province of Lecce and parts of the provinces of Brindisi and Taranto). Linking this information with the fact that the first outbreak of Xylella Fastidiosa was registered in Gallipoli municipality (south of Taranto), it is immediate to understand how easily the epidemic has been able to quickly spread in all the southern part of the region. 

## Network Definition

From the geodataframe containing the geometries of different groves, it is possible to define a network where each node is an olive grove and two nodes share an edge if the corresponding olive grove lay at a distance lower than a given threshold. 
To do so, for each pair of polygons the distance have been calculated considering the nearest points between the two. The two pictures below show an example of this process for the olive groves in the municipality of Lecce. From a randomly chosen target olive bunch, the first choropleth shows the distance of other bunches in the same municipality colored according to their distance. The .gif map shows instead the neighbors of the target olive bunch for different increasing thresholds in meters. 

<img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/lecce_dist.png" width="500" height="300" /> <img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/neighbors.gif" width="500" height="300" />

This process is performed for every couple of olive bunches in the dataset, assigning to it a distance.  From that, an edgelist is defined in the classical "source-target-distance" way and the consequent network is created.

### Degree 

The degree of a node is defined as the number of edges the node has. In other terms, this quantity refers to the number of other nodes our chosen node is connected to. 
In the plot below, the histogram for the degree distribution of the network is presented.

![alt text](https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/degree_distribution.png)

We can then have a more visual idea of the distribution of the nodes in the space, together with their degree. 
In the following plot, olive bunches are highlighted according to their degree centrality, in a network with threshold equal to 1 km. 

![alt text](https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/degree.png)

Note how the degree of the groves in the area of Gallipoli (first initial outbreak of the epidemic) is generally quite high. This is another sympthom on why the epidemic was so fast to spread starting from a position with lots of possible susceptible trees to infect.  

The degree of a node could be a useful quantity do determine groves to eradicate at priori in order to avoid a massive spread of a disease. There are of course other important quantities, the other one on which we'll focus here is the betweeness centrality of nodes. 

### Betweeness centrality

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

where $N_0 = e^{-B}$, $(x,y)$ refers to the target olive grove and $K(x,y) = \Phi(x,y)+a(1-\Phi(x,y))$ is the olive grove infection carrying capacity, where $\Phi(x,y)$ is simply the area of the olive grove divided by the biggest area in the dataset, and $a \in [0, 1]$ is the carrying capacity in nonolive grove habitat, relative to that in olive groves. $A$ and $B$ are constants related to the rate of population growth and the initial proportion of plants infected, fixed at $A=3$ and $B=14.069$, as done in **[1]**. 
Intuitively, according to these equations, starting from a given self level of infection, each year an infected olive grove increases its level of infection $N_{t}$ according to its area, in a resulting value between zero and one. Self level of infection is fundamental for the diffusion of the epidemic to other olive groves, as exposed in the next section. 

### Dispersal

Analyzing the actual diffusion of Xylella in Apulia region, it can be inferred that there has been a conjunction of local low-range dispersal and long-range dispersal, resulting in what is referred to as stratified dispersal **[8]**. 

#### Short-range dispersal

The short-distance dispersal is here modelled with a 2D deterministic exponential kernel, with a mean dispersal distance of $\beta = 100m$, given by

$\hat{k}(x,y) = exp(\frac{-((x-\hat{x})^2+(y-\hat{y})^2)^{1/2}}{\beta})$      **(2)**

In practice, what happens in a simulation scenario is that given an infected olive grove $(\hat{x},\hat{y})$, all olive groves with $\hat{k} \geq p$ gets infected. In the work, $p$ is set equal to $0.2$. 

#### Long-range dispersal 

Modelling long-range dispersal is a more difficult challenge, since lots of external factors, such as wind and cars, may contribute to the long-distance diffusion of the epidemic. Here, an isotropic stochastic dispersal is proposed. To each olive grove a weighted probability of generating a random disperser is assigned, given by $\psi N_{t}(x,y)$, where $\psi \in [0,1]$. Hence, groves with a higher level of self infection will have a higher probability of generating a random dispersal. From this, if $\psi N_{t}(x,y) \geq q$, a random number of dispersers $M \in \{1,...,M_{max}\}$ infect $M$ olive groves according to a 2D Gaussian distribution $N(0,d)$. 
Constants are fixed as $\psi = 1, q = 0.2, M_{max} = 5$ and $d=20km$.

### Simulation

To summarize the whole process, at time $t$ all infected olive groves increase their self level of infection according to equation **(1)**, then for each infected olive grove those neighbors in an average distance of $100 m$ are infected according to equation **(2)** and only for those with a self level of infection greater than a threshold $p$, $M$ dispersers infect random susceptible olive groves according to the 2D Gaussian distribution. 
Note that since the number of disperser for each olive grove is random, the long range diffusion process is completely stochastic. Hence, together with single simulations, it is also useful to investigate the average self infected level of olive groves after five years over simulations. 

The following plots shows an example for one simulation of the process in a time space of 5 years, while the last plot shows the risk map over 100 simulations. All simulations start from a random olive grove in the municipality of Gallipoli. 

<img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/sim_0y.png" width="400" height="500" /> <img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/sim_1y.png" width="400" height="500" />
<img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/sim_2y.png" width="400" height="500" /> <img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/sim_3y.png" width="400" height="500" />
<img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/sim_4y.png" width="400" height="500" /> <img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/diffusion_averaged_5years.png" width="600" height="600" />

### Control Strategy

Since its initial outbreak in Europe, many different strategies have been adopted in order to control the diffusion of Xylella Fastidiosa **[14,15]**. Up to now, no insecticide treatments have been proving working good in the removal of the infection from a plant, and so the main tactic adopted in order to face the epidemic diffusion is the eradication of the tree itself, or its roguing. Starting from the control strategy exposed in **[1]**, here a new model for the eradication of infected trees is presented. 

Starting by the assumption that every olive grove found infected is immediately eradicated, at each time step, before the infection process takes place, each already infected olive grove is labeled with an eradication probability $p_{er}$, given by the linear convex combination of three factors that, intuitively, contribute to put a given grove under the spotlight of a possible infection: 
- The self level of infection of the olive grove itself, already defined as $N_{t}(x,y)$;
- The proportion of olive groves at distance *n* km from the target olive grove that have been previously found infected(and hence eradicated), called $\beta$;
- An "attention level" value $\gamma \in [0,1]$, potentially depending by multiple factors. 

From this, we can define 
$p_{er}^{t}(x,y) = \alpha_1 \cdot N_{t}(x,y)+\alpha_2\cdot\beta_{t}(x,y)+\alpha_3\cdot\gamma$

where $\alpha_1+\alpha_2+\alpha_3= 1$ and $\alpha_i \in [0,1] \forall i$. 

Finally, in order to determine whether a grove found infected will be eradicated, an "avversion" index $\nu \in [0,1]$ is defined. This value represents the effective will on the part of those in charge of eradicating the grove and may depend on social, political and cultural bases, together with availability of tools, period of the year. It may depend also on the position of the grove itself, the aesthetic value of the trees, the stage of infective process the tree is current in, and many other factors. 
At the end, if $p_{er}^{t}(x,y) > \nu$, the grove is eradicated and cannot spread the disease anymore.

In the simulations below, $\alpha_i = \frac{1}{3} \forall i$ and different values of $\nu$ are considered.

<img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/diffusion_5years_vax_0.1.png" width="400" height="500" /> <img src="https://github.com/MatteoScianna/Xylella-Diffusion/blob/main/img/diffusion_5years_vax_0.5.png" width="400" height="500" />



## Network-based simulation model

As already mentioned before, network science framework can be very useful in order to simulate and analyse the diffusion of an epidemic **[12,13]**. In this scenario, it is possible to exploit some well established epidemic diffusion models, such as the SIR and the SI. These models, ruled by sets of differential equations, consider different possible states in which an individual can be during an epidemic and model the evolution of those states up to the end of the outbreak. 

Dr. Strona's et al. paper **[4]**, which we already referred to in the dataset section, explicitely used this framework in order to perform a qualitative analysis for the diffusion of Xylella Fastidiosa in Apulia, a process that we'll replicate now. After all, we already defined a network structure on top of the geodataset in one of the previous sections, in order to grasp some topological insights. Following this already existing network, it is possible to simulate the diffusion of an epidemic and perform an analysis on the same topic but under a different framework. 

An important disclaimer has to be done before to go on. As already stated in **[4]**, the simplicistic diffusion model that will be used does claim to be the most suitable model for Xylella Diffusion. We already defined, in the previous section, a model that tries to resemble as good as possible the real-life scenario, and this of course cannot be the case of an SIR/SI/SIS model. The main goal of this section is to focus of nodes importance, understanding which nodes are more likely to be infected based only on the network topology. 

### SIS Model 

### Simulation 

### Control Strategies

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

**[9]** Kottelenberg, David, et al. "Shape and rate of movement of the invasion front of Xylella fastidiosa spp. pauca in Puglia." Scientific Reports 11.1 (2021): 1061.

**[10]** Saponari, M., et al. "Xylella fastidiosa in olive in Apulia: Where we stand." Phytopathology 109.2 (2019): 175-186.

**[11]** "Istituto di Servizi per il Mercato Agricolo Alimentare."

**[12]** Newman, Mark. Networks. Oxford university press, 2018.

**[13]** Keeling, Matt J., and Ken TD Eames. "Networks and epidemic models." Journal of the royal society interface 2.4 (2005): 295-307.

**[14]** Quetglas, Bàrbara, et al. "Evaluation of Control Strategies for Xylella fastidiosa in the Balearic Islands." Microorganisms 10.12 (2022): 2393.

**[15]** Almeida, Rodrigo PP, et al. "Vector transmission of Xylella fastidiosa: applying fundamental knowledge to generate disease management strategies." Annals of the Entomological Society of America 98.6 (2005): 775-786.
