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
        super(aggregationAgent,self).__init__(pos,v,image,
                                              mass=p.MASS, max_speed=p.MAX_SPEED,
                                              width=p.WIDTH, height=p.HEIGHT,
                                              dT=p.dT)
        self.aggregation = aggregation
        self.wandering = True
        self.transition_of_state = None
        self.transition_counter = 0



    def change_state(self):
        if self.wandering:
            self.wandering = False
            self.v = np.zeros(2)
            self.steering = np.zeros(2)
        else:
            self.wandering = True
            self.v = self.set_velocity()


    def update_actions(self):
        #avoid any obstacles in the environment

        for area in self.aggregation.objects.sites:
            if self.transition_of_state != None and self.transition_counter < p.NUM_STEPS:
                self.transition_counter = self.transition_counter + 1
            elif self.transition_counter == p.NUM_STEPS:
                self.transition_counter = 0
                self.transition_of_state = None
                self.change_state()
            else:
                collide = pygame.sprite.collide_mask(self, area)
                neighbors = self.aggregation.find_neighbors(self, p.RADIUS_VIEW)
                siteProb = self.siteAreaBehaviour(len(neighbors))
                if bool(collide) and rd.random() < siteProb:
                    # Enter in transition of state
                    if self.wandering:
                        self.transition_of_state = 'Joining'
                    else:
                        self.transition_of_state = 'Leaving'
                    self.transition_counter = 1


        for obstacle in self.aggregation.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide) and self.wandering:
                self.avoid_obstacle(obstacle.pos, self.aggregation.object_loc)

        total_force = self.wander(p.WANDER_DIST,p.WANDER_RADIUS,p.WANDER_ANGLE) * p.WANDER_WEIGHT


        # adjust the direction of the boid
        if self.wandering:
            self.steering += helperfunctions.truncate(total_force / self.mass, p.MAX_FORCE)


    # Defines the behaviour of the agent in a Site
    def siteAreaBehaviour(self, numNeighbors):
        assert numNeighbors >= 0

        baselineProbStop = 0.5

        table1 = {0:0.03, 1:0.42, 2:0.5, 3:0.51}
        table2 = {0:1, 1:1/49, 2:1/424, 3:1/700, 4:1/1306}

        prob = 0

        if self.wandering:
            if numNeighbors > 3:
                numNeighbors = 3
            prob = table1.get(numNeighbors)
        else:
            if numNeighbors > 4:
                numNeighbors = 4
            prob = table2.get(numNeighbors)

        return prob
