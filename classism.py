import math

from contants import *
from vectors import *


class Ball:
    def __init__(self, angle: float, startpos:Vec = Vec(), speed: int = 10, color: Vec = None, wind: Vec = Vec()):
        self.pos = startpos
        self.pos_init = startpos
        self.speed = speed
        self.v = vectorize(speed, angle)
        self.a = g
        self.forces = [Vec()]
        self.angle = angle
        self.m = 4.2
        self.range = None
        if color is None:
            self.color = (randvec()*255).__abs__()
        else:
            self.color = color
        self.r = 0.125
        self.wind = wind

    def step(self):
        if self.range == None:
            self.pos += self.v * dt
            self.v += self.a * dt
            self.a = g + sum(self.forces, Vec())+ self.drag()/ self.m
            if self.pos.y <= 0:
                self.range = self.pos.x

    def drag(self):
        return (0.3*air_density*math.pi*(self.r**2)*mag(self.v - self.wind)**2) * -norm(self.v)

    def variedcopy(self, randomness):
        new_angle = random.gauss(self.angle, randomness)
        new_color = (self.angle - new_angle)/90 * self.color + self.color
        return Ball(new_angle, self.pos_init, self.speed,
                    color=new_color)

class Population:
    def __init__(self, popsize, randomness, defaultball: Ball, survival_rate = 10):
        self.population = [Ball(random.randrange(0, 90), defaultball.pos, mag(defaultball.v)) for i in range(popsize)]
        self.randomness = randomness
        self.survivalrate = survival_rate // 100

    def all_landed(self):
        for ball in self.population:
            if ball.range is None:
                return False
        return True

    def reproduction(self):
        new_pop = []
        self.population = sorted(self.population, key = lambda x: x.range, reverse=True)
        for x in self.population[0:10]:
            print(x.angle)
            for xx in range(10):
                new_pop.append(x.variedcopy(self.randomness))
        self.population = new_pop

    def step(self):
        for ball in self.population:
            ball.step()
        if self.all_landed():
            self.reproduction()
            self.randomness *= .5
            return True
        else:
            return False




