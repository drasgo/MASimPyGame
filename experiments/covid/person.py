import numpy as np
from simulation.agent import Agent
from simulation import helperfunctions
from experiments.covid import parameters as p


class Person(Agent):
    def __init__(self, pos, v, type, population):
        if type=='I':
            color = p.RED
        elif type=='S':
            color = p.YELLOW
        else:
            color = p.GREEN

        super(Person,self).__init__(pos, v, color=color, mass=p.MASS, max_speed=p.MAX_SPEED,
                                    width=p.WIDTH, height=p.HEIGHT, dT=p.dT)

        self.type = type
        self.population = population
        self.transmittable = False
        self.time_infected_C = 0.
        self.time_possible_I = p.TIME_TRANSMITTABLE+np.random.randint(100)
        self.time_to_recover = 0.
        # self.droplets = 0.


    def update_actions(self):

        force = self.wander(p.WANDER_DIST,p.WANDER_RADIUS,p.WANDER_ANGLE)

        if self.type == 'I':
            self.time_infected += 1
            self.time_to_recover += 1
            if self.time_infected >= (self.time_possible_I):
                self.transmittable = False
            else:
                if np.random.uniform(0, 1)<p.P_COUGH: #person is only infectious if they cough
                    self.transmittable = True
                    # self.droplets += 1.
                else:
                    self.transmittable = False

            if self.time_to_recover >= (p.TIME_RECOVERY + np.random.randint(200)):
                self.type = 'R'
                self.image.fill(p.GREEN)

                #infectious agent can transmit the disease
                #need to implement that this transmitable state is not infinite

        elif self.type == 'S':
            #find infected neighbors
            neighbors = self.population.find_neighbors(self, p.RADIUS_VIEW)
            if len(neighbors):
                if self.population.detect_transmittable(neighbors):
                    if np.random.uniform(0, 1)<p.P_INFECTED:
                        self.type = 'I'
                        self.image.fill(p.RED)


        self.steering +=  helperfunctions.truncate(force/self.mass, p.MAX_FORCE)

