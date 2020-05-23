import numpy as np
from simulation import helperfunctions
from simulation.swarm import Swarm
from experiments.aggregation.aggregationAgent import aggregationAgent
from experiments.aggregation import parameters as p

"""
Python code for aggregations implementation
"""


class Aggregations(Swarm):
    def __init__(self, screen_size):
        super(Aggregations, self).__init__(screen_size)
        self.object_loc = p.OUTSIDE


    def add_agents(self, pos, aggregation):
        super(Aggregations,self).add_agent(aggregationAgent(pos=np.array(pos),v=None, aggregation=aggregation))


    def initialize(self, num_agents, swarm):

        # add obstacle/-s to the environment if present
        if p.OBSTACLES:
            object_loc = p.OBJECT_LOC

            if p.OUTSIDE:
                scale = [300, 300]
            else:
                scale = [700, 700]

            filename = 'experiments/flocking/images/convex.png' if p.CONVEX else 'experiments/flocking/images/redd.png'

            self.objects.add_object(file= filename, pos=object_loc, scale=scale, type='obstacle')

            min_x, max_x = helperfunctions.area(object_loc[0], scale[0])
            min_y, max_y = helperfunctions.area(object_loc[1], scale[1])


        # add sites to the environment if present
        area_loc1, scale1, bigB1, area_loc2, scale2, bigB2 = p.experiment4(self.screen, p.OUTSIDE)
        filename2 = 'experiments/aggregation/images/greyc2.png' if bigB1 else 'experiments/aggregation/images/greyc1.png'
        filename3 = 'experiments/aggregation/images/greyc2.png' if bigB2 else 'experiments/aggregation/images/greyc1.png'
        self.objects.add_object(file=filename2, pos=area_loc1, scale=scale1, type='site')
        self.objects.add_object(file=filename2, pos=area_loc2, scale=scale2, type='site')


        # add agents to the environment
        for agent in range(num_agents):
            coordinates = helperfunctions.generate_coordinates(self.screen)

            # if obstacles present re-estimate the corrdinates
            if p.OBSTACLES:
                if p.OUTSIDE:
                    while coordinates[0] <= max_x and coordinates[0] >= min_x and coordinates[1] <= max_y and \
                            coordinates[1] >= min_y:
                        coordinates = helperfunctions.generate_coordinates(self.screen)
                else:
                    while coordinates[0] >= max_x or coordinates[0] <= min_x or coordinates[1] >= max_y or coordinates[
                        1] <= min_y:
                        coordinates = helperfunctions.generate_coordinates(self.screen)

            self.add_agents(coordinates, swarm)

        #print(self.agents)


    def update(self):
        for cockroach in self.agents:
            cockroach.update_actions()
            #print(cockroach.get_state())

        self.remain_in_screen()
        self.update_general()


    def get_number_wandering_agents(self):
        counter = 0
        for agent in self.agents:
            if agent.get_state():
                counter = counter + 1

        return counter
