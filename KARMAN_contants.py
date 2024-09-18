from vectors import *

dt = 0.001
g = Vec(0, -9.81)
air_density = 0.97

def airdensity(height):
    if height < 11000:
        t = 15.04 - (0.00649 * height)
        return (101.29 * ((t + 273.1) / 288.08)**5.26) / (0.2869 * (t + 273.1))
    elif height < 25000:
        t = -56.46
        return (22.65 * math.e ** (1.73 - 0.000157 * height)) / (0.2869 * (t + 273.1))
    else:
        t = -131.21 + 0.00299 * height
        return (2.488 * ((t + 273.1)/216.6) ** -11.388) / (0.2869 * (t + 273.1))

print(airdensity(3000))