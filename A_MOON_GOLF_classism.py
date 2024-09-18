import math

from A_MOON_GOLF_contants import *
from vectors import *


class Ball:
    def __init__(self, angle: float, startpos:Vec = Vec(), speed: int = 10, color: Vec = None, wind: Vec = Vec()):
        self.pos = Vec()
        self.pos_init = startpos
        self.speed = speed
        self.v = vectorize(speed, angle)
        self.a = g
        self.forces = [Vec()]
        self.angle = angle
        self.m = 0.045
        self.range = None
        self.r = 0.021335
        self.wind = wind
        self.A = math.pi * (self.r ** 2)
        self.initspeed = speed
        self.hitcircle = False
        self.mindist = 100
        if color is None:
            self.color = (randvec()*255).__abs__()
        else:
            self.color = color


    def step(self):
        if self.range == None:
            self.pos += self.v * dt
            self.v += self.a * dt
            self.a = g
            if mag(self.pos-Vec(100)) < self.mindist:
                self.mindist = mag(self.pos-Vec(100))
            if self.pos.x <= 50 or self.pos.x >= 150:
                if self.pos.y <= 0:
                    if self.pos.x <= 50:
                        self.hitcircle = True
                    self.range = self.pos.x
                    return True
                else:
                    return False
            else:
                if mag(self.pos - Vec(100)) <= 50:
                    self.range = self.pos.x
                    self.hitcircle = True
                    return True
                else:
                    return False

    def drag(self):
        vba = self.v - self.wind
        return 0.5*(0.3 * air_density * self.A * (mag(vba))**2) * -norm(vba)

    def variedcopy(self, randomness):
        new_speed = random.gauss(self.initspeed, randomness)
        new_angle = random.gauss(self.angle, randomness)
        new_color = (self.angle - new_speed)/90 * self.color + self.color
        return Ball(new_angle, self.pos_init, new_speed,
                    color=new_color, wind=self.wind)
    def __repr__(self):
        return f"Ball with wind speed {self.wind} travelled {self.range}m from speed {self.initspeed} {self.mindist}\n"

class Population:
    def __init__(self, popsize, randomness, defaultball: Ball, survival_rate = 10):
        self.population = [defaultball.variedcopy(randomness) for i in range(popsize)]
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
        pop2 = [x for x in self.population if x.hitcircle is False]
        pop2 = sorted(pop2, key = lambda x: x.initspeed)
        print(pop2[0])
        for x in pop2[0:10]:
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
            self.randomness *= .6
            return True
        else:
            return False

