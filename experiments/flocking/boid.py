import pygame
import numpy as np
from simulation import helperfunctions
from simulation.agent import Agent

"""
Specific boid properties and helperfunctions 
"""
#boid mass
MASS = 20

#Viewing angle
RADIUS_VIEW=150

#velocity force
BOID_MAX_FORCE = 9.

#Wander settings
WANDER_RADIUS = 3.0
WANDER_DIST = 5.0
WANDER_ANGLE = 1.0

#weights for velocity forces
COHESION_WEIGHT = 8.
ALIGNMENT_WEIGHT = 2.
SEPERATION_WEIGHT = 7.
WANDER_WEIGHT=1.3

class Boid(Agent):
    def __init__(self, pos, v, flock, image='experiments/flocking/images/normal-boid.png', mass=MASS):
        super(Boid,self).__init__(pos,v,image)

        self.mass = mass
        self.wandering_angle = helperfunctions.randrange(-np.pi, np.pi) #set a random wandering angle
        self.flock = flock


    def update_actions(self):

        #avoid any obstacles in the environment
        for obstacle in self.flock.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle(obstacle.pos, self.flock.object_loc)

        align_force, cohesion_force, separate_force = self.neighbor_forces()

        #combine the vectors in one
        total_force = self.wander() * WANDER_WEIGHT\
                + align_force * ALIGNMENT_WEIGHT \
                + cohesion_force * COHESION_WEIGHT\
                + separate_force * SEPERATION_WEIGHT

        #adjust the direction of the boid
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


    def neighbor_forces(self):

        align_force, cohesion_force, separate_force = np.zeros(2), np.zeros(2), np.zeros(2)

        #find all the neighbors of a boid based on its radius view
        neighbors = self.flock.find_neighbors(self, RADIUS_VIEW)

        #if there are neighbors, estimate the influence of their forces
        if neighbors:
            align_force = self.align(self.flock.find_neighbor_velocity(neighbors))
            cohesion_force = self.cohesion(self.flock.find_neighbor_center(neighbors))
            separate_force = self.flock.find_neighbor_separation(self,neighbors)

        return align_force, cohesion_force, separate_force

    def align(self, neighbor_force):
        """
        Function to align the agent in accordance to neighbor velocity
        :param neighbor_force: np.array(x,y)
        """
        return helperfunctions.normalize(neighbor_force - self.v)

    def cohesion(self, neighbor_center):
        """
        Function to move the agent towards the center of mass of its neighbors
        :param neighbor_rotation: np.array(x,y)
        """
        force = neighbor_center - self.pos
        return helperfunctions.normalize(force - self.v)



