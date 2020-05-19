"""
Parameter settings for aggregation experiment
"""
"""
General settings 
"""
#screen settings
S_WIDTH, S_HEIGHT = 1000, 1000
SCREEN = (S_WIDTH, S_HEIGHT)
#define the number of agents
N_AGENTS = 20
#choose how long to run the simulation
#-1 : infinite, N: finite
FRAMES=-1
#choose swarm type
SWARM = 'Aggregation'


"""
Aggregation class settings
"""

#Define the environment
OBSTACLES = True
OUTSIDE = False
CONVEX = True

#object location
OBJECT_LOC = [S_WIDTH/2., S_HEIGHT/2.]


"""
AggregationAgent class settings
"""

#agents mass
MASS=20
#agent maximum speed
MAX_SPEED = 10.

# Agents Viewing angle
RADIUS_VIEW = 75

# For velocity forces
WANDER_WEIGHT=1.3
MAX_FORCE = 9.

#Wander settings
WANDER_RADIUS = 3.0
WANDER_DIST = 5.0
WANDER_ANGLE = 1.0
