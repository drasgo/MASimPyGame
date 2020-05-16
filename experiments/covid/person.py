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
P_COUGH=0.4
P_INFECTED = 0.8
RADIUS_VIEW=50
TIME_TRANSMITTABLE = 800 #comparison to 1 week
TIME_RECOVERY = 1600 #comparison to 2 weeks

#colors
RED=(255, 0, 0 )
YELLOW= (255,255,0)
GREEN=(0, 0, 0 )


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
        self.time_infected = 0.
        self.time_to_recover = 0.


    def update_actions(self):

        force = self.random_walk()

        if self.type == 'I':
            self.time_infected += 1
            self.time_to_recover += 1
            if self.time_infected >= (TIME_TRANSMITTABLE+np.random.randint(100)):
                self.transmittable = False
            else:
                if np.random.uniform(0, 1)<P_COUGH: #person is only infectious if they cough
                    self.transmittable = True
                else:
                    self.transmittable = False

            if self.time_to_recover >= (TIME_RECOVERY + np.random.randint(200)):
                self.type = 'R'
                self.image.fill(GREEN)

                #infectious agent can transmit the disease
                #need to implement that this transmitable state is not infinite

        elif self.type == 'S':
            #find infected neighbors
            neighbors = self.population.find_neighbors(self, RADIUS_VIEW)
            if len(neighbors):
                if self.population.detect_transmittable(neighbors):
                    if np.random.uniform(0, 1)<P_INFECTED:
                        self.type = 'I'
                        self.image.fill(RED)


        self.steering +=  helperfunctions.truncate(force/self.mass, MAX_FORCE)


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

