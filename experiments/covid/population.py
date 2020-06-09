import numpy as np
from simulation.swarm import Swarm
from simulation import helperfunctions
from experiments.covid.person import Person
from experiments.covid import parameters as p


class Population(Swarm):
    def __init__(self, screen_size):
        super(Population, self).__init__(screen_size)
        self.points_to_plot = {'S':[], "I":[], "R":[]}
        self.object_loc = p.OUTSIDE

    def add_agents(self, pos, type, swarm):
        super(Population,self).add_agent(Person(pos=np.array(pos),v=None, type=type, population=swarm))

    def initialize(self, num_agents, swarm):

        # add obstacle/-s to the environment if present
        if p.OBSTACLES:
            object_loc = p.OBJECT_LOC
            scale = [1000, 1000]
            filename = 'experiments/covid/images/house.png'

            self.objects.add_object(file=filename, pos=object_loc, scale=scale, type='obstacle')

            min_x, max_x = helperfunctions.area(object_loc[0], scale[0])
            min_y, max_y = helperfunctions.area(object_loc[1], scale[1])


        # add agents to the environment
        for id, agent in enumerate(range(num_agents)):
            coordinates = helperfunctions.generate_coordinates(self.screen)

            if p.OBSTACLES:
                while coordinates[0]<=max_x and coordinates[0]>=min_x and coordinates[1]<=max_y and coordinates[1]>=min_y:
                    coordinates = helperfunctions.generate_coordinates(self.screen)

            if id < (int(round(p.INFECTED*num_agents))):
                self.add_agents(coordinates, 'I', swarm)
            else:
                self.add_agents(coordinates, 'S', swarm)

    # plotting the number of infected and recovered
    def add_point(self, lst):
        #Count current numbers
        values = {'S':0, 'I':0, 'R':0}
        for state in lst:
            values[state] += 1

        for x in values:
            self.points_to_plot[x].append(values[x])



    def detect_transmittable(self, neighbors):
        for idx in neighbors:
            if list(self.agents)[idx].transmittable == True: #at the moment check if one is transmittable return true
                return True

    def update(self): #simplify by passing flock, and see whether can simply the update to one (while keeping for each agent)

        datapoints = []

        for person in self.agents:
            person.update_actions()

            #Get S I R values
            datapoints.append(person.type)
        self.add_point(datapoints)
        self.remain_in_screen()
        self.update_general()
