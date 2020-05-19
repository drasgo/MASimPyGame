import numpy as np
import random
import pygame
from simulation import helperfunctions


"""
General agent properties, which are common across all types of agents 
"""
#agent size
WIDTH=10
HEIGHT=8

dT=1.

#defines general agent properties
class Agent(pygame.sprite.Sprite): #super class
    def __init__(self, pos=None, v=None, image=None, color=None, mass=None, max_speed=None):
        super(Agent, self).__init__()

        self.image_file = image
        if self.image_file != None: #load image from file
            self.base_image, self.rect = helperfunctions.image_with_rect(self.image_file, [WIDTH, HEIGHT])
            self.image = self.base_image
            self.mask = pygame.mask.from_surface(self.image)
            self.mask = self.mask.scale((12, 10))

        else: #draw an agent
            self.image = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)

        self.mass = mass
        self.max_speed = max_speed
        self.wandering_angle = helperfunctions.randrange(-np.pi, np.pi)  # set a random wandering angle

        self.steering = np.zeros(2)
        self.pos = np.zeros(2) if pos is None else pos
        self.v = self.set_velocity() if v is None else v

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos
        self.rect.center = tuple(pos)  # update the rect position as thats actually displayed

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, v):
        self._v = v
        if self.image_file: self._rotate_image()

    def _rotate_image(self):
        """Rotate base image using the velocity and assign to image."""
        angle = -np.rad2deg(np.angle(self.v[0] + 1j * self.v[1])) #using complex number to estimate the angle for rotation
        self.image = pygame.transform.rotate(self.base_image, angle) #rotates the image
        self.rect = self.image.get_rect(center=self.rect.center)


    def set_velocity(self):
        angle = np.pi * (2 * np.random.rand() - 1)
        velocity = [random.randrange(1, self.max_speed + 1) * helperfunctions.plusminus(),
                    random.randrange(1, self.max_speed + 1) * helperfunctions.plusminus()]
        velocity *= np.array([np.cos(angle), np.sin(angle)])
        return velocity

    def wander(self, wander_dist, wander_radius, wander_angle):
        """
        Function to make the agents to perform random movement
        """
        rands = 2 * np.random.rand() - 1
        cos = np.cos(self.wandering_angle)
        sin = np.sin(self.wandering_angle)
        n_v = helperfunctions.normalize(self.v)
        circle_center = n_v * wander_dist
        displacement = np.dot(np.array([[cos, -sin], [sin, cos]]), n_v * wander_radius)
        wander_force = circle_center + displacement
        self.wandering_angle += wander_angle * rands
        return wander_force

    def update(self):
        self.v = helperfunctions.truncate(self.v + self.steering, self.max_speed)
        self.pos += self.v * dT


    def display(self, screen):
        screen.blit(self.image, self.rect)

    def reset_frame(self):
        self.steering = np.zeros(2)
