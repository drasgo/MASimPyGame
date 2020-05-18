from simulation.simulation import Simulation
import pygame


"""
Code for multi-agent simulation in PyGame with/without physical objects in the environment
"""

#define the screen settings
screen_width, screen_height = 1000, 1000
screen_size = (screen_width, screen_height)

#define the number of agents
number_agents = 20

#choose how long to run the simulation
#-1 : infinite, N: finite
frames=-1

#choose swarm type
swarm = 'Aggregation'#Covid'


if __name__ == "__main__":
    pygame.init()
    sim = Simulation(num_agents=number_agents, screen_size=screen_size,
                     swarm_type=swarm, iterations=frames)
    sim.run()
