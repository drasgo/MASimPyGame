from agents import Boid
import numpy as np
import pygame
import functions

"""
Python code for possible swarm class definition
Currently implemented a Flocking class representing a 'swarm' of boids
"""

#General settings for a floccking
RADIUS_VIEW=200
WANDER = True
SEPARATE= True
ALIGN= True
COHESION= True
OBSTACLE = True


class Flock(pygame.sprite.Sprite):
    def __init__(self, screen_size):
        super(Flock,self).__init__()
        self.all_boids=pygame.sprite.Group()
        self.screen = screen_size
        self.obstacles = None


    def add_agents(self, pos):
        self.all_boids.add(Boid(pos=np.array(pos)))

    def set_obstacles(self, sprite_obj):
        self.obstacles  = sprite_obj


    def find_neighbors(self,boid):
        boids = list(self.all_boids).copy()
        neighbors = []
        for j, neighbor in enumerate(boids):
            if boid == neighbor:
                continue
            elif functions.dist(boid.pos, neighbor.pos) < RADIUS_VIEW:
                neighbors.append(j)
        return neighbors, len(neighbors)

    def find_neighbor_velocity(self, neighbors):
        neighbor_sum_v = np.zeros(2)
        for idx in neighbors:
            neighbor_sum_v += list(self.all_boids)[idx].v
        return neighbor_sum_v


    def find_neighbor_center(self, neighbors):
        neighbor_sum_pos = np.zeros(2)
        for idx in neighbors:
            neighbor_sum_pos += list(self.all_boids)[idx].pos
        return neighbor_sum_pos


    def find_neighbor_seperation(self,neighbors,boid):
        seperate = np.zeros(2)
        for idx in neighbors:
            neighbor_pos = list(self.all_boids)[idx].pos
            difference = boid.pos - neighbor_pos
            difference /= functions.dist(boid.pos, neighbor_pos)
            seperate += difference
        return seperate

    def remain_in_screen(self):
        for boid in self.all_boids:
            if boid.pos[0] > self.screen[0]:
                boid.pos[0]=0.
            if boid.pos[0] < 0:
                boid.pos[0] = float(self.screen[0])
            if boid.pos[1] < 0:
                boid.pos[1] = float(self.screen[1])
            if boid.pos[1] > self.screen[1]:
                boid.pos[1]=0.


    def update(self):
        """
        Function to update the agents in a synchronous manner
        (1) First each agent acts on the world as a snapshot (first for loop)
        (2) Then the world is updated (second for loop)
        """
        #execute the actions
        for boid in self.all_boids:
            if self.obstacles != None: #obtacle avoidance
                for obstacle in self.obstacles:
                    collide = pygame.sprite.collide_mask(boid, obstacle)
                    if bool(collide):
                        boid.avoid_obstacle(obstacle.pos, obstacle.outside)

            if WANDER: boid.wander()  #wandering

            if ALIGN or COHESION or SEPARATE: #flocking forces
                neighbors, count = self.find_neighbors(boid)
                if count:
                    if ALIGN: boid.align(self.find_neighbor_velocity(neighbors)/count)
                    if COHESION: boid.cohesion(self.find_neighbor_center(neighbors)/count)
                    if SEPARATE: boid.separate(self.find_neighbor_seperation(neighbors,boid)/count)

        #keep agents within the display
        self.remain_in_screen()

        #update the world
        for boid in self.all_boids:
            boid.update()



    def display(self, screen):
        #display the changes made
        for obstacle in self.obstacles:
            obstacle.display(screen)
        for boid in self.all_boids:
            boid.display(screen)

        #reset the boid steering force to be updated again
        for boid in self.all_boids:
            boid.reset_frame()
