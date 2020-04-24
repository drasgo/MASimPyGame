# BoidsPyGame
Implementation of flocking in pygame with hallow objects in the environment 

# Contents
Each individual agent specifications are coded in the file agents.py
The overall swarm behavior (in this case flocking) is specified in the file swarm.py
The file functions.py contains supporting functions for vector computations
The simulations.py file contains the general set-up of the environment (initialization and the game loop)
Lastly, the file main.py is the execution file. 

# How it works
Simply run the main.py file, where you can specify:
- Display size
- Number of Boids
- Whether to include and obstacle, and if 'True', then whether to position the birds inside or outside
- Selection of boid actions (wander, align, separate, cohere) 

If you want to change the speed of the birds, then you have to change the global variables (BOID_MAX_SPEED & BOID_MAX_FORCE) in agent.py code. 

# Bugs
Sometimes the agent gets stuck at the corners of the object --> still to be fully fixed 

Have fun! 
Here is how it looks:
Boids Outside the object


![Output sample](https://github.com/IlzeAmandaA/BoidsPyGame/blob/master/boids_outside.gif)


Boids Inside the object


![Output sample](https://github.com/IlzeAmandaA/BoidsPyGame/blob/master/boids_inside.gif)
 

