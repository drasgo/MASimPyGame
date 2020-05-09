# BoidsPyGame
Implementation of multi-agent simulations in PyGame.

Current example based on the flocking phenomena 

## Contents
1. `main.py` The main file to execute, can specify here the general simulation settings:
    - the number of agents
    - screen size
    - swarm type (which experiment to run)

 
2. `simulation.py` Contains the main execution loop: the simulation is initialized and ran until the user exits the window.

3. In the folder experiments, you can find the general multi-agent classes shared across all experiments:
    - `swarm.py` General swarm properties and updates
    - `agent.py` General agent properties and updates
    - `physical_objects.py` General obstacle properties
    - `helperfunctions.py` General vector transformation functions 

Each experiment is defined in a separate folder: flocking, aggregation and etc.

4. Flocking folder contains detailed characteristics for flocking behavior
    - `flock.py` defines the environment of the flock, as well as specific flocking related functions
    - `boid.py` defines a boid, with its possible actions and update rule 
    - images Folder where the images for the environment and boid design is stored 
    
5. Aggregation folder contains detailed characteristics for aggregation behavior
   
    TO BE WRITTEN BY ANDRE
    - `aggreagte.py`
    - `cockroach.py`


## How it works
Simply run the main.py file from terminal by specifying the type of swarm to use, and the number of agents 

If you want the specific behavior of the given swarm, look into the corresponding swarm folder, and adjust the global variables 


Have fun! 


## Examples
Here are some flocking examples: 

Boids outside a circle object

![Output sample](https://github.com/IlzeAmandaA/BoidsPyGame/blob/master/gifs/boids_outside.gif)


Boids inside a circle object


![Output sample](https://github.com/IlzeAmandaA/BoidsPyGame/blob/master/gifs/boids_inside.gif)
 

Boids inside a convex object

![Output sample](https://github.com/IlzeAmandaA/BoidsPyGame/blob/master/gifs/convexgif.gif)

