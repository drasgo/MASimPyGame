import numpy as np
from simulation import utils
from simulation.swarm import Swarm
from experiments.aggregation.cockroach import Cockroach
from experiments.aggregation.config import config
from experiments.aggregation.testing_scenarios import *
"""
Python code for aggregations implementation
"""


class Aggregations(Swarm):
    def __init__(self, screen_size):
        super(Aggregations, self).__init__(screen_size)
        self.object_loc = config["aggregation"]["outside"]

    def initialize(self, num_agents):

        # add obstacle/-s to the environment if present
        if config["aggregation"]["obstacles"]:
            object_loc = config["base"]["object_location"]

            if config["aggregation"]["outside"]:
                scale = round_v([config["screen"]["width"]*.3, config["screen"]["height"]*.3])
            else:
                scale = round_v([config["screen"]["width"]*.7, config["screen"]["height"]*.7])

            filename = 'experiments/flocking/images/convex.png' if config["aggregation"]["convex"] else 'experiments/flocking/images/redd.png'

            self.objects.add_object(file= filename, pos=object_loc, scale=scale, obj_type='obstacle')

            min_x, max_x = utils.area(object_loc[0], scale[0])
            min_y, max_y = utils.area(object_loc[1], scale[1])


        # add sites to the environment if present
        area_loc1, scale1, bigB1, area_loc2, scale2, bigB2 = experiment2(self.screen, config["aggregation"]["outside"])
        #area_loc1, scale1, bigB1 = p.experiment0(self.screen, p.OUTSIDE)
        filename2 = 'experiments/aggregation/images/greyc2.png' if bigB1 else 'experiments/aggregation/images/greyc1.png'
        filename3 = 'experiments/aggregation/images/greyc2.png' if bigB2 else 'experiments/aggregation/images/greyc1.png'
        self.objects.add_object(file=filename2, pos=area_loc1, scale=scale1, obj_type='site')
        self.objects.add_object(file=filename3, pos=area_loc2, scale=scale2, obj_type='site')


        # add agents to the environment
        for index, agent in enumerate(range(num_agents)):
            coordinates = utils.generate_coordinates(self.screen)

            # if obstacles present re-estimate the corrdinates
            if config["aggregation"]["obstacles"]:
                if config["aggregation"]["outside"]:
                    while max_x >= coordinates[0] >= min_x and max_y >= coordinates[1] >= min_y:
                        coordinates = utils.generate_coordinates(self.screen)
                else:
                    while coordinates[0] >= max_x or coordinates[0] <= min_x or coordinates[1] >= max_y or coordinates[
                        1] <= min_y:
                        coordinates = utils.generate_coordinates(self.screen)

            self.add_agent(Cockroach(pos=np.array(coordinates),v=None, aggregation=self, index=index))
