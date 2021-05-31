import numpy as np
import pygame

from simulation.utils import image_with_rect


class Objects(pygame.sprite.Sprite):
    """
    Object in charge of creating and storing every object (both obstacles and sites).

    Attributes:
    ----------
        obstacles:
        sites:
    """

    def __init__(self) -> None:
        super(Objects, self).__init__()
        self.obstacles = pygame.sprite.Group()
        self.sites = pygame.sprite.Group()

    def add_object(self, file, pos, scale, obj_type) -> None:
        """
        Args:
        ----
            file:
            scale:
            pos:
            obj_type:

        """
        if obj_type == "obstacle":
            self.obstacles.add(Object(filename=file, pos=np.array(pos), scale=scale))
        elif obj_type == "site":
            self.sites.add(Object(filename=file, pos=np.array(pos), scale=scale))
        else:
            print("object type not specified")


class Object(pygame.sprite.Sprite):
    """
    General Object class to load images in the environment. The generated object can be either an obstacle or a site but,
    as they are both static, nothing needs to be done but displaying the object every frame.

    Attributes:
    ----------
        image:
        rect:
        mask:
        pos:
    """

    def __init__(self, filename: str = None, pos: np.ndarray = None, scale=None) -> None:
        """
        Arguments:
        ---------
            filename (str): Defaults to None
            pos: (np.ndarray): Defaults to None
            scale: Defaults to None
        """
        super(Object, self).__init__()
        self.image, self.rect = image_with_rect(filename, scale)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos: np.ndarray = pos if pos is not None else np.zeros(2)
        self.rect = self.image.get_rect(center=self.pos)

    def display(self, screen) -> None:
        """
        Display the object for the new frame.

        Args:
        ----
            screen:

        """
        screen.blit(self.image, self.rect)
