"""
Parameter settings for covid experiment
"""
"""
General settings 
"""
#screen settings
S_WIDTH, S_HEIGHT = 1000, 1000
SCREEN = (S_WIDTH, S_HEIGHT)
#define the number of agents
N_AGENTS = 80

#choose how long to run the simulation
#-1 : infinite, N: finite
FRAMES=-1

#choose swarm type
SWARM = 'Covid'

#agent size
WIDTH=5
HEIGHT=5

dT=1


"""
Population class settings
"""
#initial condition probabilities
INFECTED = 0.01

"""
Person class settings
"""

#agents mass
MASS=50

#agent maximum speed and 'duration'
MAX_SPEED = 2.


MAX_FORCE= 0.6
RADIUS_VIEW=50

#wandering definition
WANDER_RADIUS = 3.0
WANDER_DIST = 0.5
WANDER_ANGLE = 2.0

#transmition and susceptibility probabilities
P_COUGH=0.8
P_INFECTED = 0.9
TIME_TRANSMITTABLE = 1200 #comparison to 1 week
TIME_RECOVERY = 1400 #comparison to 2 weeks

#colors
RED=(255, 0, 0 )
YELLOW= (255,255,0)
GREEN=(0, 0, 0 )






