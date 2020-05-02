import pygame
import numpy as np
import functions
import random

"""
Python code for agent class definition
Each agent class contains the agent's properties and possible actions to execute based on environmental input 
Currently implemented a Boid class 
"""

#velocity speed and force
BOID_MAX_SPEED = 4.
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

class Boid(pygame.sprite.Sprite):

    def __init__(self, pos=None, v=None, mass=30): #40
        super(Boid,self).__init__()
        if pos is None:
            pos = np.zeros(2)
        if v is None:
            v = self.speedvector()

        self.base_image, self.rect = functions.image_with_rect('normal-boid.png', [10,8])
        self.image = self.base_image
        self.mask = pygame.mask.from_surface(self.image)
        self.mask = self.mask.scale((12, 10))

        self.pos = pos
        self.v = v
        self.mass = mass

        self.steering = np.zeros(2)
        self.wandering_angle = functions.randrange(-np.pi, np.pi) #set a random wandering angle

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self,pos):
        self._pos = pos
        self.rect.center = tuple(pos) #update the rect position as thats actually displayed

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self,v):
        self._v = v
        self._rotate_image()

    def _rotate_image(self):
        """Rotate base image using the velocity and assign to image."""
        angle = -np.rad2deg(np.angle(self.v[0] + 1j * self.v[1])) #using complex number to estimate the angle for rotation
        self.image = pygame.transform.rotate(self.base_image, angle) #rotates the image
        self.rect = self.image.get_rect(center=self.rect.center)

    def speedvector(self):
        angle = np.pi * (2 * np.random.rand() - 1)
        velocity=[random.randrange(1, BOID_MAX_SPEED + 1) * functions.plusminus(),
         random.randrange(1, BOID_MAX_SPEED + 1) * functions.plusminus()]
        velocity *= np.array([np.cos(angle), np.sin(angle)])
        return velocity


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
        self.v = (functions.rotate(functions.normalize(self.v)) * functions.norm(self.v))  # 5.


    def wander(self):
        """
        Function to make the agents to perform random movement
        """
        rands = 2 * np.random.rand() - 1
        cos = np.cos(self.wandering_angle)
        sin = np.sin(self.wandering_angle)
        n_v = functions.normalize(self.v)
        circle_center = n_v * WANDER_DIST
        displacement = np.dot(np.array([[cos, -sin], [sin, cos]]), n_v * WANDER_RADIUS)
        wander_force = circle_center + displacement
        self.steer(wander_force * WANDER_WEIGHT)
        self.wandering_angle += WANDER_ANGLE * rands


    def align(self, neighbor_force):
        """
        Function to align the agent in accordance to neighbor velocity
        :param neighbor_force: np.array(x,y)
        """
        self.steer(functions.normalize(neighbor_force-self.v)*ALIGNMENT_WEIGHT)

    def cohesion(self, neighbor_center):
        """
        Function to move the agent towards the center of mass of its neighbors
        :param neighbor_rotation: np.array(x,y)
        """
        force = neighbor_center - self.pos
        self.steer(functions.normalize(force - self.v)*COHESION_WEIGHT)

    def separate(self, separate_force):
        """
        Function to separate agents from being too close
        :param separate_force: np.array(x,y)
        """
        self.steer(functions.normalize(separate_force) * SEPERATION_WEIGHT)


    def steer(self, force, alt_max=None): #here should all the forces come together
        """Add a force to the current steering force."""
        # limit the steering each time we add a force
        if alt_max is not None:
            self.steering += functions.truncate(force / self.mass, alt_max)
        else:
            self.steering += functions.truncate(
                force / self.mass, BOID_MAX_FORCE)

    def update(self):
        #update the velocity and position of the boid
        self.v = functions.truncate(self.v + self.steering, BOID_MAX_SPEED)
        self.pos += self.v


    def display(self, screen):
        screen.blit(self.image, self.rect)

    def reset_frame(self):
        self.steering = np.zeros(2)

