import pygame
import numpy as np
import functions
import random

BOID_MAX_SPEED = 8.
BOID_MAX_FORCE = 10.

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
        # print('size agent', self.mask.get_size())

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

    #
    # def steer_new(self, force):
    #     self.steering += force
    #
    # def steer_normalize(self, weight_sum):
    #     self.steering /= weight_sum
    #     self.steering = functions.scalevector(self.steering, random.randrange(averagebirdspeed-lowerbound,averagebirdspeed+upperbound))


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


    def display(self, screen, debug=False):
        screen.blit(self.image, self.rect)

    def reset_frame(self):
        self.steering = np.zeros(2)

    def speedvector(self):
        angle = np.pi * (2 * np.random.rand() - 1)
        velocity=[random.randrange(1, BOID_MAX_SPEED + 1) * functions.plusminus(),
         random.randrange(1, BOID_MAX_SPEED + 1) * functions.plusminus()]
        velocity *= np.array([np.cos(angle), np.sin(angle)])
        return velocity


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, pos=None, scale=None, outside=False):
        super(Obstacle,self).__init__()
        self.image, self.rect = functions.image_with_rect('redd.png', scale) #'red.png'
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pos if pos is not None else np.zeros(2)
        self.rect = self.image.get_rect(center=self.pos)
        self.outside = outside



    def display(self, screen):
        screen.blit(self.image ,self.rect)