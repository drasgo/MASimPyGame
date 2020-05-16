from simulation.agent import Agent
from simulation import helperfunctions
import numpy as np

#wandering definition
WANDER_RADIUS = 3.0
WANDER_DIST = 0.5
WANDER_ANGLE = 2.0

MAX_FORCE= 0.4

MASS=60

#transmition and susceptibility probabilities
P_COUGH=0.3
P_INFECTED = 0.8
RADIUS_VIEW=50

#colors
RED=(255, 0, 0 )
YELLOW= (255,255,0)
GREEN=(0, 255, 0 )


class Person(Agent):
    def __init__(self, pos, v, type, population):
        if type=='I':
            color = RED #red
        elif type=='S':
            color = YELLOW
        else:
            color = GREEN

        super(Person,self).__init__(pos, v, color=color)

        self.wandering_angle = helperfunctions.randrange(-np.pi, np.pi)
        self.type = type
        self.population = population
        self.mass = MASS
        self.transmittable = False


    def update_actions(self):

        force = self.random_walk()

        if self.type == 'I':
            if np.random.uniform(0, 1)<P_COUGH:
                self.transmittable = True
                #infectious agent can transmit the disease
                #need to implement that this transmitable state is not infinite

        elif self.type == 'S':
            #find infected neighbors
            neighbors = self.population.find_neighbors(self, RADIUS_VIEW)
            if len(neighbors):
                if self.population.detect_transmittable(self):
                    if np.random.uniform(0, 1)<P_INFECTED:
                        self.type = 'I'
                        self.image.fill(RED)







        self.steering +=  helperfunctions.truncate(self.random_walk()/self.mass, MAX_FORCE)


    def random_walk(self):
        """
        Function to make the agents to perform random movement
        """
        rands = 2 * np.random.rand() - 1
        cos = np.cos(self.wandering_angle)
        sin = np.sin(self.wandering_angle)
        n_v = helperfunctions.normalize(self.v)
        circle_center = n_v * WANDER_DIST
        displacement = np.dot(np.array([[cos, -sin], [sin, cos]]), n_v * WANDER_RADIUS)
        wander_force = circle_center + displacement
        self.wandering_angle += WANDER_ANGLE * rands
        return wander_force

