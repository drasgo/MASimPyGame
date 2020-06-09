import pygame
import numpy as np
from simulation.agent import Agent
from simulation import helperfunctions
from experiments.covid import parameters as p


class Person(Agent):
    def __init__(self, pos, v, type, population):
        if type=='I':
            color = p.RED
        elif type=='S':
            color = p.ORANGE
        else:
            color = p.GREEN

        super(Person,self).__init__(pos, v, color=color, mass=p.MASS, max_speed=p.MAX_SPEED,
                                    min_speed=p.MIN_SPEED, width=p.WIDTH,
                                    height=p.HEIGHT, dT=p.dT)
        self.color = color
        self.type = type
        self.population = population
        self.transmittable = False
        self.time_infected = 0.
        self.time_to_recover = 0.
        self.unique_transmit_time = np.random.randint(100)
        self.unique_recovery_time = np.random.randint(100)
        self.transmittable_counter = 0.

    def check_transmittable(self):

        if not self.transmittable:
            if np.random.uniform(0, 1) < p.P_COUGH:  # person is only infectious if they cough
                self.transmittable = True
            else:
                self.transmittable = False
                self.color = p.RED
                self.image.fill(p.RED)

    def infected(self):
        self.time_infected += 1

        if self.time_infected >= (p.TIME_TRANSMITTABLE + self.unique_transmit_time):
            self.image.fill(p.RED)
            self.transmittable = False
        else:
            self.check_transmittable()

        self.recovery()

    def recovery(self):
        self.time_to_recover += 1
        if self.time_to_recover >= (p.TIME_RECOVERY + self.unique_recovery_time):
            self.type = 'R'
            self.image.fill(p.GREEN)
            # infectious agent can transmit the disease
            # need to implement that this transmitable state is not infinite

    def susceptible(self):
        #find infected neighbors
        neighbors = self.population.find_neighbors(self, p.RADIUS_VIEW)
        if len(neighbors):
            if self.population.detect_transmittable(neighbors):
                if np.random.uniform(0, 1)<p.P_INFECTED:
                    self.type = 'I'
                    self.image.fill(p.RED)

    def droplets_timer(self):
        if self.transmittable:
            self.transmittable_counter += 1
            if self.transmittable_counter == p.DROPLETS:
                self.transmittable = False
                self.transmittable_counter = 0

    def update_actions(self):

        for obstacle in self.population.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()

        force = self.wander(p.WANDER_DIST,p.WANDER_RADIUS,p.WANDER_ANGLE)

        if self.type == 'I':
            self.infected()
            self.droplets_timer()

        elif self.type == 'S':
            self.susceptible()

        self.population.datapoints.append(self.type)

        self.steering +=  helperfunctions.truncate(force/self.mass, p.MAX_FORCE)
