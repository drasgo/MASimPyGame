import numpy as np
import math
import random
from math import *
import pygame

def image_with_rect(filename, scale):
    _image = pygame.image.load(filename)
    _image = pygame.transform.scale(_image, (scale[0],scale[1])) #10,8
    return _image, _image.get_rect()

def area(a,b):
    min = a-b
    max = a +b
    return min, max

def randrange(a, b):
    """Random number between a and b."""
    return a + np.random.random() * (b - a)


def rotate(vector):
    new_vector=np.zeros(2)
    theta=np.deg2rad(random.randint(120,180))
    cs = np.cos(theta)
    sn = np.sin(theta)
    new_vector[0] = vector[0] *cs - vector[1]*sn
    new_vector[1] = vector[0] *sn + vector[1]*cs
    return new_vector


def truncate(vector, max_length):
    """Truncate the length of a vector to a maximum value."""
    n = norm(vector)
    if n > max_length:
        return normalize(vector, pre_computed=n) * max_length
    else:
        return vector

def norm(vector):
    """Compute the norm of a vector."""
    return math.sqrt(vector[0]**2 + vector[1]**2)

def norm2(vector):
    """Compute the square norm of a vector."""
    return vector[0] * vector[0] + vector[1] * vector[1]


def normalize(vector, pre_computed=None):
    """Return the normalized version of a vector.

    Parameters
    ----------
    vector : np.array
    pre_computed : float, optional
        The pre-computed norm for optimization. If not given, the norm
        will be computed.
    """
    n = pre_computed if pre_computed is not None else norm(vector)
    if n < 1e-13:
        return np.zeros(2)
    else:
        return np.array(vector) / n

def dist(a,b):
    """
    return the distance between two vectors
    :param a: np.array
    :param b: np.array
    :return:
    """
    return norm(a-b)

def dist2(a, b):
    """Return the square distance between two vectors.

    Parameters
    ----------
    a : np.array
    b : np.array
    """
    return norm2(a - b)
#
# #small functions, mostly for making it easier to work with the vectors
def plusminus():                                    #random 1 or -1
    return 1 if (random.random()>0.5) else -1

def speedvector(max_speed):
    return [random.randrange(1,max_speed*2+1)*plusminus(), random.randrange(1,max_speed*2+1)*plusminus()]

# # def vmag(v):                                        #returns a vectors magnitude
#     return abs(sqrt( v[0]**2 + v[1]**2 ))
#
#
# def scalevector(vector, magnitude):                 #scale a vector to a certain magnitude without altering its direction
#     ratio=magnitude/vmag(vector)
#     return [vector[0]*ratio, vector[1]*ratio]