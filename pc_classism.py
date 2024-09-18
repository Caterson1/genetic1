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
        self.angle = angle
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
            self.a = g + (self.drag()/ self.m)
            if self.pos.y <= 0:
                self.range = self.pos.x
                return True
            else:
                return False

    def drag(self):
        vba = self.v - self.wind
        return 0.5*(0.3 * air_density * self.A * (mag(vba))**2) * -norm(vba)

    def variedcopy(self, randomness):
        new_angle = random.gauss(self.angle, randomness)
        new_color = (self.angle - new_angle)/90 * self.color + self.color
        return Ball(new_angle, self.pos_init, self.speed,
                    color=new_color, wind=self.wind)
    def __repr__(self):
        return f"Ball with wind speed {self.wind} travelled {self.range}m from angle {self.angle}"

class Population:
    def __init__(self, popsize, randomness, defaultball: Ball, survival_rate = 10):
        self.population = [Ball(random.randrange(0, 90), defaultball.pos, mag(defaultball.v), wind=defaultball.wind) for i in range(popsize)]
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
        print(self.population[0])
        for x in self.population[0:10]:
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

