import numpy as np
import math
import matplotlib.pyplot as plt


class RandomNumberTestCase: 


    def getRegressionPlot(self, numbers):
        indices = np.arange(0, len(numbers))

        plt.scatter(indices, numbers, label = 'Random Numbers')
        plt.xlabel('Index Number')
        plt.ylabel('Value')
        plt.legend(loc = 'lower left')
        plt.title('Regression plot for a list of random numbers')
        plt.show()


    def getHistogramPlot(self, numbers, indicesPerBin):

        numberOfBins = math.ceil(len(numbers) / indicesPerBin)

        plt.hist(numbers, bins=numberOfBins)

        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.grid(axis='y')
        plt.title('Histogram plot for a list of random numbers')
        plt.show()


    def getPhasePlot(self, numbers):

        copiedNumbers = numbers.copy()
        copiedNumbersList = copiedNumbers.tolist()
        copiedNumbersList.pop()

        #we need to use copiedNumbers to generate a new array from numbers[1] to numbers[end]. 
        #then be able to plot numbers[0] to numbers[end-1] vs the new array

        newArr = [numbers[i+1] for i in range(len(copiedNumbersList))]    

        plt.scatter(copiedNumbersList, newArr)
        plt.xlabel('r_i')
        plt.ylabel('r_(i+1)')
        plt.title('Phase plot for a list of random numbers')
        plt.show()



    def getKthMoment(self, numbers, k):

        numberOfNumbers = len(numbers)
        kthMoment = 0

        for number in numbers:
            kthMoment += number**k

        kthMoment /= numberOfNumbers
        return kthMoment


    def getOrderOfKthMoment(self, numbers, k):

        #Note, for this to be accurate, numbers must be normalised (i.e between 0 and 1)

        N = len(numbers)

        kThMoment = self.getKthMoment(numbers, k)
        temp = kThMoment - (1/(k+1))
        return np.sqrt(N) * np.abs(temp)


    def getNearestNeighbourCorrelation(self, numbers, k):

        normalisationConst = 1/len(numbers)
        result = 0

        for i in range(0,len(numbers)-k):
            result += numbers[i]*numbers[i+k]

        result *= normalisationConst
        return result




class LinearCongruenceRNG(RandomNumberTestCase): 

    def __init__(self, randSeed, a, c, maxPlusOne, N):

        self.randomSeed = randSeed
        self.a = a
        self.c = c
        self.maxPlusOne = maxPlusOne
        self.N = N

    def generateNextRN(self, currentRN): 
            return (self.a * currentRN + self.c) % self.maxPlusOne



    def generateRandomNumbers(self):

        currentRandNo = self.randomSeed
        randomNumbers = np.zeros(self.N)
        randomNumbers[0] = currentRandNo

        for i in range(1,self.N):

            currentRandNo = self.generateNextRN(currentRandNo)
            randomNumbers[i] = currentRandNo

        return randomNumbers


    def generateNormalisedRandomNumbers(self):
        
        randomNumbers = self.generateRandomNumbers()
        return randomNumbers / (self.maxPlusOne - 1)



def main():

    testRandomNumberGen = LinearCongruenceRNG(10, 57, 1, 256, 200)

    myRandomNumbers = testRandomNumberGen.generateNormalisedRandomNumbers()



    #Tests 


    #Graphical tests


    # testRandomNumberGen.getRegressionPlot(myRandomNumbers)

    testRandomNumberGen.getPhasePlot(myRandomNumbers)

    # testRandomNumberGen.getHistogramPlot(myRandomNumbers, 20)


    #Numerical tests

    # kthMomentTest = testRandomNumberGen.getOrderOfKthMoment(myRandomNumbers, 3)
    # #Should be on the order of 1

    # nearestNeighbourTest = testRandomNumberGen.getNearestNeighbourCorrelation(myRandomNumbers, 3)

    # print('kth moment test gives' + ' {}'.format(round(kthMomentTest, 5)))

    # print('nearest nieghbour correlation =' + ' {}'.format(round(nearestNeighbourTest, 5)))


if __name__ == '__main__': 

    main()
