import pygame
import random as rd
import numpy as np
from simulation import helperfunctions
from simulation.agent import Agent
from experiments.aggregation import parameters as p

"""
Specific the aggregation agent properties and actions
"""


class aggregationAgent(Agent):
    def __init__(self, pos, v, aggregation, image='experiments/aggregation/images/color_ant.png'):
        super(aggregationAgent,self).__init__(pos,v,image, mass=p.MASS, max_speed=p.MAX_SPEED)
        self.aggregation = aggregation
        self.wandering = True

    def change_state_stop(self):
        self.wandering = False
        self.v = np.zeros(2)


    def change_state_leave(self):
        self.wandering = True
        self.v = self.set_velocity()


    def get_state(self):
        """
        :return: the agent's boolean current state (wandering or in a aggregation)
        """
        return self.wandering

    def update_actions(self, numberWanderingAgents):
        #avoid any obstacles in the environment

        for area in self.aggregation.objects.sites:
            collide = pygame.sprite.collide_mask(self, area)
            prob = rd.random()
            neighbors = self.aggregation.find_neighbors(self, p.RADIUS_VIEW)
            if bool(collide) and prob < self.siteAreaBehaviour(len(neighbors)):
                if self.wandering:
                    self.change_state_stop()
                elif numberWanderingAgents == 0:
                    self.change_state_leave()

        for obstacle in self.aggregation.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle(obstacle.pos, self.aggregation.object_loc)

        total_force = self.wander(p.WANDER_DIST,p.WANDER_RADIUS,p.WANDER_ANGLE) * p.WANDER_WEIGHT

        # adjust the direction of the boid
        self.steering += helperfunctions.truncate(total_force / self.mass, p.MAX_FORCE)



    # Defines the behaviour of the agent in a Site
    def siteAreaBehaviour(self, numNeighbors):
        assert numNeighbors >= 0

        baselineProbStop = 0.5
        baselineProbLeave = 0.2

        jFactor = 0.02
        lFactor = 0.03

        if self.wandering:
            prob = baselineProbStop + (jFactor * numNeighbors)
        else:
            prob = baselineProbLeave - (lFactor * numNeighbors)

        prob = max(prob, 0)

        return prob


    def update(self):
        if self.wandering:
            super(aggregationAgent, self).update()
