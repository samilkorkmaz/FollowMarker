Kp = 1.5 #proportionality constant
Ki = 1 #integral constant
integX = 0
integY = 0

def generateCommands(refLoc, currentLoc, timeStep_s):
    global Kp, Ki, integX, integY 
    dx = refLoc[0] - currentLoc[0]
    dy = refLoc[1] - currentLoc[1]
    errorStr = "dx = %1.0f, dy = %1.0f" % (dx, dy)
    propX = Kp*dx #proportianl term in x direction
    integX = integX + Ki*dx*timeStep_s #integral term in x direction
    forceX = propX + integX #force in x direction
    propY = Kp*dy #proportianl term in y direction
    integY = integY + Ki*dy*timeStep_s #integral term in y direction
    forceY = propY + integY #force in y direction
    return [forceX, forceY, errorStr]

        