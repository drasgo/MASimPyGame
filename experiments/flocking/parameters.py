"""
Parameter settings to be loaded in the model
"""

"""
General settings 
"""
#screen settings
S_WIDTH, S_HEIGHT = 1000, 1000
SCREEN = (S_WIDTH, S_HEIGHT)

#choose how long to run the simulation
#-1 : infinite, N: finite
FRAMES=-1

#choose swarm type
SWARM = 'Flock'

#agent size
WIDTH=10
HEIGHT=8

dT=0.2

#object location
OBJECT_LOC = [S_WIDTH/2., S_HEIGHT/2.]


"""
Flock class parameters (defines the environment of where the flock to act)
"""

#define the number of agents
N_AGENTS = 30

#Define the environment
OBSTACLES = True
OUTSIDE = True
CONVEX = True


"""
Boid class parameters
"""

#agents mass
MASS=20

#agent maximum/minimum speed
MAX_SPEED = 7.
MIN_SPEED = 4.

#view of neighbor agents
RADIUS_VIEW=50

#velocity force
MAX_FORCE = 8.

#Wander settings
WANDER_RADIUS = 2.5
WANDER_DIST = 5.0
WANDER_ANGLE = 0.8

#weights for velocity forces
COHESION_WEIGHT = 3.5
ALIGNMENT_WEIGHT = 4.5
SEPERATION_WEIGHT = 6.
WANDER_WEIGHT=0.01










