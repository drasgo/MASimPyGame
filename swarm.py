from agents import Boid,Obstacle
import numpy as np
import pygame
import functions


#Wander settings
WANDER_RADIUS = 3.0
WANDER_DIST = 3.5
WANDER_ANGLE = 1.0

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
        self.implement_obstacle = obstacle
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

    def wander(self):
        """Make all boids wander around randomly."""
        rands = 2 * np.random.rand(len(self.all_boids)) - 1
        cos = np.cos([b.wandering_angle for b in self.all_boids])
        sin = np.sin([b.wandering_angle for b in self.all_boids])
        for i, boid in enumerate(self.all_boids):
            nvel = functions.normalize(boid.v)
            # calculate circle center
            circle_center = nvel * WANDER_DIST
            # calculate displacement force
            c, s = cos[i], sin[i]
            displacement = np.dot(np.array([[c, -s], [s, c]]), nvel * WANDER_RADIUS)
            wander_force = circle_center + displacement
            boid.steer(wander_force*WANDER_WEIGHT)
            boid.wandering_angle += WANDER_ANGLE * rands[i]

    def align(self):

        boids = list(self.all_boids)
        neighbors = [[] for boid in boids]

        #find neighbors
        for i,boid in enumerate(boids):
            for j,neighbor_boid in enumerate(boids):
                # if functions.isinview(boid, neighbor_boid):
                if boid == neighbor_boid:
                    continue
                elif functions.dist(boid.pos, neighbor_boid.pos) < RADIUS_VIEW:
                    neighbors[i].append(j)
                    neighbors[j].append(i)

        for i, boid in enumerate(boids):
            n_neighbors = len(neighbors[i])
            if n_neighbors:
                neighbor_sum_vel = np.zeros(2)
                for j in neighbors[i]:
                    neighbor_sum_vel += boids[j].v

                neighbor_avg_vel = neighbor_sum_vel/n_neighbors


                boid.steer(functions.normalize(neighbor_avg_vel - boid.v)*ALIGNMENT_WEIGHT) #.9#4. when alone
                #wander align 3.
                #all together 2.5

    def cohesion(self):

        boids = list(self.all_boids)
        neighbors = [[] for boid in boids]

        #find neighbors
        for i,boid in enumerate(boids):
            for j,neighbor_boid in enumerate(boids):
                if boid == neighbor_boid:
                    continue
                elif functions.dist(boid.pos, neighbor_boid.pos) < RADIUS_VIEW:
                    neighbors[i].append(j)
                    neighbors[j].append(i)

        for i, boid in enumerate(boids):
            n_neighbors = len(neighbors[i])
            if n_neighbors:
                neighbor_sum_pos = np.zeros(2)
                for j in neighbors[i]:
                    neighbor_sum_pos += boids[j].pos

                neighbor_avg_pos = (neighbor_sum_pos/n_neighbors - boid.pos)
                boid.steer(functions.normalize(neighbor_avg_pos - boid.v)*COHESION_WEIGHT) #0.5 #when aline 4.
                #wander + cohesion 18.
                #all together 5.9

    def separate_single(self, boid):
        number_of_neighbors = 0
        force = np.zeros(2)
        for neighbor_boid in self.all_boids:
            distance = functions.dist(boid.pos, neighbor_boid.pos)
            if boid == neighbor_boid:
                continue
            elif distance < RADIUS_VIEW:
                difference = boid.pos - neighbor_boid.pos
                difference /= distance
                force += difference
                number_of_neighbors +=1
            # elif pygame.sprite.collide_rect(boid, other_boid):
            #     force -= other_boid.pos - boid.pos
            #     number_of_neighbors += 1
        if number_of_neighbors:
            force /= number_of_neighbors
        boid.steer(functions.normalize(force)*SEPERATION_WEIGHT) #with align 1. alone 10.
        #wander plus seperate 40.
        #all together 5.


    def separate(self):
        for boid in self.all_boids:
            self.separate_single(boid)


    def avoid_obstacle(self):
        for boid in self.all_boids:
            for obstacle in self.obstacles:
                if bool(pygame.sprite.collide_mask(boid,obstacle)):
                    x_col, y_col = pygame.sprite.collide_mask(boid,obstacle)
                    x, y = boid.pos
                    x_ob, y_ob = obstacle.pos
                    if obstacle.outside:
                        if x>=x_ob:
                            boid.pos[0] += x_col*MOVE
                        elif x <x_ob :
                            boid.pos[0] -= x_col*MOVE

                        if y >=y_ob:
                            boid.pos[1] +=y_col*MOVE
                        elif y <y_ob:
                             boid.pos[1] -=y_col*MOVE
                    else:
                        if x <= x_ob:
                            boid.pos[0] += x_col*MOVE
                        elif x > x_ob:
                            boid.pos[0] -= x_col*MOVE

                        if y <= y_ob:
                            boid.pos[1] += y_col*MOVE
                        elif y > y_ob:
                            boid.pos[1] -= y_col*MOVE

                    #unit vector which is rotated as compared to the original velocity times the previous magnitude
                    boid.v = (functions.rotate(functions.normalize(boid.v))*functions.norm(boid.v)) #5.
                    boid.steering = np.zeros(2)



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
        if self.implement_obstacle: self.avoid_obstacle()
        #it matters where the obstacle avoidance is places as it teleports the agent and changes the direction of its velocity
        if self.wander_selected: self.wander()
        if self.align_selected: self.align()
        if self.cohesion_selected: self.cohesion()
        if self.separate_selected: self.separate()


        self.remain_in_screen()

        for boid in self.all_boids:
            boid.update()



    def display(self, screen):
        for obstacle in self.obstacles:
            obstacle.display(screen)
        for boid in self.all_boids:
            boid.display(screen, debug=False)
        for boid in self.all_boids:
            boid.reset_frame()
