# BoidsPyGame
Implementation of multi-agent simulations in PyGame.

Current example based on the flocking phenomena 

## Contents
1. `main.py` The main file to execute, can specify here the general simulation settings:
    - the number of agents
    - screen size
    - swarm type (which experiment to run)
    
2. **simulation folder** Contains the general simulation design, as well as general multi-agent classes with properties that can be shared across the experiments. 
    - `simulation.py` The main execution loop: the simulation is initialized and ran until the user exits the window.
    - `swarm.py` General swarm properties and updates
    - `agent.py` General agent properties and updates
    - `physical_objects.py` General obstacle properties
    - `helperfunctions.py` General vector transformation functions 

3. **experiments folder** Contains separate folder for each experiment:
    - flocking 
    - aggregation
    - covid


4. **flocking folder** Contains detailed characteristics of a flocking behavior
    - `flock.py` defines the environment of the flock, as well as specific flocking related functions
    - `boid.py` defines a boid, with its possible actions and update rule 
    - **images folder** where the images for the environment and boid design is stored 
    
5. **aggregation folder** Contains detailed characteristics for aggregation behavior

    - `aggreagte.py`defines the environment of the aggregation simuation
    - `cockroach.py` defines the specific agent actions
    
6. **covid folder** Contains experimental set-up for modeling disease spread based on the SIR model
    - `population.py` defines the properties of the population, such as initial infected proportion
    - `person.py` define the properties of each individual 


## How it works
Simply run the main.py file from terminal by specifying the type of swarm to use, and the number of agents 

If you want to change the specific behavior of the given swarm, look into the corresponding swarm folder, and adjust the global variables 


Have fun! 


## Examples
Here are some flocking examples: 

Boids outside a circle object

![Output sample](https://github.com/IlzeAmandaA/BoidsPyGame/blob/master/gifs/boids_outside.gif)


Boids inside a circle object


![Output sample](https://github.com/IlzeAmandaA/BoidsPyGame/blob/master/gifs/boids_inside.gif)
 

Boids inside a convex object

![Output sample](https://github.com/IlzeAmandaA/BoidsPyGame/blob/master/gifs/convexgif.gif)

Here are simple disease spread example:

![Output sample](https://github.com/IlzeAmandaA/BoidsPyGame/blob/master/gifs/covid_randomwalk.gif)
