import pygame
import numpy as np
import functions

"""
Python code for physical object implementation
Contains a main class Objects, to which an Obstacle instance is passed via add_obstacle 
"""


class Objects(pygame.sprite.Sprite):
    def __init__(self):
        super(Objects,self).__init__()
        self.obstacles = pygame.sprite.Group()

    def add_obstacle(self, pos, scale, outside, convex):
        self.obstacles.add(Obstacle(pos=np.array(pos), scale=scale, outside=outside, convex_shape=convex))


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, pos=None, scale=None, outside=False, convex_shape=False):
        super(Obstacle,self).__init__()
        filename = 'redd.png' if not convex_shape else 'convex.png'
        self.image, self.rect = functions.image_with_rect(filename, scale)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pos if pos is not None else np.zeros(2)
        self.rect = self.image.get_rect(center=self.pos)
        self.outside = outside


    def display(self, screen):
        screen.blit(self.image ,self.rect)