import pygame

# from experiments.aggregation.config import config
# from experiments.covid.config import config
from experiments.flocking.config import config
from simulation.simulation import Simulation

"""
Code for multi-agent simulation in PyGame with/without physical objects in the environment
"""

if __name__ == "__main__":
    pygame.init()
    sim = Simulation(num_agents=config["base"]["n_agents"],
                     screen_size=(config["screen"]["width"], config["screen"]["height"]),
                     swarm_type=config["base"]["swarm_type"], iterations=config["screen"]["frames"])
    sim.run()
