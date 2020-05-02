from simulation import Simulation
import pygame


"""
Code for multi-agent simulation in PyGame with/without physical objects in the environment
"""

#define the screen settings
screen_width, screen_height = 1000, 1000
screen_size = (screen_width, screen_height)

#define the number of agents
number_agents = 30

#choose to display an obstacle, its shape, and whether to position agents inside or outside of the obstacle
obstacle_present = True
obstacle_convex = True
agents_outside = False


if __name__ == "__main__":
    pygame.init()
    sim = Simulation(num_agents=number_agents, screen_size=screen_size,
                     obstacle=obstacle_present, outside=agents_outside, convex = obstacle_convex)
    sim.run()
