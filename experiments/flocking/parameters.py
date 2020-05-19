"""
Parameter settings to be loaded in the model
"""

"""
General settings 
"""
#screen settings
S_WIDTH, S_HEIGHT = 1000, 1000
SCREEN = (S_WIDTH, S_HEIGHT)
#define the number of agents
N_AGENTS = 30

#choose how long to run the simulation
#-1 : infinite, N: finite
FRAMES=-1

#choose swarm type
SWARM = 'Flock'


"""
Flock class parameters (defines the environment of where the flock to act)
"""
#Define the environment
OBSTACLES = True
OUTSIDE = True
CONVEX = True

#object location
OBJECT_LOC = [S_WIDTH/2., S_HEIGHT/2.]

"""
Boid class parameters
"""

#agents mass
MASS=20
#agent maximum speed and 'duration'
MAX_SPEED = 2.

#Viewing angle
RADIUS_VIEW=150

#velocity force
MAX_FORCE = 9.

#Wander settings
WANDER_RADIUS = 3.0
WANDER_DIST = 5.0
WANDER_ANGLE = 1.0

#weights for velocity forces
COHESION_WEIGHT = 8.
ALIGNMENT_WEIGHT = 2.
SEPERATION_WEIGHT = 7.
WANDER_WEIGHT=1.3










