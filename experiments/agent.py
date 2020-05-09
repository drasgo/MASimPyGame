import pygame
import numpy as np
from experiments import helperfunctions
import random

"""
General agent properties, which are common across all types of agents 
"""


MAX_SPEED = 4.


#defines general agent properties
class Agent(pygame.sprite.Sprite): #super class
    def __init__(self, pos=None, v=None, image=None):
        super(Agent, self).__init__()

        self.base_image, self.rect = helperfunctions.image_with_rect(image, [10, 8])
        self.image = self.base_image
        self.mask = pygame.mask.from_surface(self.image)
        self.mask = self.mask.scale((12, 10))

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
        self._rotate_image()

    def _rotate_image(self):
        """Rotate base image using the velocity and assign to image."""
        angle = -np.rad2deg(np.angle(self.v[0] + 1j * self.v[1])) #using complex number to estimate the angle for rotation
        self.image = pygame.transform.rotate(self.base_image, angle) #rotates the image
        self.rect = self.image.get_rect(center=self.rect.center)


    def set_velocity(self):
        angle = np.pi * (2 * np.random.rand() - 1)
        velocity = [random.randrange(1, MAX_SPEED + 1) * helperfunctions.plusminus(),
                    random.randrange(1, MAX_SPEED + 1) * helperfunctions.plusminus()]
        velocity *= np.array([np.cos(angle), np.sin(angle)])
        return velocity

    def update(self):
        self.v = helperfunctions.truncate(self.v + self.steering, MAX_SPEED)
        self.pos += self.v


    def display(self, screen):
        screen.blit(self.image, self.rect)

    def reset_frame(self):
        self.steering = np.zeros(2)
