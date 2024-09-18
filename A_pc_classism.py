import math

from pc_contants import *
from vectors import *


class Ball:
    def __init__(self, angle: float, startpos:Vec = Vec(), speed: int = 10, color: Vec = None, wind: Vec = Vec()):
        self.pos = vectorize(30.48, angle)
        self.pos_init = startpos
        self.speed = speed
        self.v = vectorize(speed, angle)
        self.a = g
        self.forces = [Vec()]
        self.init_split = norm(wind)
        self.m = 4.2
        self.range = None
        self.r = 0.125
        self.wind = wind
        self.A = math.pi * (self.r ** 2)
        if color is None:
            self.color = (randvec()*255).__abs__()
        else:
            self.color = color


    def step(self):
        if self.range == None:
            self.pos += self.v * dt
            self.v += self.a * dt
            self.a = g + (sum(self.forces, Vec()) + self.drag()/ self.m)
            if self.pos.y <= 0:
                self.range = self.pos.x
                return True
            else:
                return False

    def drag(self):
        vba = self.v - self.wind
        return 0.5*(0.3 * air_density * self.A * (mag(vba))**2) * -norm(vba)

    def variedcopy(self, randomness):
        change = randvec()*randomness / 100
        new_color = change + self.color
        return Ball(35, self.pos_init, self.speed,
                    color=new_color, wind=(13.5 * norm(self.init_split + change)))
    def __repr__(self):
        return f"Ball with wind speed {self.wind} travelled {self.range}m from angle {self.init_split}"

class Population:
    def __init__(self, popsize, randomness, defaultball: Ball, survival_rate = 10):
        self.population = [Ball(35, defaultball.pos, mag(defaultball.v), wind=13.5 * randvec()) for i in range(popsize)]
        self.randomness = randomness
        self.survivalrate = survival_rate // 100
        self.landed = []

    def all_landed(self):
        for x in self.population:
            if x.range == None:
                return False
        else:
            return True

    def reproduction(self):
        new_pop = []
        self.population = sorted(self.population, key = lambda x: x.range, reverse=True)
        for x in self.population[0:10]:
            print(x.range, x.wind)
            for xx in range(10):
                new_pop.append(x.variedcopy(self.randomness))
        print("New Population Start --------------------------------------------------------------")
        self.population = new_pop

    def step(self):
        for ball in self.population:
            if ball.step():
                self.landed.append(ball)

        if self.all_landed():
            self.reproduction()
            self.randomness *= .5
            return True
        else:
            return False

