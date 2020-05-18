import pygame
import sys
from experiments.flocking.flock import Flock
from experiments.covid.population import Population
from experiments.aggregation.aggregation import Aggregations


"""
General simulation pipeline, suitable for all experiments 
"""

class Simulation():
    def __init__(self, num_agents, screen_size, swarm_type, iterations):


        #general settings
        self.screensize = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.sim_background = pygame.Color('gray21')
        self.iter = iterations

        #swarm settings
        self.num_agents = num_agents
        if swarm_type == 'Flock':
            self.swarm = Flock(screen_size)
        elif swarm_type == 'Aggregation':
            self.swarm = Aggregations(screen_size)
            pass
        elif swarm_type == 'Covid':
            self.swarm = Population(screen_size)
        else:
            print('None of the possible swarms selected')
            sys.exit()

        #update
        self.to_update = pygame.sprite.Group()
        self.to_display = pygame.sprite.Group()
        self.running = True



    def display(self):
        for sprite in self.to_display:
            sprite.display(self.screen)

    def update(self):
        self.to_update.update()


    def initialize(self):

        #initialize a swarm type specific environment
        self.swarm.initialize(self.num_agents, self.swarm)

        #add all agents/objects to the update
        self.to_update = pygame.sprite.Group(self.swarm)

        #add all agents/objects to display
        self.to_display = pygame.sprite.Group(
            self.to_update
        )

    def simulate(self):
        self.screen.fill(self.sim_background)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.update()
        self.display()
        pygame.display.flip()



    def run(self):
        #initialize the environment and agent/obstacle positions
        self.initialize()

        #the simulation loop, infinite until the user exists the simulation
        #finite time parameter or infinite
        if self.iter == -1:
            while self.running:
                self.simulate()
        else:
            for i in range(self.iter):
                self.simulate()


