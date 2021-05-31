import pygame
import numpy as np
from simulation.agent import Agent
from simulation import utils
from experiments.covid.config import config


class Person(Agent):
    def __init__(self, pos, v, type, population, index):
        if type=='I':
            color = config["plot"]["red"]
        elif type=='S':
            color = config["plot"]["orange"]
        else:
            color = config["plot"]["green"]

        super(Person,self).__init__(pos, v, color=color, mass=config["agent"]["mass"], max_speed=config["agent"]["min_speed"],
                                    min_speed=config["agent"]["min_speed"], width=config["agent"]["width"],
                                    height=config["agent"]["height"], dT=config["agent"]["dt"], index=index)
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
            if np.random.uniform(0, 1) < config["person"]["p_cough"]:  # person is only infectious if they cough
                self.transmittable = True
            else:
                self.transmittable = False
                self.color = config["plot"]["red"]
                self.image.fill(config["plot"]["red"])

    def infected(self):
        self.time_infected += 1

        if self.time_infected >= (config["person"]["time_transmittable"] + self.unique_transmit_time):
            self.image.fill(config["plot"]["red"])
            self.transmittable = False
        else:
            self.check_transmittable()

        self.recovery()

    def recovery(self):
        self.time_to_recover += 1
        if self.time_to_recover >= (config["person"]["time_recovery"] + self.unique_recovery_time):
            self.type = 'R'
            self.image.fill(config["plot"]["green"])
            # infectious agent can transmit the disease
            # need to implement that this transmitable state is not infinite

    def susceptible(self):
        #find infected neighbors
        neighbors = self.population.find_neighbors(self, config["person"]["radius_view"])
        if neighbors:
            if self.population.detect_transmittable(neighbors):
                if np.random.uniform(0, 1)<config["person"]["p_infected"]:
                    self.type = 'I'
                    self.image.fill(config["plot"]["red"])

    def droplets_timer(self):
        if self.transmittable:
            self.transmittable_counter += 1
            if self.transmittable_counter == config["person"]["droplets"]:
                self.transmittable = False
                self.transmittable_counter = 0

    def update_actions(self):

        for obstacle in self.population.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()

        force = self.wander(config["person"]["wander_dist"],config["person"]["wander_radius"],config["person"]["wander_angle"])

        if self.type == 'I':
            self.infected()
            self.droplets_timer()

        elif self.type == 'S':
            self.susceptible()

        self.population.datapoints.append(self.type)

        self.steering +=  utils.truncate(force/self.mass, config["person"]["max_force"])
