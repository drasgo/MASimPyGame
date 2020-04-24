from simulation import Simulation
import pygame

"""
Code for flocking simulation in pygame with/without hallow obstacle 
"""


screen_width, screen_height = 1000, 1000
screen_size = (screen_width, screen_height)
number_boids = 50

if __name__ == "__main__":
    pygame.init()
    sim = Simulation(num_boids=number_boids, screen_size=screen_size,
                     obstacle=True, outside=True,
                     wander=True,
                     align=True,
                     separate=True,
                     cohesion = True)
    sim.run()
