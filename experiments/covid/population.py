import numpy as np
from simulation.swarm import Swarm
from simulation import helperfunctions
from experiments.covid.person import Person
from experiments.covid import parameters as p




class Population(Swarm):
    def __init__(self, screen_size):
        super(Population, self).__init__(screen_size)

    def add_agents(self, pos, type, swarm):
        super(Population,self).add_agent(Person(pos=np.array(pos),v=None, type=type, population=swarm))

    def initialize(self, num_agents, swarm):

        # add agents to the environment
        for id, agent in enumerate(range(num_agents)):
            coordinates = helperfunctions.generate_coordinates(self.screen)

            if id < (int(round(p.INFECTED*num_agents))):
                self.add_agents(coordinates, 'I', swarm)
            else:
                self.add_agents(coordinates, 'S', swarm)


    def detect_transmittable(self, neighbors):
        for idx in neighbors:
            if list(self.agents)[idx].transmittable == True: #at the moment check if one is transmittable return true
                return True

    def update(self): #simplify by passing flock, and see whether can simply the update to one (while keeping for each agent)
        for person in self.agents:
            person.update_actions()

        self.remain_in_screen()
        self.update_general()