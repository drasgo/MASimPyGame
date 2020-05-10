from simulation.simulation import Simulation
import pygame


"""
Code for multi-agent simulation in PyGame with/without physical objects in the environment
"""

#define the screen settings
screen_width, screen_height = 1000, 1000
screen_size = (screen_width, screen_height)

#define the number of agents
number_agents = 30

#choose swarm type
swarm = 'Flock'


if __name__ == "__main__":
    pygame.init()
    sim = Simulation(num_agents=number_agents, screen_size=screen_size,
                     swarm_type=swarm)
    sim.run()
