import pygame
from swarm import Flock
from physical_objects import Objects
import functions

"""
Code for initializing the simulation, as well as executing it 
"""


class Simulation():
    def __init__(self, num_agents, screen_size, obstacle=False, outside=False, convex=True):

        # environment settings
        self.obstacles_present = obstacle
        self.outside = outside
        self.convex = convex

        #display settings
        self.screensize = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.sim_background = self.set_background()

        #swarm settings
        self.num_agents = num_agents
        self.swarm = Flock(screen_size)
        self.objects = Objects()

        #update
        self.to_update = pygame.sprite.Group()
        self.to_display = pygame.sprite.Group()
        self.running = True


    def set_background(self):
        if self.convex:
            return pygame.Color('gray21')
        else:
            return pygame.Color('black')


    def display(self):
        for sprite in self.to_display:
            sprite.display(self.screen)

    def update(self):
        self.to_update.update()


    def initialize(self):

        #add obstacle/-s to the environment if present
        if self.obstacles_present:
            object_loc = [self.screensize[0]/2.,self.screensize[1]/2.]

            if self.outside:
                scale = [300,300]
            else:
                scale = [700,700]

            self.objects.add_obstacle(object_loc, scale=scale, outside=self.outside, convex=self.convex)

            min_x, max_x = functions.area(object_loc[0], scale[0])
            min_y, max_y = functions.area(object_loc[1], scale[1])


        #add obstacles to the swarm for easier functionality
        self.swarm.set_obstacles(self.objects.obstacles)


        #add agents to the environment
        for agent in range(self.num_agents):
            coordinates = functions.generate_coordinates(self.screensize)

            #if obstacles present re-estimate the corrdinates
            if self.obstacles_present:
                if self.outside:
                    while coordinates[0]<=max_x and coordinates[0]>=min_x and coordinates[1]<=max_y and coordinates[1]>=min_y:
                        coordinates = functions.generate_coordinates(self.screensize)
                else:
                    while coordinates[0]>=max_x or coordinates[0]<=min_x or coordinates[1]>=max_y or coordinates[1]<=min_y:
                        coordinates = functions.generate_coordinates(self.screensize)

            self.swarm.add_agents(coordinates)

        #add all agents/objects to the update
        self.to_update = pygame.sprite.Group(self.swarm)

        #display all the agents/objects
        self.to_display = pygame.sprite.Group(
            self.to_update
        )


    def run(self):
        #initialize the agent and obstacle positions within the environment
        self.initialize()

        #the simulation loop, infinite until the user exists the simulation
        while self.running:
            self.screen.fill(self.sim_background)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update()
            self.display()
            pygame.display.flip()

