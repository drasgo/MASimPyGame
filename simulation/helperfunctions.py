import numpy as np
import math
import random
import pygame

"""
Useful vector transformation functions, and other to make the code more clear 
"""

def area(a,b):
    """
    :param a: object mid point
    :param b: scale
    :return:
    """
    if b<a:
        max = a + 0.5*b
        min = a - 0.5*b
    else:
        max = a + 0.25*b
        min=a - 0.25*b
    return min, max

def generate_coordinates(screensize):
    return [float(random.randrange(0, screensize[0])), float(random.randrange(0, screensize[1]))]

def dist(a,b):
    """
    return the distance between two vectors
    :param a: np.array
    :param b: np.array
    :return:
    """
    return norm(a-b)


def image_with_rect(filename, scale):
    _image = pygame.image.load(filename)
    _image = pygame.transform.scale(_image, (scale[0],scale[1])) #10,8
    return _image, _image.get_rect()


def randrange(a, b):
    """Random number between a and b."""
    return a + np.random.random() * (b - a)

def plusminus():
    # random 1 or -1
    return 1 if (random.random()>0.5) else -1


def rotate(vector):
    new_vector=np.zeros(2)
    theta=np.deg2rad(random.randint(120,180))
    cs = np.cos(theta)
    sn = np.sin(theta)
    new_vector[0] = vector[0] *cs - vector[1]*sn
    new_vector[1] = vector[0] *sn + vector[1]*cs
    return new_vector

def normalize(vector):
    """
    Function to normalize a vector
    ----------
    param vector : np.array
    return: unit vector
    """
    n = norm(vector)
    if n < 1e-13:
        return np.zeros(2)
    else:
        return np.array(vector) / n


def truncate(vector, max_length, min_lenght=None):
    """Truncate the length of a vector to a maximum/minimum value."""
    n = norm(vector)
    if n > max_length:
        return normalize(vector) * max_length
    elif min_lenght != None and n< min_lenght:
        return normalize(vector)*min_lenght
    else:
        return vector

def norm(vector):
    """Compute the norm of a vector."""
    return math.sqrt(vector[0]**2 + vector[1]**2)


def speedvector(max_speed):
    return [random.randrange(1,max_speed*2+1)*plusminus(), random.randrange(1,max_speed*2+1)*plusminus()]




