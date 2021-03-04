tau = 2 #time constant of first order system
def calcState(force, prevState, timeStep_s):
    #Time derivatives for first order system:
    xDot = (force[0] - prevState[0])/tau
    yDot = (force[1] - prevState[1])/tau
    #Euler integration:
    nextState = [0, 0]
    nextState[0] = prevState[0] + xDot*timeStep_s 
    nextState[1] = prevState[1] + yDot*timeStep_s
    return nextState