import math
import random

import numpy as np
import pygame

from typing import Any, List, Mapping, Tuple, Union

"""
Useful vector transformation functions, and other to make the code more clear 
"""


def area(a, b: float):
    """
    Args:
    ----
        a: object mid point
        b (float):

    """
    if b < a:
        max_val = a + 0.5 * b
        min_val = a - 0.5 * b
    else:
        max_val = a + 0.25 * b
        min_val = a - 0.25 * b
    return min_val, max_val


def generate_coordinates(screensize) -> List[float]:
    """
    Generate random coordinates given the screensize

    Args:
    ----
        screensize:

    """
    return [
        float(random.randrange(0, screensize[0])),
        float(random.randrange(0, screensize[1])),
    ]


def dist(a: np.ndarray, b: np.ndarray) -> float:
    """
    Return the euclidean distance between two vectors

    Args:
    ----
        a (np.ndarray):
        b (np.ndarray):

    """
    return norm(a - b)


def image_with_rect(filename: str, scale: Union[Mapping[int, Any], List[int]]) ->\
        Tuple[Union[pygame.Surface, pygame.SurfaceType], Union[pygame.Rect, Any]]:
    """
    Load the image that is going to represent the agent on the GUI

    Args:
    ----
        filename (str):
        scale (Mapping[int: Any]):

    """
    _image = pygame.image.load(filename)
    _image = pygame.transform.scale(_image, (scale[0], scale[1]))  # 10,8
    return _image, _image.get_rect()


def randrange(a: float, b: float) -> float:
    """
    Random number between a and b.

    Args:
    ----
        a (float):
        b (float):

    """
    return a + np.random.random() * (b - a)


def plusminus() -> int:
    """Returns randomly either 1 or -1"""
    return 1 if (random.random() > 0.5) else -1


def rotate(vector: np.ndarray) -> np.ndarray:
    """
    Randomly rotate the input vector

    Args:
    ----
        vector (numpy.ndarray):

    """
    new_vector = np.zeros(2)
    theta = np.deg2rad(random.randint(150, 210))
    cs = np.cos(theta)
    sn = np.sin(theta)
    new_vector[0] = vector[0] * cs - vector[1] * sn
    new_vector[1] = vector[0] * sn + vector[1] * cs
    return new_vector


def normalize(vector: np.ndarray) -> np.ndarray:
    """Function to normalize a vector

    Args:
    -----
        vector (np.array):

    """
    n = norm(vector)
    if n < 1e-13:
        return np.zeros(2)
    else:
        return np.array(vector) / n


def truncate(vector: np.ndarray, max_length: float, min_length: float = None) -> np.ndarray:
    """
    Truncate the length of a vector to a maximum/minimum value.

    Args:
    ----
    vector (numpy.ndarray):
    min_lenght (float): Defaults to None
    max_length (float):

    """
    n = norm(vector)
    if n > max_length:
        return normalize(vector) * max_length
    elif min_length is not None and n < min_length:
        return normalize(vector) * min_length
    else:
        return vector


def norm(vector: np.ndarray) -> float:
    """
    Compute the norm of a vector.

    Args:
        vector (numpy.ndarray):

    """
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)


def speedvector(max_speed: int) -> List[int]:
    """
    Return a random speed vector

    Args:
        max_speed (int):

    """
    return [
        random.randrange(1, max_speed * 2 + 1) * plusminus(),
        random.randrange(1, max_speed * 2 + 1) * plusminus(),
    ]


def relative(u: np.ndarray, v: np.ndarray) -> List[int]:
    """
    Args:
        u (numpy.ndarray):
        v (numpy.ndarray):

    """
    return [int(u[i]) - int(v[i]) for i in range(len(u))]
