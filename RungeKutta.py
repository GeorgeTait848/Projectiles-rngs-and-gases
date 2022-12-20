import numpy as np

def rungeKutta(f, x, y, h):

    K_1 = f(x,y)
    K_2 = f(x + h/2, y + (h * K_1 * 0.5))
    K_3 = f(x + h/2, y + (h * K_2 * 0.5))
    K_4 = f(x + h, y + (h * K_3))

    tot_slope = K_1 + 2*K_2 + 2*K_3 + K_4
    total_change = (h/6)*tot_slope
    new_y = y + total_change

    return new_y


def rungeKuttaArr(f, x, initialy, h):

    currentI = initialy
    integral = np.zeros(len(x))

    for i in range(len(x)):

        currentI = rungeKutta(f, x[i], currentI, h)
        integral[i] = currentI

    return integral




def adaptiveRungeKuttaArr(f, xLowerLim, xUpperLim, initialy, relativeTol):

    x = []
    integral = []
    currentX = xLowerLim
    currentI = initialy
    currentH = 0.01

    while currentX < xUpperLim:
        
        currentH = adaptStep(f,currentX, currentI, currentH, relativeTol)
        currentI = rungeKutta(f, currentX, currentI, currentH)

        x.append(currentX)
        integral.append(currentI)
        currentX += currentH

    
    currentH = xUpperLim - currentX
    currentI = rungeKutta(f,currentX, currentI, currentH)
    x.append(currentX)
    integral.append(currentI)

    return x, integral

def getDefiniteIntegralValue_RK(f, xLowerLim, xUpperLim, initialy, relativeTol):

    currentX = xLowerLim
    currentI = initialy
    currentH = 0.01

    while currentX < xUpperLim:
        
        currentH = adaptStep(f,currentX, currentI, currentH, relativeTol)
        currentI = rungeKutta(f, currentX, currentI, currentH)
        currentX += currentH

    currentH = xUpperLim - currentX
    currentI = rungeKutta(f,currentX, currentI, currentH)

    return currentI
   
    



def checkEquivalenceUnderRelativeTolerance(a,b, relativeTol):

    magDif = abs(a-b)

    if a == 0 and b == 0: 
        return True

    elif a == 0 or b == 0 :
        return magDif <= relativeTol

    else: 
        absTol = a * relativeTol
        return magDif <= absTol
    



def adaptStep(f, x, y, h, relativeTol):

    hh = h / 2.0
    dh = h * 2.0
    min_h = 0.0005

    
    new_y_h = rungeKutta(f, x, y, h)
    new_y_hh = rungeKutta(f, x, y, hh)
    new_y_dh = rungeKutta(f, x, y, dh)
    
    if h < min_h:
        return min_h
    
    elif checkEquivalenceUnderRelativeTolerance(new_y_hh, new_y_h, relativeTol) == False:
        return adaptStep(f, x, y, hh, relativeTol)
    
    
    elif checkEquivalenceUnderRelativeTolerance(new_y_h, new_y_dh, relativeTol) == False:    
        return h

    else:
        return adaptStep(f, x, y, dh, relativeTol)



def adaptiveRungeKutta(f, x, y, h, relativeTol):
    
    new_h = adaptStep(f, x, y, h, relativeTol) 
    new_y = rungeKutta(f, x, y, new_h)
    
    return new_y
    
    
