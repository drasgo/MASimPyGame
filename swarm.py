from agents import Boid,Obstacle
import numpy as np
import pygame
import functions




RADIUS_VIEW=200

#weights
COHESION_WEIGHT = 10.9 #10.
ALIGNMENT_WEIGHT = 3.5
SEPERATION_WEIGHT = 7.5
WANDER_WEIGHT=1.3 #1.1

#Transport
MOVE=1.5


class Flock(pygame.sprite.Sprite):
    def __init__(self, screen_size, obstacle, wander=True, separate=True, align=True, cohesion=True):
        super(Flock,self).__init__()
        #create a list of boids as sprite objects
        self.all_boids=pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.screen = screen_size
        self.obstacle_selected = obstacle
        self.wander_selected = wander
        self.separate_selected = separate
        self.align_selected = align
        self.cohesion_selected = cohesion

    def add_boid(self, pos):
        #add boids to the sprite list
        # angle = np.pi * (2 * np.random.rand() - 1)
        # #estimate velocity vector
        # velocity=Boid.speedvector()
        # velocity = velocity * np.array([np.cos(angle), np.sin(angle)])
        self.all_boids.add(Boid(pos=np.array(pos))) #initialize all velocities to the same value

    def add_obstacle(self, pos, scale, outside, convex):
        self.obstacles.add(Obstacle(pos=np.array(pos), scale=scale, outside = outside, convex=convex))



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

        #execute actions
        for i,boid in enumerate(self.all_boids):
            #obtacle avoidance
            if self.obstacle_selected:
                for obstacle in self.obstacles:
                    collide = pygame.sprite.collide_mask(boid, obstacle)
                    if bool(collide):
                        boid.avoid_obstacle(obstacle.pos, obstacle.outside)
            #wandering
            if self.wander_selected: boid.wander()
            #flocking forces
            if self.align_selected or self.cohesion_selected or self.separate_selected:
                neighbors, count = self.find_neighbors(boid)
                if count:
                    if self.align_selected: boid.align(self.find_neighbor_velocity(neighbors)/count)
                    if self.cohesion_selected: boid.cohesion(self.find_neighbor_center(neighbors)/count)
                    if self.separate_selected: boid.separate(self.find_neighbor_seperation(neighbors,boid)/count)

        #keep agents within the display
        self.remain_in_screen()

        #update actions
        for boid in self.all_boids:
            boid.update()



    def display(self, screen):
        for obstacle in self.obstacles:
            obstacle.display(screen)
        for boid in self.all_boids:
            boid.display(screen)
        for boid in self.all_boids:
            boid.reset_frame()
