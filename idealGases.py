import numpy as np
import matplotlib.pyplot as plt
import RungeKutta as rk
import sys


GAS_CONST = 8.31446261815324


class IdealGas: 

    #one mole

    def __init__(self, volume, temperature, gamma):

        self.T = temperature
        self.V = volume
        self.gamma = gamma
        self.P = GAS_CONST*self.T/self.V


    
    def getCarnotCyclePVPlot(self, carnotVolumes, step): 

        self.checkValidCarnotCycle(carnotVolumes)

        V1 = self.V

        isothermalExpansionVol, isothermalExpansionPress = self.getIsothermalPVData(carnotVolumes.V2, step)


        plt.plot(isothermalExpansionVol, isothermalExpansionPress/1000, label = 'Isothermal Expansion')

        self.updateVolume(carnotVolumes.V2)
        self.updatePressure(isothermalExpansionPress[-1])

        adiabaticExpansionVol, adiabaticExpansionPress = self.getAdiabaticPVData(carnotVolumes.V3, step)

        plt.plot(adiabaticExpansionVol, adiabaticExpansionPress/1000, label = 'Adiabatic Expension')

        self.updateVolume(carnotVolumes.V3)
        self.updatePressure(adiabaticExpansionPress[len(adiabaticExpansionPress) - 1])
        self.updateTemperature(self.getCurrentTemperature(self.P, self.V))

        #now the expansions are done, gas undergoes isothermal compression, since volume decreases, the step must be negative for
        #np.arange to work correctly.

        step *= -1

        isothermalCompressionVol, isothermalCompressionPress = self.getIsothermalPVData(carnotVolumes.V4, step)

        plt.plot(isothermalCompressionVol, isothermalCompressionPress/1000, label = 'Isothermal Compression')

        self.updateVolume(carnotVolumes.V4)


        adiabaticCompressionVol, adiabaticCompressionPress = self.getAdiabaticPVData(V1, step)
        self.updateVolume(V1)

        plt.plot(adiabaticCompressionVol, adiabaticCompressionPress/1000, label = 'Adiabatic Compression')

        plt.legend(loc = 'best')
        plt.title('P-V curve of a Carnot Cycle for an ideal gas')
        plt.xlabel('Volume (m^3)')
        plt.ylabel('Pressure (kPa)')
        plt.grid()
        plt.show()

    



    def checkValidCarnotCycle(self, carnotVolumes):

        ratio_21 = carnotVolumes.V2 / self.V
        ratio_34 = carnotVolumes.V3/carnotVolumes.V4

        if ratio_21 != ratio_34:
            sys.exit('Cannot compute Carnot Cycle: A valid Carnot Cycle must have the ratio of volumes V2/V1 = V3/V4')



    def getIsothermalPVData(self, finalVolume, step):

        volumesData = np.arange(self.V, finalVolume + step, step)
        pressuresData = self.getCurrentIsothermalPressure(volumesData)

        return volumesData, pressuresData

    
  
    def getAdiabaticPVData(self, finalVolume, step):

        volumesData = np.arange(self.V, finalVolume + step, step)
        pressuresData = self.getCurrentAdiabaticPressure(volumesData)

        return volumesData, pressuresData



    def getIsothermalWorkDone(self, finalVolume, relativeTol):

        workDone = rk.getDefiniteIntegralValue_RK(self.getCurrentIsothermalPressure, self.V, finalVolume, 0, relativeTol)
        return workDone
    

    def getAdiabaticWorkDone(self, finalVolume, relativeTol):

        workDone = rk.getDefiniteIntegralValue_RK(self.getCurrentAdiabaticPressure, self.V, finalVolume, 0, relativeTol)
        return workDone


    
    def getCurrentIsothermalPressure(self, currentVolume, placeholder = 0):

        #placeholder required to meet requirements of runge kutta integration for work done. Uses optional argument syntax so doesnt need to be specified when calling

        return GAS_CONST*self.T/currentVolume

    

    def getCurrentAdiabaticPressure(self, currentVolume, placeholder = 0):

        return (self.getAdiabaticConst())/ (currentVolume ** self.gamma)


    def getAdiabaticConst(self): 

        return (GAS_CONST*self.T) * (self.V ** (self.gamma - 1)) 


        

    def getCurrentTemperature(self, currentP, currentV):

        return currentP * currentV / GAS_CONST


    def updateVolume(self, newVolume):

        self.V = newVolume

    def updateTemperature(self, newTemperature):

        self.T = newTemperature

    def updatePressure(self, newPressure):

        self.P = newPressure


    def getHeatChangesInCarnotCycle(self, carnotVolumes, relativeTol, step):

        initialP, initalV, initialT = self.saveCurrentState()

        Q_h = self.getIsothermalWorkDone(carnotVolumes.V2, relativeTol)
        self.updateVolume(carnotVolumes.V2)
        P2 = GAS_CONST * self.T * carnotVolumes.V2 
        self.updatePressure(P2)

        #undergo adiabatic expansion to get to Tc and then get work done to get to V3 from V4 at Tc

        adiabaticVolData, adiabaticPressData = self.getAdiabaticPVData(carnotVolumes.V3, step)

        T_c = adiabaticPressData[-1]*carnotVolumes.V3/ GAS_CONST


        self.updateTemperature(T_c)
        self.updateVolume(carnotVolumes.V3)
        pressure = GAS_CONST*T_c/carnotVolumes.V3
        self.updatePressure(pressure)

        Q_c = self.getIsothermalWorkDone(carnotVolumes.V4, relativeTol)
        self.restorePreviousState(initialP, initalV, initialT)

        return Q_h, Q_c




    def getWorkDoneInCarnotCycleStages(self, carnotVolumes, relativeTol, step):

        initialP, initialV, initialT = self.saveCurrentState()
        Q_h, Q_c = self.getHeatChangesInCarnotCycle(carnotVolumes, relativeTol,step)
        W_1 = -Q_h
        W_3 = -Q_c

        #work done in adiabatic process from V2 to V3 
        self.updateVolume(carnotVolumes.V2)
        P2 = GAS_CONST * self.T / carnotVolumes.V2
        self.updatePressure(P2)

        W_2 = self.getAdiabaticWorkDone(carnotVolumes.V3, relativeTol)

        #then from V4 to V1, first need to undergo adiabatic to get to Tc
        adiabaticVolData, adiabaticPressData = self.getAdiabaticPVData(carnotVolumes.V3, step)

        T_c = adiabaticPressData[-1]*carnotVolumes.V3 / GAS_CONST
        self.updateTemperature(T_c)
        pressure = GAS_CONST*T_c / carnotVolumes.V4
        self.updatePressure(pressure)

        W_4 = self.getAdiabaticWorkDone(initialV, relativeTol)

        self.restorePreviousState(initialP, initialV, initialT)
        return W_1, W_2, W_3, W_4


    def getCarnotUsefulWorkDone(self, carnotVolumes, relativeTol, step): 

        Q_h, Q_c = self.getHeatChangesInCarnotCycle(carnotVolumes, relativeTol, step)
        return Q_h + Q_c





    def getCarnotEfficiencyViaTemperatures(self, carnotVolumes, step):

        self.checkValidCarnotCycle(carnotVolumes)
        initialP, initialV, initialT = self.saveCurrentState()


        self.updateVolume(carnotVolumes.V2)
        adiabaticVolData, adiabaticPressData = self.getAdiabaticPVData(carnotVolumes.V3, step)

        T_c = adiabaticPressData[-1]*carnotVolumes.V3/ GAS_CONST
        efficiency = 1 - T_c/initialT
        self.restorePreviousState(initialP, initialV, initialT)

        return efficiency




    def getCarnotEfficiencyViaHeatTransfers(self, carnotVolumes, relativeTol, step):

        Qh, Qc = self.getHeatChangesInCarnotCycle(carnotVolumes, relativeTol, step)

        return 1 + Qc/Qh
    

    def saveCurrentState(self):

        return self.P, self.V, self.T


    def restorePreviousState(self, previousP, previousV, previousT):

        self.updatePressure(previousP)

        self.updateVolume(previousV)

        self.updateTemperature(previousT)

        


class CarnotCycleVolumeContainer:

    def __init__(self, V2, V3, V4):

        self.V2 = V2
        self.V3 = V3
        self.V4 = V4



def main():

    V2 = 0.01
    V3 = 0.015
    V4 = 0.0075

    myCarnotVolumes = CarnotCycleVolumeContainer(V2, V3, V4)

    myIdealGas = IdealGas(0.005, 320, 5/3)


    #PV plot

    # myIdealGas.getCarnotCyclePVPlot(myCarnotVolumes, 0.0001)

    #heat transfers

    # Qh, Qc = myIdealGas.getHeatChangesInCarnotCycle(myCarnotVolumes, 0.001, 0.0001)

    # print('Heat in = ' + str(Qh) + ' J')

    # print('Heat out = ' + str(Qc) + ' J')


    #work done in each process 

    # W1, W2, W3, W4 = myIdealGas.getWorkDoneInCarnotCycleStages(myCarnotVolumes, 0.001, 0.0001)

    # print('W1 = ' + str(W1) + " J")
    # print('W2 = ' + str(W2) + " J")
    # print('W3 = ' + str(W3) + " J")
    # print('W4 = ' + str(W4) + " J")



    #efficiencies - calculable through two methods:

    eff_heat = myIdealGas.getCarnotEfficiencyViaHeatTransfers(myCarnotVolumes, 0.0001, 0.0001)
    eff_temp = myIdealGas.getCarnotEfficiencyViaTemperatures(myCarnotVolumes, 0.00001)

    print('eff_heat = ' + str(eff_heat))
    print('eff_temp = ' + str(eff_temp))



if __name__ == '__main__':
    main()
        







        

        
