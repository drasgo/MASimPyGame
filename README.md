# BoidsPyGame
Implementation of flocking in pygame with hallow objects in the environment 

## Contents
1. `main.py` The main file to execute, can specify here the general simulation settings:
    - the number of agents
    - screen size
    - obstacle presence
    - obstacle type 
    - agents inside or outside the obstacle
 
2. `simulation.py` Contains the main execution loop: the simulation is initialized and ran until the user exits the window. 
3. `swarm.py` Contains the possible swarm classes. Currently, only flocking implemented. 
4. `agents.py` Containts the possible agent types to be utilized by the swarm classes. Defines the agent properties and actions
5. `physical_objects.py` Contains a main object class in which a specific obstacle type can be loaded 
6. `functions.py` Contains useful vector transformation functions 

## How it works
Simply run the main.py file from terminal.
If you want to change the behavior of the agents, then you can adjust the global variables defined within the `agents.py` file. 
If you want to change the shape of the obstacles, choose a different file to load in the `physical_objects.py` file.  

Have fun! 
Here are some flocking examples: 

Boids outside a circle object

![Output sample](https://github.com/IlzeAmandaA/BoidsPyGame/blob/master/boids_outside.gif)


Boids inside a circle object


![Output sample](https://github.com/IlzeAmandaA/BoidsPyGame/blob/master/boids_inside.gif)
 

Boids inside a convex object

![Output sample](https://github.com/IlzeAmandaA/BoidsPyGame/blob/master/convexgif.gif)

