import numpy as np
import pygame

from typing import Tuple

from simulation.agent import Agent
from simulation.utils import normalize, truncate
from experiments.flocking.config import config

"""
Specific boid properties and helperfunctions 
"""


class Boid(Agent):
    """
    Class that represents a boid (i.e. a simulated virtual "bird": bird-oid object). This class inherits the behavior
    from the base class Agent.

    Attributes:
    ----------
        flock:
        steering:
        mass:
        v:
        pos:

    """

    def __init__(
            self, pos, v, flock, index: int, image: str = "experiments/flocking/images/normal-boid.png"
    ) -> None:
        """
        Args:
        ----
            pos:
            v:
            flock:
            index (int):
            image (str): Defaults to "experiments/flocking/images/normal-boid.png"
        """
        super(Boid, self).__init__(
            pos,
            v,
            image,
            max_speed=config["agent"]["max_speed"],
            min_speed=config["agent"]["min_speed"],
            mass=config["agent"]["mass"],
            width=config["agent"]["width"],
            height=config["agent"]["height"],
            dT=config["agent"]["dt"],
            index=index
        )

        self.flock = flock

    def update_actions(self) -> None:
        """
        Every change between frames happens here. This function is called by the method "update" in the class Swarm,
        for every agent/object. Here, it is checked if there is an obstacle in collision (in which case it avoids it by
        going to the opposite direction), align force, cohesion force and separate force between the agent and its neighbors
        is calculated, and the steering force and direction of the agent are updated
        """

        # avoid any obstacles in the environment
        for obstacle in self.flock.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()

        align_force, cohesion_force, separate_force = self.neighbor_forces()

        # combine the vectors in one
        steering_force = (
                align_force * config["boid"]["alignment_weight"]
                + cohesion_force * config["boid"]["cohesion_weight"]
                + separate_force * config["boid"]["separation_weight"]
        )

        # adjust the direction of the boid
        self.steering += truncate(
            steering_force / self.mass, config["boid"]["max_force"]
        )

    def neighbor_forces(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Find the neighbors of the agent and compute the total align force (force required to align agent with its neighbors'
        total force), cohesion force (force required to move the agent towards the center of mass of its neighbors)
        and separate force considering the total amount of neighbors close to the agent
        """
        # find all the neighbors of a boid based on its radius view
        neighbors = self.flock.find_neighbors(self, config["boid"]["radius_view"])

        pre_align_force, pre_cohesion_force, separate_force = self.flock.find_neighbor_velocity_center_separation(self,
                                                                                                                  neighbors)
        #
        # if there are neighbors, estimate the influence of their forces
        if neighbors:
            align_force = self.align(pre_align_force)
            cohesion_force = self.cohesion(pre_cohesion_force)
        #
        else:
            align_force, cohesion_force = (
                np.zeros(2),
                np.zeros(2),
            )
        return align_force, cohesion_force, separate_force

    def align(self, neighbor_force: np.ndarray):
        """
        Function to align the agent in accordance to neighbor velocity

        Args:
            neighbor_force (np.ndarray):

        """
        return normalize(neighbor_force - self.v)

    def cohesion(self, neighbor_center):
        """
        Function to move the agent towards the center of mass of its neighbors

        Args:
        ----
            neighbor_center:

        """
        force = neighbor_center - self.pos
        return normalize(force - self.v)
