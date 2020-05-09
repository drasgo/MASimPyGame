import pygame
import numpy as np
from experiments import helperfunctions
from experiments.agent import Agent

"""
Specific boid properties and helperfunctions 
"""
#boid mass
MASS = 30

#velocity force
BOID_MAX_FORCE = 5.

#Wander settings
WANDER_RADIUS = 3.0
WANDER_DIST = 5.0
WANDER_ANGLE = 1.0

#weights for velocity forces
COHESION_WEIGHT = 10.9
ALIGNMENT_WEIGHT = 3.5
SEPERATION_WEIGHT = 7.5
WANDER_WEIGHT=1.3

class Boid(Agent):
    def __init__(self, pos, v, image='experiments/flocking/images/normal-boid.png', mass=MASS):
        super(Boid,self).__init__(pos,v,image)

        self.mass = mass
        self.wandering_angle = helperfunctions.randrange(-np.pi, np.pi) #set a random wandering angle

    def update_actions(self, obstacles, object_loc, align, cohere, separate):
        for obstacle in obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle(obstacle.pos, object_loc)


        total_force = self.wander() * WANDER_WEIGHT\
                + self.align(align) * ALIGNMENT_WEIGHT \
                + self.cohesion(cohere) * COHESION_WEIGHT\
                + self.separate(separate) * SEPERATION_WEIGHT

        self.steering += helperfunctions.truncate(total_force / self.mass, BOID_MAX_FORCE)

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
        # self.steer(wander_force * WANDER_WEIGHT)



    def align(self, neighbor_force):
        """
        Function to align the agent in accordance to neighbor velocity
        :param neighbor_force: np.array(x,y)
        """
        return helperfunctions.normalize(neighbor_force-self.v)
        # self.steer(helperfunctions.normalize(neighbor_force-self.v)*ALIGNMENT_WEIGHT)

    def cohesion(self, neighbor_center):
        """
        Function to move the agent towards the center of mass of its neighbors
        :param neighbor_rotation: np.array(x,y)
        """
        force = neighbor_center - self.pos
        return helperfunctions.normalize(force - self.v)
        # self.steer(helperfunctions.normalize(force - self.v)*COHESION_WEIGHT)

    def separate(self, separate_force):
        """
        Function to separate agents from being too close
        :param separate_force: np.array(x,y)
        """
        return helperfunctions.normalize(separate_force)
        # self.steer(helperfunctions.normalize(separate_force) * SEPERATION_WEIGHT)


