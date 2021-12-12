# Collin Paiz
# COEN 148 Computer Graphics Assignment 2
# 31 October 2021
# Takes vertices and displays them on screen as points or as triangles
# Ensure the .txt and .data files have no empty lines at the end of the files

# import modules
import cv2              # image control
import numpy            # arrays
import math             # math functions
import csv              # file control

# global variables
vertView = True
imgSize = 640
imgCenter = int(imgSize/2)
d = 5
size = imgSize
pixels = numpy.zeros((imgSize, imgSize, 3), numpy.uint8)

# reference x
def refX(theta):
    cos = math.cos(theta)
    sin = math.sin(theta)
    for i in range(len(vertices)):
        vertex = vertices[i]
        pnt = [0.0, 0.0, 0.0]
        pnt[0] = vertex[0]
        pnt[1] = cos*vertex[1] - sin*vertex[2]
        pnt[2] = sin*vertex[1] + cos*vertex[2]
        vertices[i] = pnt

# reference y
def refY(theta):
    cos = math.cos(theta)
    sin = math.sin(theta)
    for i in range(len(vertices)):
        vertex = vertices[i]
        pnt = [0.0, 0.0, 0.0]
        pnt[0] = vertex[2]*sin + vertex[0]*cos
        pnt[1] = vertex[1]
        pnt[2] = -sin*vertex[0] + cos*vertex[2]
        vertices[i] = pnt

# clean points/lines from window
def clean():
    global pixels

    # reset pixel array
    pixels = numpy.zeros((imgSize, imgSize, 3), numpy.uint8)

# draw vertices by pixel
def drawPixel(x, y, color):
    # if within img bounds, set pixel color at coordinate
    if((x >= 0) and (x < imgSize) and (y >= 0)and (y < imgSize)):
        pixels[int(y)][int(x)][0] = color

# plot vertices relative to imgSize
def plotVerts():
    # x', y'
    for vertex in vertices:
        zd = float(vertex[2]) / d
        xp = int(size*vertex[0] / (1+zd))
        yp = int(size*vertex[1] / (1+zd))

        # plot pixel
        drawPixel(imgCenter+xp, imgCenter-yp, 255)

# plot tris from current index of points
def plotTris(a, b, c):
    # x1', y1'
    zd1 = vertices[a][2] / d
    xp1 = int(size*vertices[a][0] / (1+zd1))
    yp1 = int(size*vertices[a][1] / (1+zd1))

    # x2', y2'
    zd2 = vertices[b][2] / d
    xp2 = int(size*vertices[b][0] / (1+zd2))
    yp2 = int(size*vertices[b][1] / (1+zd2))

    # x3', y3'
    zd3 = vertices[c][2] / d
    xp3 = int(size*vertices[c][0] / (1+zd3))
    yp3 = int(size*vertices[c][1] / (1+zd3))

    # draw lines
    cv2.line(pixels, (imgCenter+xp1, imgCenter-yp1), (imgCenter+xp2, imgCenter-yp2), (255, 255, 0))
    cv2.line(pixels, (imgCenter+xp1, imgCenter-yp1), (imgCenter+xp3, imgCenter-yp3), (255, 255, 0))
    cv2.line(pixels, (imgCenter+xp3, imgCenter-yp3), (imgCenter+xp2, imgCenter-yp2), (255, 255, 0))

# plot lines from index of points
def plotLines():
    for index in indexes:
        plotTris(int(index[0]), int(index[1]), int(index[2]))

# view view
def view():
    clean()

    # control key
    cv2.putText(pixels, "esc: exit", (0,20), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255))
    cv2.putText(pixels, "v: change view", (0,50), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255))

    # vertices, else tris
    if vertView:
        plotVerts()
    else:
        plotLines()

    # show image
    cv2.imshow("image", pixels)

# main function
if __name__ == '__main__':

    # initialize lists
    vertices = []
    indexes = []

    # open and read face-vertices.data
    with open('face-vertices.data') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        # add vertices to vertices list
        for row in csv_reader:
            vertices.append([float(x) for x in row])

    # open and read face-index.txt
    with open('face-index.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        # add indexes to indexes list
        for index in csv_reader:
            indexes.append(index)

    # eye (change to view from different angles)
    refX(45/180 * math.pi)
    refY(45/180 * math.pi)

    # view view window
    view()

    # change view, quit
    while True:
        input = cv2.waitKey(0)
        if input == 27:                 # esc to quit
            #print("quit")
            cv2.destroyAllWindows()
            break
        if input == 118:                # v to change view
            vertView = not vertView
            view()

# end