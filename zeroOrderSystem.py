#https://eleceng.dit.ie/gavin/Instrument/Dynamic/Dynamic%20Notes.html:
#   The output of a zero order system is proportional to the input.
Kp = 1
def calcState(refState, prevState, dt_s):
    nextState = [0, 0]
    #nextState[0] = Kp * prevState[0] 
    #nextState[1] = Kp * prevState[1]
    Velocity = [0, 0]
    Velocity[0] = 0.05*(refState[0] - prevState[0]) / dt_s
    Velocity[1] = 0.05*(refState[1] - prevState[1]) / dt_s
    nextState[0] = prevState[0] + Velocity[0]*dt_s
    nextState[1] = prevState[1] + Velocity[1]*dt_s
    return nextState