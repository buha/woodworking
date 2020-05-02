#!/usr/bin/python3
import math
import numpy as np
from scipy.special import *
import matplotlib.pyplot as plt
np.seterr(divide='ignore', invalid='ignore')

def distance(p1, p2):
    return np.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)

# inputs
r = 75
a = 40
h = -115
t = 475

# generate a bunch of gamma angles
g = np.linspace(0, 90, 901)

# equation of the chisel position / orientation
m = -cotdg(g + a) 
c = r * sindg(g) - m * r * cosdg(g)
xt = (h - c) / m

# contact point coordinates
xr = r * cosdg(g)
yr = r * sindg(g)

# computed lengths from chisel-stone to chisel-jig contact points
lvalues = np.sqrt((xt - xr) ** 2 + (h - yr) ** 2)
lmaxi = np.argmax(lvalues)
lvalues = lvalues[:lmaxi] # discard values without physical meaning

# deltas between these lengths and given tool length
deltas = lvalues - t

# numeric search of the smallest delta
li = np.argmin(abs(deltas))
l = lvalues[li]

# tangent m and c from y = m * x + c
mtan = -cotdg(g[li])
ctan = r / sindg(g[li])

# compute tool length based on results
point1 = [xr[li], yr[li]]
point2 = [xt[li], h]
tcomp = distance(point1, point2)
if tcomp / t > 1.01:
    print("computed t = {} mm".format(tcomp))
    print("Couldn't find a solution.");
    exit()

# compute alpha based on results
point1 = [xt[li], h]
point2 = [xr[li], yr[li]]
point3 = [(h - ctan) / mtan, h]
A = distance(point1, point2)
B = distance(point2, point3)
C = distance(point3, point1)
alpha = np.arccos((A ** 2 + B ** 2 - C ** 2) / 2 / A / B)
alpha = alpha * 180 / np.pi
if abs(alpha - a) > 1 or alpha != alpha:
    print("computed alpha = {:.1f} deg".format(alpha))
    print("Couldn't find a solution.");
    exit()
print("alpha = {:.1f} deg".format(alpha))

# draw circle
circle1 = plt.Circle((0, 0), r)
fig, ax = plt.subplots()
ax.add_artist(circle1)

# draw jig
point1 = [0, h]
point2 = [xt[li], h]
x_values = [point1[0], point2[0]]
y_values = [point1[1], point2[1]]
plt.plot(x_values, y_values, color='r', label="distancer jig: {:.1f} mm".format(xt[li]))

# draw tool
point1 = [xr[li], yr[li]]
point2 = [xt[li], h]
x_values = [point1[0], point2[0]]
y_values = [point1[1], point2[1]]
plt.plot(x_values, y_values, color='g', label="chisel: {:.1f} mm".format(lvalues[li]))

# draw tangent
point1 = [0, ctan]
point2 = [(h - ctan) / mtan, h]
x_values = [point1[0], point2[0]]
y_values = [point1[1], point2[1]]
plt.plot(x_values, y_values, linestyle='dashed', label="circle tangent at contact point")

s = 3
ax.set(xlim=(-s * r, xt[li] + r), ylim = (- s * r, s * r))
plt.gca().set_aspect('equal', adjustable='box')
plt.legend(loc="upper left")
plt.show()
