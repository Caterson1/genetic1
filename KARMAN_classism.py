import math

from KARMAN_contants import *
from vectors import *


class Ball:
    def __init__(self, angle: float, startpos:Vec = Vec(), speed: int = 10, color: Vec = None, wind: Vec = Vec()):
        self.range = None
        self.pos = startpos
        self.pos_init = startpos
        self.speed = speed
        self.initspeed = speed
        self.v = Vec(0, speed)
        self.a = g
        self.forces = [Vec()]
        self.angle = angle
        self.m = 15
        self.r = 0.08
        self.wind = wind
        self.maxdrag = 0
        self.failed = True
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
            if self.v.y <= 0:
                if self.pos.y > 100000:
                    self.failed = False
                self.range = self.pos.y
                return True
            else:
                return False

    def drag(self):
        vba = self.v - self.wind
        drag = 0.5*(0.5 * airdensity(self.pos.y) * self.A * (mag(vba))**2) * -norm(vba)
        if mag(drag) > self.maxdrag:
            self.maxdrag = mag(drag)
        return drag

    def variedcopy(self, randomness):
        new_speed = random.gauss(self.initspeed, randomness)
        new_color = (self.initspeed - new_speed)/1000 * self.color + self.color
        return Ball(90, self.pos_init, new_speed,
                    color=new_color, wind=self.wind)
    def __repr__(self):
        return f"The cannonball starting at {self.pos_init.y}m travelled {self.range}m from speed {self.initspeed}. The ball experienced {self.maxdrag}N of drag at one point"

class Population:
    def __init__(self, popsize, randomness, defaultball: Ball, survival_rate = 10):
        self.population = [Ball(90, defaultball.pos, random.randrange(1000, 50000), wind=defaultball.wind) for i in range(popsize)]
        self.randomness = randomness
        self.defaultball = defaultball
        self.survivalrate = survival_rate // 100
        self.landed = []
        self.popsize = popsize

    def all_landed(self):
        for x in self.population:
            if x.range is None:
                return False
        else:
            return True

    def reproduction(self):
        new_pop = []
        # for x in self.population:
        #     print(x.pos.y)
        self.population = [x for x in self.population if x.failed is False]
        self.population = sorted(self.population, key = lambda x: x.initspeed)
        try:
            print(self.population[0])
        except:
            print("population failed")
            self.population = [Ball(90, self.defaultball.pos, random.randrange(1000, 100000), wind=self.defaultball.wind) for i in range(self.popsize)]
        else:
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
            self.randomness *= .9
            return True
        else:
            return False

