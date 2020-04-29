# BoidsPyGame
Implementation of flocking in pygame with hallow objects in the environment 

## Contents
1. `main.py` The main file to execute, can specify here:
    - the number of boids
    - screen size
    - forces to execute (wander, align, separate, cohere) 
    - obstacle presence
    - obstacle type 
    - boids inside or outside the obstacle
    - to display screen or not 
    
2. `simulation.py` Contains the main execution loop: the game is initialized and ran until the user exits the window
3. `swarm.py` Defines the swarm behavior (weights for each force applied), as well as the update sequence
4. `agents.py` Defines the properties of boids (mass of a boid) and obstacles. 
5. `functions.py` Contains useful vector transformation functions 

## How it works
Simply run the main.py file from terminal 

## Bugs
Sometimes the agent gets stuck at the corners of the object --> still to be fully fixed 

Have fun! 
Here is how it looks:

Boids outside a circle object

![Output sample](https://github.com/IlzeAmandaA/BoidsPyGame/blob/master/boids_outside.gif)


Boids inside a circle object


![Output sample](https://github.com/IlzeAmandaA/BoidsPyGame/blob/master/boids_inside.gif)
 

Boids inside a convex object

![Output sample](https://github.com/IlzeAmandaA/BoidsPyGame/blob/master/convexgif.gif)

