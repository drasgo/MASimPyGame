from simulation.utils import *

"""
General agent properties, which are common across all types of agents 
"""


# defines general agent properties
class Agent(pygame.sprite.Sprite):  # super class
    """
    This is the base class for any type of agent. This class contains the references for the position and velocity, as
    well as the possibility of rotating the image on the GUI, set the agent to wander, avoid an obstacle and set its
    velocity. Finally, here reside the update and display function, for visualizing the next frame on the GUI, as it extends
    the class pygame.sprite.Sprite

    Attributes:
    ----------
        index:
        image_file:
        base_image:
        rect:
        image:
        mask:
        mass:
        max_speed:
        min_speed:
        wandering_angle:
        steering:
        pos:
        v:
        dT:
        type:
     """
    base_image = None
    base_rect = None

    def __init__(
            self,
            pos=None,
            v=None,
            image: str = None,
            color=None,
            max_speed=None,
            min_speed=None,
            mass=None,
            width: int=None,
            height: int=None,
            dT=None,
            index: int = None
    ) -> None:
        """
        Args:
        ---------
            pos : Defaults to None
            v: Defaults to None
            image (str): Defaults to None
            color: Defaults to None
            max_speed: Defaults to None
            min_speed: Defaults to None
            mass: Defaults to None
            width: Defaults to None
            height: Defaults to None
            dT: Defaults to None
            index (int):Defaults to None
        """
        super(Agent, self).__init__()
        self.angle = None
        self.index = index
        self.image_file = image
        if self.image_file is not None:  # load image from file
            if not Agent.base_image:
                Agent.base_image, Agent.rect = image_with_rect(
                    self.image_file, [width, height]
                )
            self.rect = Agent.rect
            self.image = Agent.base_image
            self.mask = pygame.mask.from_surface(self.image)
            self.mask = self.mask.scale((12, 10))

        else:  # draw an agent
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)

        self.mass = mass
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.wandering_angle = randrange(
            -np.pi, np.pi
        )  # set a random wandering angle

        self.steering = np.zeros(2)
        self.pos = np.zeros(2) if pos is None else pos
        self.v: np.ndarray = self.set_velocity() if v is None else v
        self.dT = dT
        self.type = None

    @property
    def pos(self) -> np.ndarray:
        """Position getter for the current instance of Agent"""
        return self._pos

    @pos.setter
    def pos(self, pos) -> None:
        """
        Position setter for the current instance of Agent

        Args:
        ---------
            pos:

        """
        self._pos = pos
        self.rect.center = tuple(
            pos
        )  # update the rect position as thats actually displayed

    @property
    def v(self) -> np.ndarray:
        """Velocity getter for the current instance of Agent"""
        return self._v

    @v.setter
    def v(self, v: np.ndarray) -> None:
        """
        Velocity setter for the current instance of Agent

        Args:
        ---------
            v (np.ndarray):

        """
        self._v = v
        if self.image_file:
            self._rotate_image()

    def _rotate_image(self) -> None:
        """
        Rotate base image using the velocity to estimate the angle of rotation,
        which is later going to be used for the GUI.
        """
        angle = -np.rad2deg(
            np.angle(self.v[0] + 1j * self.v[1])
        )  # using complex number to estimate the angle for rotation

        if self.angle is None or np.abs(angle - self.angle) > 0.1:
            del self.image
            self.image = pygame.transform.rotate(
                Agent.base_image, angle
            )  # rotates the image
            self.rect = self.image.get_rect(center=self.rect.center)

        self.angle = angle

    def set_velocity(self) -> List[int]:
        """Determines a "random" velocity based on a random angle and x and y random speed components"""
        angle = np.pi * (2 * np.random.rand() - 1)
        velocity = [
            random.randrange(1, self.max_speed + 1) * plusminus(),
            random.randrange(1, self.max_speed + 1) * plusminus(),
        ]
        velocity *= np.array([np.cos(angle), np.sin(angle)])
        return velocity

    def wander(self, wander_dist, wander_radius, wander_angle) -> np.ndarray:
        """
        Function to make the agents perform random movement (wandering_angle) based on the wander angle, and with a
        (returned) wander force, based on the previous velocity, the wander distance and wander radius.

        Args:
        ---------
            wander_dist:
            wander_angle:
            wander_radius:
        """
        rands = 2 * np.random.rand() - 1
        cos = np.cos(self.wandering_angle)
        sin = np.sin(self.wandering_angle)
        n_v = normalize(self.v)
        circle_center = n_v * wander_dist
        displacement = np.dot(np.array([[cos, -sin], [sin, cos]]), n_v * wander_radius)
        wander_force = circle_center + displacement
        self.wandering_angle += wander_angle * rands
        return wander_force

    def avoid_obstacle(self) -> None:
        """
        Function to avoid obstacles
        need to take into account whether agents inside/outside the obstacle
        moves the agent away from the boarder by distance equivalent to its size
        """
        # adjust the velocity by rotating it around
        self.v = rotate(
            normalize(self.v)
        ) * norm(self.v)
        self.pos += self.v * 1.5

    def update(self) -> None:
        """
        Update the agent's velocity and position with the previously calculated speed and steering,
        so it's ready for the next frame.
        """
        self.v = truncate(
            self.v + self.steering, self.max_speed, self.min_speed
        )
        self.pos += self.v * self.dT

    def display(self, screen: pygame.Surface) -> None:
        """
        Refresh the updated agent on the GUI for the next frame.

        Args:
        ------
            screen (pygame.Surface):

        """
        screen.blit(self.image, self.rect)

    def reset_frame(self) -> None:
        """Reset the steering value for the next computations"""
        self.steering = np.zeros(2)
