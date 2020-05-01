from simulation import Simulation
import os

#if you want to run the game without a visuals:
#set display = False
# os.environ['SDL_VIDEODRIVER']='dummy'

import pygame


"""
Code for flocking simulation in pygame with/without hallow obstacle 
"""


screen_width, screen_height = 1000, 1000
screen_size = (screen_width, screen_height)
number_boids = 30 #100

if __name__ == "__main__":
    pygame.init()
    sim = Simulation(num_boids=number_boids, screen_size=screen_size,
                     obstacle=True, outside=False,
                     wander=True,
                     align=True,
                     separate=True,
                     cohesion = True,
                     display_screen = True,
                     convex = False)
    sim.run()
