import pygame
import random as rd
import numpy as np
from simulation import helperfunctions
from simulation.agent import Agent

"""
Specific the aggregation agent properties and actions 
"""

#boid mass
MASS = 20

# Agents Viewing angle
RADIUS_VIEW = 75

#Wander settings
WANDER_RADIUS = 3.0
WANDER_DIST = 5.0
WANDER_ANGLE = 1.0

# For velocity forces
WANDER_WEIGHT=1.3
BOID_MAX_FORCE = 9.


class aggregationAgent(Agent):
    def __init__(self, pos, v, aggregation, mass = MASS, image='experiments/aggregation/images/color_ant.png'):
        super(aggregationAgent,self).__init__(pos,v,image)
        self.aggregation = aggregation
        self.wandering = True
        self.wandering_angle = helperfunctions.randrange(-np.pi, np.pi)  # set a random wandering angle
        self.mass = mass

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
            neighbors = self.aggregation.find_neighbors(self, RADIUS_VIEW)
            if bool(collide) and prob < self.siteAreaBehaviour(len(neighbors)):
                if self.wandering:
                    self.change_state_stop()
                elif numberWanderingAgents == 0:
                    self.change_state_leave()

        for obstacle in self.aggregation.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle(obstacle.pos, self.aggregation.object_loc)

        total_force = self.wander() * WANDER_WEIGHT

        # adjust the direction of the boid
        self.steering += helperfunctions.truncate(total_force / self.mass, BOID_MAX_FORCE)


    def wander(self):
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


    #actions
    def avoid_obstacle(self, obstacle_center, obstacle_outside):
        """
        Function to avoid obstacles
        need to take into account whether agents inside/outside the obstacle
        moves the agent away from the boarder by distance equivalent to its size
        :param obstacle_center: tuple (int,int), the center coordinates of the obstacle
        :param obstacle_outside: boolean, defines whether the agents are inside or outside of the obstacle
        """
        x,y = self.mask.get_size() #get the size of the boid
        x_ob, y_ob = obstacle_center

        if obstacle_outside: #agents outside the obstacle
            if self.pos[0] >= x_ob:
                self.pos[0] += x
            else:
                self.pos[0] -= x

            if self.pos[1] >= y_ob:
                self.pos[1] += y
            else:
                self.pos[1] -= y
        else:  #agents inside the obstacle:
            if self.pos[0] <= x_ob:
                self.pos[0] +=x
            else:
                self.pos[0] -=x

            if self.pos[1] <= y_ob:
                self.pos[1] += y
            else:
                self.pos[1] -= y

        #adjust the velocity by rotating it around
        self.v = (helperfunctions.rotate(helperfunctions.normalize(self.v)) * helperfunctions.norm(self.v))  # 5.


    # Defines the behaviour of the agent in a Site
    def siteAreaBehaviour(self, numNeighbors):
        assert numNeighbors >= 0

        baselineProbStop = 0.5
        baselineProbLeave = 0.5

        jFactor = 0.02
        lFactor = 0.04

        if self.wandering:
            prob = baselineProbStop + (jFactor * numNeighbors)
        else:
            prob = baselineProbLeave - (lFactor * numNeighbors)

        prob = max(prob, 0)

        return prob


    def update(self):
        if self.wandering:
            super(aggregationAgent, self).update()