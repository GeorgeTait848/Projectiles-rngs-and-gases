import numpy as np
import matplotlib.pyplot as plt

g = 9.81


class Projectile:

    def __init__(self, v0, h, theta):

        self.v0 = v0 #initial speed
        self.h = h #height of tower
        self.theta = theta #initial release angle

        #tower assumed to be at x=0

        self.ux = v0*np.cos(theta) #x component of initial velocity

        self.uy = v0*np.sin(theta) #y component of initial velocity


    def getX(self, time):

        return self.ux * time

    def getY(self, time):
        return self.h + self.uy*time -0.5*g*time**2

    def getMotionData(self, timeIncrement = 0.02):

        currentTime = 0

        xValues = []
        yValues = []

        currentYValue = self.getY(currentTime)

        while(currentYValue >= 0):

            currentXValue = self.getX(currentTime)

            xValues.append(currentXValue)
            yValues.append(currentYValue)

            currentTime += timeIncrement
            currentYValue = self.getY(currentTime)
        
        return xValues, yValues



    def getProjectileMotionPlot(self):

        xValues, yValues = self.getMotionData()


        plt.plot(xValues, yValues)
        plt.title('Projectile path from height ' + str(self.h) + ', initial speed ' +  str(self.v0) + ', release angle ' + str(round(self.theta, 3)) + ' rad')
        plt.xlabel('x')
        plt.ylabel('y')

        plt.show()


        

def main():

    myProjectile = Projectile(15, 5, 5*np.pi/12)
    myProjectile.getProjectileMotionPlot()



if __name__ == '__main__':

    main()


    






