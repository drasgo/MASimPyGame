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
RADIUS_VIEW = 30

# For velocity forces
WANDER_WEIGHT=1.3
MAX_FORCE = 9.

#Wander settings
WANDER_RADIUS = 3.0
WANDER_DIST = 5.0
WANDER_ANGLE = 1.0

# Changing of state
NUM_STEPS = 3

"""
The testing scenarios recommended by Eliseo
"""

def experiment1(screensize, outside): # Different sizes | Different locations
    area_loc1 = [55 + screensize[0]/4., 55 + screensize[1]/3.]
    area_loc2 = [screensize[0]/2., screensize[1]/2.]


    if outside:
        scale1 = [140,140]
        scale2 = [180,180]
    else:
        scale1 = [110,110]
        scale2 = [140,140]

    bigB1 = False
    bigB2 = True

    return area_loc1, scale1, bigB1, area_loc2, scale2, bigB2


def experiment2(screensize, outside): # Same size | Big | Different locations
    area_loc1 = [55 + screensize[0]/4., 55 + screensize[1]/3.]
    area_loc2 = [screensize[0]/2., screensize[1]/2.]

    if outside:
        scale1 = [180,180]
        scale2 = [180,180]
    else:
        scale1 = [140,140]
        scale2 = [140,140]

    bigB1 = True
    bigB2 = True

    return area_loc1, scale1, bigB1, area_loc2, scale2, bigB2

def experiment3(screensize, outside): # Different sizes |  Symmetric locations
    area_loc1 = [screensize[0]/2. - screensize[0]/4., screensize[1]/2.]
    area_loc2 = [screensize[0]/4. + screensize[0]/2., screensize[1]/2.]

    if outside:
        scale1 = [140,140]
        scale2 = [180,180]
    else:
        scale1 = [110,110]
        scale2 = [140,140]

    bigB1 = False
    bigB2 = True

    return area_loc1, scale1, bigB1, area_loc2, scale2, bigB2


def experiment4(screensize, outside): # Equal size |  Symmetric locations
    area_loc1 = [screensize[0]/2. - screensize[0]/4.4, screensize[1]/2.]
    area_loc2 = [screensize[0]/4.4 + screensize[0]/2., screensize[1]/2.]

    if outside:
        scale1 = [140,140]
        scale2 = [180,180]
    else:
        scale1 = [110,110]
        scale2 = [110,110]

    bigB1 = False
    bigB2 = False

    return area_loc1, scale1, bigB1, area_loc2, scale2, bigB2
