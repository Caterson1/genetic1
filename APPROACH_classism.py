import math

from APPROACH_contants import *
from vectors import *


class Ball:
    def __init__(self, angle: float, startpos:Vec = Vec(), speed: int = 10, color: Vec = None, wind: Vec = Vec(), spin:Vec = Vec()):
        self.pos = startpos
        self.pos_init = startpos
        self.speed = speed
        self.speedinit = speed
        self.v = vectorize(speed, angle)
        self.a = g
        self.forces = [Vec()]
        self.angle = angle
        self.m = 0.045
        self.range = None
        self.r = 0.021335
        self.wind = wind
        self.A = math.pi * (self.r ** 2)
        self.spin = spin
        self.failed = True
        self.vx = None
        if color is None:
            self.color = (randvec()*255).__abs__()
        else:
            self.color = color


    def step(self):
        if self.range == None:
            self.pos += self.v * dt
            self.v += self.a * dt
            self.a = g + ((self.magnus() + self.drag())/ self.m)
            if self.pos.y <= 0:
                self.range = abs(mag(self.pos - Vec(160, 0)))
                self.vx = self.v.x
                return True
            else:
                return False

    def spin_attrition(self):
        if mag(self.spin)  != 0:
            self.spin.z = (abs(self.spin.z) - attrition*dt) * (self.spin.z / abs(self.spin.z))
            if self.spin.z <= 0:
                self.spin.z = 0
        return

    def magnus(self):
        vba = self.v - self.wind
        return (self.spin.cross(b=vba))*magnus_coeff

    def drag(self):
        vba = self.v - self.wind
        return 0.5*(0.2 * air_density * self.A * (mag(vba))**2) * -norm(vba)

    def variedcopy(self, randomness):
        new_angle = random.gauss(self.angle, randomness)
        new_color = (self.angle - new_angle) / 90 * self.color + self.color
        return Ball(new_angle, self.pos_init, self.speed,
                    color=new_color, wind=self.wind, spin=self.spin)

    def __repr__(self):
        return f"Ball with {self.wind} that landed with an x vel of {self.vx} landed {self.range}m away from the target. Angle equaled: {self.angle}m/s"


class Population:
    def __init__(self, popsize, randomness, defaultball: Ball, survival_rate = 10):
        self.population = [Ball(random.randrange(0, 90), defaultball.pos, mag(defaultball.v), wind=defaultball.wind, spin=defaultball.spin) for i in range(popsize)]
        self.randomness = randomness
        self.survivalrate = survival_rate // 100
        self.defaultball = defaultball
        self.landed = []

    def all_landed(self):
        for x in self.population:
            if x.range == None:
                return False
        else:
            return True

    def reproduction(self):
        new_pop = []
        self.population = sorted(self.population, key = lambda x: x.range - x.vx)
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
            self.randomness *= .3
            return True
        else:
            return False

