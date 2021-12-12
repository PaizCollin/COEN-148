# Collin Paiz
# COEN 148 - Computer Graphics
# Assignment 3 - Raycasting
# 10 December 2021
# The following code utilizes the raycasting algorithm to find intersection points from the camera
# to the objects in the scene. It creates spheres and light sources that have the ability to change 
# position, color, and scale; and each object casts shadows/is affected by the light source(s). After
# initializing the objects, lights and camera, it draws each pixel based on the intersections.

import numpy as np
from PIL import Image
from math import sqrt

# init global vars
MAXITER = 6
WIDTH = 640
HEIGHT = 480
FPFIXER = 0.00000000001

# position class
class pos:
    def __init__(self, x, y, z):
        self.arr = np.array([x, y, z], dtype = float)

    def __add__(self, other):
        arr = self.arr + other.arr
        return pos(arr[0], arr[1], arr[2])

    def __sub__(self, other):
        arr = self.arr - other.arr
        return pos(arr[0], arr[1], arr[2])

    def __mul__(self, other):
            arr = np.multiply(self.arr, other)
            return pos(arr[0], arr[1], arr[2])

    def dot(self, other):
        return np.dot(self.arr, other.arr)

    def length(self):
        return sqrt(np.dot(self.arr, self.arr))

    def cosine(self, other):
        return self.dot(other) / (self.length()*other.length())

# color class
class color:
    def __init__(self, r, g, b):
        self.arr = np.array([r, g, b], dtype = int)

    def __add__(self, other):
        arr = self.arr + other.arr
        for i in range(3):
            if arr[i] > 255:
                arr[i] = 255
        return color(arr[0], arr[1], arr[2])

    def __mul__(self, other):
        arr = np.multiply(self.arr, other)
        for i in range(3):
            if arr[i] < 0:
                arr[i] = 0
            if arr[i] > 255:
                arr[i] = 255
        return color(arr[0], arr[1], arr[2])

    def __eq__(self, other):
        return self.arr.all() == other.arr.all()

    def shd(self, other):
        arr = np.array([0, 0, 0], dtype = int)
        for i in range(3):
            arr[i] = int(self.arr[i] * other.arr[i] / 255)
        return color(arr[0], arr[1], arr[2])

# instance parent
class instance:
    def __init__(self, x, y, z):
        self.pos = pos(x, y, z)

# light child
class light(instance):
    def __init__(self, x, y, z, r, g, b):       # position, color
        super().__init__(x, y, z)
        self.color = color(r, g, b)

# sphere child
class sphere(instance):
    def __init__(self, x, y, z, r, g, b,        # position, color
                 rad = 1, shine = 8,
                 kar = 200, kag = 200, kab = 200,
                 kdr = 150, kdg = 150, kdb = 150,
                 ksr = 30, ksg = 30, ksb = 30):
        super().__init__(x, y, z)
        self.color = color(r, g, b)
        self.radius = rad
        self.shine = shine
        self.ka = color(kar, kag, kab)
        self.kd = color(kdr, kdg, kdb)
        self.ks = color(ksr, ksg, ksb)

    # determines normal at pos
    def normal(self, pos):
        return pos - self.pos

    # checks for position of intersection
    def intersect(self, o, d):
        a = d.dot(d)
        tmp = o - self.pos
        b = (tmp*2).dot(d)
        c = tmp.dot(tmp) - self.radius**2

        det = b**2 - 4*a*c
        if det < 0:         # no intersections
            return
        t1 = (-sqrt(det)-b) / (2*a)
        t2 = (sqrt(det)-b) / (2*a)

        if t2 < 0:
            return
        if t1 < 0:
            return t2
        return min(t1, t2)

# find direction of object (for camera)
def finddir(w, h, e):
    x = int(WIDTH/2)
    y = int(HEIGHT/2)
    p = pos((w - x) / 1000, 1, (y - h) / 1000)
    p = p - e.pos
    return(p)

# checks for intersections with light
def hits(source, dir, spheres):
    if spheres is None:     # no spheres, no intersections
        return False
    for s in spheres:
        if s.intersect(source, dir):
            return True
    return False

# raycast function
def raycast(source, dir, spheres, lights, n = 0):
    black = color(0, 0, 0)
    Ia = color(20, 20, 20)      # ambient light
    if n == MAXITER:
        return black

    c = black
    min = float("inf")
    sphere = None
    plane = None

    if spheres is None:     # no spheres, black
        return black

    for s in spheres:
        pos = s.intersect(source, dir)
        if pos is not None and pos < min:
            min = pos
            sphere = s

    if sphere is not None:
        intersection = source + dir * (min - FPFIXER)
        norm = sphere.normal(intersection)
        Iu = black
        for li in lights:
            ldir = li.pos - intersection

            # env light
            if hits(intersection, ldir, spheres):
                Ie = black
            else:
                Ie = li.color

            Ia = Ia.shd(sphere.ka)      # ambient light
            Id = Ie.shd(sphere.kd) * ldir.cosine(norm)      # diffuse light
            Iu = Iu + Ia + Id

        c = sphere.color.shd(Iu)

    return(c)

# draw pixel at pixel pos p
def drawpix(p, w, h, c):
    p[w, h] = tuple(c.arr)

# main function
if __name__ == '__main__':
    img = Image.new('RGB', (WIDTH, HEIGHT))
    pixels = img.load()
    cam = instance(0, 0, 0)
    spheres = []
    lights = []
    planes = []

    # removed
    #planes.append(plane(0, 0, -0.5, 255, 255, 255))
    spheres.append(sphere(-1, 16, 0.5, 255, 0, 0, 1))       # red, left
    spheres.append(sphere(0.5, 15, 0, 0, 255, 0, 0.5))      # green, right
    spheres.append(sphere(0, 22, 0.75, 0, 0, 255, 1.5))     # blue, back
    lights.append(light(100, -50, 25, 255, 255, 255))       # light, right

    # for all pixels in img, draw image
    for h in range(HEIGHT):
        for w in range(WIDTH):
            direction = finddir(w, h, cam)
            c = raycast(cam.pos, direction, spheres, lights)
            drawpix(pixels, w, h, c)

    # save and show final result
    img.save("raycast.png")
    img.show()

# end       