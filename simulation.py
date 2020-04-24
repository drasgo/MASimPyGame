import pygame
import random
from swarm import Flock
import functions


SIM_BACKGROUND = pygame.Color('black')

class Simulation():
    def __init__(self, num_boids, screen_size, obstacle=False, outside=False,
                 wander=True, align=True,separate=True, cohesion=True):

        self.num_boids = num_boids
        self.flock = Flock(screen_size, obstacle, wander=wander, align=align, separate=separate, cohesion =cohesion)
        self.screensize = screen_size
        self.to_update = pygame.sprite.Group()
        self.to_display = pygame.sprite.Group()
        self.running = True
        self.screen = pygame.display.set_mode(screen_size)
        self.barriers = obstacle
        self.outside = outside

    def display(self):
        for sprite in self.to_display:
            sprite.display(self.screen) #loop all the objects stored in to_display, access their display

    def generate_coordinates(self):
        return [float(random.randrange(0, self.screensize[0])), float(random.randrange(0,self.screensize[1]))]

    def update(self):
        self.to_update.update()

    def initialize(self):
        min_x, max_x=None, None
        min_y, max_y = None, None
        if self.barriers:
            if self.outside:
                scale = [300,300]
            else:
                scale = [700,700]
            min_x, max_x = functions.area(self.screensize[0] / 2, scale[0]/2)
            min_y, max_y = functions.area(self.screensize[1] / 2, scale[1]/2)

            self.flock.add_obstacle([self.screensize[0]/2.,self.screensize[1]/2.], scale=scale, outside=self.outside)

        #weird bug but need to adjust the sie when the flock is inside, smth with scale funciton is different
        if not self.outside:
            max_x -=150
            max_y -=150
            min_x += 150
            min_y += 150

        for boid in range(self.num_boids): #add boids to the environment
            coordinates = self.generate_coordinates() #generate coordinates within the scope of the screen
            if self.barriers:
                if self.outside:
                    while coordinates[0]<=max_x and coordinates[0]>=min_x and coordinates[1]<=max_y and coordinates[1]>=min_y:
                        coordinates = self.generate_coordinates()
                else:
                    while coordinates[0]>=max_x or coordinates[0]<=min_x or coordinates[1]>=max_y or coordinates[1]<=min_y:
                        coordinates = self.generate_coordinates()
            self.flock.add_boid(coordinates)


        self.to_update = pygame.sprite.Group(self.flock)


        self.to_display = pygame.sprite.Group(
            self.to_update
        )


    def run(self):
        self.initialize()
        while self.running:
            self.screen.fill(SIM_BACKGROUND)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


            self.update()
            self.display()
            pygame.display.flip()




