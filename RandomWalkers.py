import numpy as np
import math
import matplotlib.pyplot as plt
import random as rnd




class RandomWalker: 

    def __init__(self, normalised = True):
        self.normalised = normalised



    def getRandomWalkValue(self):

        num = (rnd.random() - 0.5)*2
        normalisationConst = abs(num) if self.normalised == True else 1
        num /= normalisationConst

        return num





class TwoDRandomWalker(RandomWalker):

    def __init__(self, steps, normalised=True):

        super().__init__(normalised)
        self.steps = steps



    def getTwoDRandomWalkValues(self):

        x = np.zeros(self.steps)
        y = np.zeros(self.steps)

        for i in range(1,self.steps):

            randomX = self.getRandomWalkValue()
            randomY = self.getRandomWalkValue()

            x[i] = x[i-1] + randomX
            y[i] = y[i-1] + randomY

        return x,y


    def plotRandomWalkValues(self):

        walkX, walkY = self.getTwoDRandomWalkValues()

        finalX = walkX[self.steps-1]
        finalY = walkY[self.steps-1]

        plt.plot(walkX, walkY, '-o')
        plt.arrow(0, 0, finalX, finalY, color = 'red', linewidth = 1)

        plt.xlabel('x position')
        plt.ylabel('y position')
        plt.title('Illustration of a 2D random walk')
        plt.show()

        

    def calculateRandomDistance(self):

        walkX, walkY = self.getTwoDRandomWalkValues()
        finalX = walkX[self.steps-1]
        finalY = walkY[self.steps-1]

        return math.sqrt(finalX**2 + finalY**2)


    def getRandomDistances(self, numberOfTrials):

        distances = [self.calculateRandomDistance() for _ in range(numberOfTrials)]
        return distances



    def calculateAverageDistance(self, numberOfTrials):

        distances = self.getRandomDistances(numberOfTrials)
        return sum(distances)/numberOfTrials


   

class MultipleTwoDrandomWalkers: 

    def __init__(self, stepNumbers, numberOfTrials, normalised = True):

        self.numberOfTrials = numberOfTrials
        self.normalised = normalised
        self.stepNumbers = stepNumbers
        self.randomWalkers = []

        for i in range(len(stepNumbers)):
            self.randomWalkers.append(TwoDRandomWalker(stepNumbers[i], normalised))



    def plotAverageDistances(self):

        sqrtStepNumbers  = np.sqrt(self.stepNumbers)

        averageDistances = [self.randomWalkers[i].calculateAverageDistance(self.numberOfTrials) for i in range(len(self.stepNumbers))]
     
        plt.plot(sqrtStepNumbers, averageDistances, '-o')
        plt.xlabel('sqrt(N)')
        plt.ylabel('R_av')
        plt.title('Plot of mean distance vs sqrt(N) for a set of 2D random walks of steps ' + str(self.stepNumbers))

        plt.show()




def main():

    myWalk = TwoDRandomWalker(100)

    # #illustration of normalised random walk
    # myWalk.plotRandomWalkValues()


    #testing linearity of R_av vs sqrt(N) 
    myStepNumbers = [100,1000,2000, 4000, 6000, 8000, 10000]
    myWalkTrials = MultipleTwoDrandomWalkers(myStepNumbers, 100)
    myWalkTrials.plotAverageDistances()



if __name__ == '__main__':

    main()
          