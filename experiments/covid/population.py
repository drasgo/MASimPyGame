import numpy as np
from simulation.swarm import Swarm
from simulation import helperfunctions
from experiments.covid.person import Person
from experiments.covid import parameters as p


class Population(Swarm):
    def __init__(self, screen_size):
        super(Population, self).__init__(screen_size, plot={'S':[], "I":[], "R":[]})
        self.object_loc = p.OUTSIDE

    def initialize(self, num_agents, swarm):

        # add obstacle/-s to the environment if present
        if p.OBSTACLES:
            object_loc = p.OBJECT_LOC #center point location
            scale = [700, 700]
            filename = 'experiments/covid/images/maze.png'
            # filename = 'experiments/covid/images/house.png'

            self.objects.add_object(file=filename, pos=object_loc, scale=scale, type='obstacle')

        # add agents to the environment
        for id, agent in enumerate(range(num_agents)):
            coordinates = helperfunctions.generate_coordinates(self.screen)

            if p.OBSTACLES:
                for object in self.objects.obstacles:
                    rel_coordinate = helperfunctions.relative(coordinates,(object.rect[0], object.rect[1]))
                    try:
                        while object.mask.get_at(rel_coordinate):
                            coordinates = helperfunctions.generate_coordinates(self.screen)
                            rel_coordinate = helperfunctions.relative(coordinates, (object.rect[0], object.rect[1]))
                    except IndexError:
                        pass

            if id < (int(round(p.INFECTED*num_agents))):

                self.add_agent(Person(pos=np.array(coordinates), v=None, type='I', population=swarm))
            else:
                self.add_agent(Person(pos=np.array(coordinates), v=None, type='S', population=swarm))


    def detect_transmittable(self, neighbors):
        for idx in neighbors:
            if list(self.agents)[idx].transmittable == True: #at the moment check if one is transmittable return true
                return True
