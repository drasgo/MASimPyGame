import pygame
from simulation import helperfunctions
from simulation.objects import Objects

"""
General swarm class that defines general swarm properties, which are common across different swarm types
"""

#superclass
class Swarm(pygame.sprite.Sprite):

    def __init__(self,screen_size, plot=None):
        super(Swarm,self).__init__()
        self.agents = pygame.sprite.Group()
        self.screen = screen_size
        self.objects = Objects()
        self.points_to_plot = plot
        self.datapoints = []


    def add_agent(self,agent):
        self.agents.add(agent)

    def find_neighbors(self, agent, radius):
        agents = list(self.agents).copy()
        neighbors = []
        for j, neighbor in enumerate(agents):
            if agent == neighbor:
                continue
            else:
                try:
                    type = neighbor.type
                except:
                    type = None

            if type != None:
                if type =='I' and helperfunctions.dist(agent.pos, neighbor.pos) < radius:
                    neighbors.append(j)
            elif helperfunctions.dist(agent.pos, neighbor.pos) < radius:
                neighbors.append(j)

        return neighbors

    def remain_in_screen(self):
        for agent in self.agents:
            if agent.pos[0] > self.screen[0]:
                agent.pos[0]=0.
            if agent.pos[0] < 0:
                agent.pos[0] = float(self.screen[0])
            if agent.pos[1] < 0:
                agent.pos[1] = float(self.screen[1])
            if agent.pos[1] > self.screen[1]:
                agent.pos[1]=0.

    # plotting the number of infected and recovered
    def add_point(self, lst):
        #Count current numbers
        values = {'S':0, 'I':0, 'R':0}
        for state in lst:
            values[state] += 1

        for x in values:
            self.points_to_plot[x].append(values[x])

    def update(self):
        #update the movement
        self.datapoints = []
        for agent in self.agents:
            agent.update_actions()

        if len(self.datapoints):
            self.add_point(self.datapoints)
        self.remain_in_screen()

        #execute the update
        for agent in self.agents:
            agent.update()


    def display(self, screen):
        for obstacle in self.objects.obstacles:
            obstacle.display(screen)

        for site in self.objects.sites:
            site.display(screen)

        for agent in self.agents:
            agent.display(screen)

        for agent in self.agents:
            agent.reset_frame()
