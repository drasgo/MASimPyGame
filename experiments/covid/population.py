import numpy as np
from simulation.swarm import Swarm
from simulation import utils
from experiments.covid.person import Person
from experiments.covid.config import config


class Population(Swarm):
    def __init__(self, screen_size):
        super(Population, self).__init__(screen_size, plot={'S':[], "I":[], "R":[]})

    def initialize(self, num_agents):

        # add obstacle/-s to the environment if present
        if config["population"]["obstacles"]:
            object_loc = config["base"]["object_location"] #center point location
            scale = [800, 800]
            filename = 'experiments/covid/images/house2.png'
            # filename = 'experiments/covid/images/house.png'

            self.objects.add_object(file=filename, pos=object_loc, scale=scale, obj_type='obstacle')

        # add agents to the environment
        for id, agent in enumerate(range(num_agents)):
            coordinates = utils.generate_coordinates(self.screen)

            if config["population"]["obstacles"]:
                for object in self.objects.obstacles:
                    rel_coordinate = utils.relative(coordinates,(object.rect[0], object.rect[1]))
                    try:
                        while object.mask.get_at(rel_coordinate):
                            coordinates = utils.generate_coordinates(self.screen)
                            rel_coordinate = utils.relative(coordinates, (object.rect[0], object.rect[1]))
                    except IndexError:
                        pass

            if id < (int(round(config["person"]["p_infected"]*num_agents))):

                self.add_agent(Person(pos=np.array(coordinates), v=None, type='I', population=self, index=id))
            else:
                self.add_agent(Person(pos=np.array(coordinates), v=None, type='S', population=self, index=id))


    def detect_transmittable(self, neighbors: list) -> bool:
        if any(neighbor.transmittable is True for neighbor in neighbors):
            return True
        return False
