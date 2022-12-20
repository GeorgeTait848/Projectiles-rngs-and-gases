from cProfile import label
from cmath import sqrt
from turtle import color, distance
import numpy as np
import math
import matplotlib.pyplot as plt
import random as rnd
import RandomWalkers as wlk



class Square: 

    def __init__(self, length):

        self.length = length
        self.area = length**2

        self.bottomLeft = [0,0]
        self.topLeft = [0, length]
        self.topRight = [length, length]
        self.bottomRight = [length, 0]



class WalkersOnASquare: 

    def __init__(self, lengthOfSquare, randomWalkers, numberOfTrials):

        if not (type(randomWalkers) == wlk.TwoDRandomWalker):
            raise TypeError('randomWalkers must be of type TwoDrandomWalker')

        self.square = Square(lengthOfSquare)
        self.walkers = randomWalkers
        self.numberOfTrials = numberOfTrials



    def getVertexRav(self):
        return self.walkers.calculateAverageDistance(self.numberOfTrials)


    def calculateMInimumAxisLimits(self):
        return np.sqrt(self.walkers.steps)
        


    def plotRavAsCircles(self):

        axisLimValue = self.calculateMInimumAxisLimits()*2 + self.square.length

        ax = plt.gca()
        ax.set_xlim((-1*axisLimValue, axisLimValue))
        ax.set_ylim((-1*axisLimValue, axisLimValue))

        plottedSquare = plt.Rectangle((0,0), self.square.length, self.square.length, fill = False, label = 'square of sides length {}'.format(self.square.length))

        ax.add_patch(plottedSquare)

        vertices = [self.square.topLeft, self.square.topRight, self.square.bottomLeft, self.square.bottomRight]
        verticesNames = ['top left', 'top right', 'bottom left', 'bottom right']
        colours = ['red', 'blue', 'green', 'orange']



        for i in range(len(vertices)):

            currentRav = self.getVertexRav()
            currentCircle = plt.Circle((vertices[i][0], vertices[i][1]), currentRav, fill = False, label = verticesNames[i], color = colours[i])
            ax.add_patch(currentCircle)
        
        plt.legend()
        plt.title('Average displacement of multiple random walks of' +  ' {}'.format(self.walkers.steps) + ' steps at the verteces of a square of sides' + ' {}'.format(self.square.length))
        plt.show()


def main():

    myRandomWalker = wlk.TwoDRandomWalker(1000)
    myWalkersOnSquare = WalkersOnASquare(10, myRandomWalker, 100)
    myWalkersOnSquare.plotRavAsCircles()


if __name__ == '__main__':
    main()


