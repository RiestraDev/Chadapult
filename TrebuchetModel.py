import math

# -------------------------------------------------------------------

# constants
gravity = 9.81
massOfPlateInKg = 20.4117

# -------------------------------------------------------------------

# user defined variables

# using multiple plates - simplify by just multiplying by the constant
counterWeightMass = massOfPlateInKg * 2 # Kg

# 450 is the diameter of a 45 lb plate
counterWeightDiameter = .45 # meters 

# about 10 lbs
payloadMass = 4.5 # Kg

# this can be 3.75, 4, 5 - more research needed to find right ratio
longArmLengthToshortArmLengthRatio = 3.75 

# shortArmLength must > counterWeightRadius this ratio must be > 1 
shortArmLengthToCounterWeightRadiusRatio = 2 # user defined

# Additional height to add to base. Will lift counterweight to higher position.
# Increasing this might add power, to a point. 
additionalHeight = .3048 # meters

# 0.1 - 0.2: Smooth wood on smooth wood (lubricated).
# 0.4 - 0.5: Wood dragging on dirt/grass.
# 0.6 - 0.8: Rough stone dragging on dirt/grass.
frictionCoefficient = .2

# -------------------------------------------------------------------

# calculate Total Arm Length
counterWeightRadius = counterWeightDiameter / 2
shortArmLength = counterWeightRadius * shortArmLengthToCounterWeightRadiusRatio
longArmLength = shortArmLength * longArmLengthToshortArmLengthRatio
beamLength = shortArmLength + longArmLength

slingLength = longArmLength * .9 # .9 is a hardcoded ratio. Ratio will be user defined. 

# -------------------------------------------------------------------

# find dimensions of the base

# baseHeight (pivotPointHeight) must be > shortArmLength + counterWeightOverhang (radius) 
counterWeightOverhang = counterWeightRadius
baseHeight = shortArmLength + counterWeightOverhang + additionalHeight

# length of each side of the base
baseSideLength = (baseHeight * 2) / math.sqrt(3) 

additionalBaseWidthRatio = 2 # user defined - Additional width to add base support

addtionalBaseWidth = baseSideLength * additionalBaseWidthRatio

# print(baseSideLength)
# print(addtionalBaseWidth)
# print(baseHeight)
print(f"{beamLength = } m")
print(f"{baseHeight = } m")
print(f"{addtionalBaseWidth = } m")

# -------------------------------------------------------------------

# figure out mass of beam

# in meters
beamThickness = 0.0254 # user defined - 1 inch
beamWidth = 0.0762 # user defined - 3 inch

beamVolume = beamLength * beamThickness * beamWidth

# kg/m^3
beamMaterialDensity = 500 # user defined - Will depend on type of wood
beamMass = beamVolume * beamMaterialDensity

print(f"{beamMass = } kg")

# -------------------------------------------------------------------

# Calculate Struts for base
# include base struts in calculations
# 1 will set strut halfway up base
# 2 will set them 1/3 up and 2/3 up
includeBaseStruts = True # user defined
baseStrutCount = 1 # user defined

strut1Length = 0
strut2Length = 0  
    
if includeBaseStruts:

    if baseStrutCount == 1:
        strut1Length = ((baseHeight / 2) / math.sqrt(3)) * 2
    if baseStrutCount == 2:
        strut1Length = ((baseHeight / 3) / math.sqrt(3)) * 2
        strut2Length = ( ((baseHeight / 3) * 2) / math.sqrt(3)) * 2

print(f"{strut1Length = } m")
print(f"{strut2Length = } m")

# -------------------------------------------------------------------

# Calculate max counter weight height

# Counter weight angle will be hardcoded. Will later find what optimal and possible top angle is. 
# relative to the horizon
startingCounterWeightAngle = 45

counterWeightHeightAbovePivot = shortArmLength * math.sin(startingCounterWeightAngle)

counterWeightHeight = baseHeight + counterWeightHeightAbovePivot

print(f"{counterWeightHeight = } m")

# -------------------------------------------------------------------

# We leave the world of trig behind and arrive at physics

# basic physics without factoring in the sling

# Hfall (m)
vertialDistanceCounterWeightFalls = counterWeightHeightAbovePivot + shortArmLength

# PEin (J joules)
# The total energy available is the potential energy lost by the counterweight falling.
potentialEnergyInput = counterWeightMass * gravity * vertialDistanceCounterWeightFalls

# vMax (meters per second)
theoreticalExitVelocity = math.sqrt( (2 * potentialEnergyInput) /  payloadMass)

# meters
maximumRange = math.pow(theoreticalExitVelocity, 2) / gravity

print(f"{potentialEnergyInput = } J")
print(f"{theoreticalExitVelocity = } m/s")
print(f"{maximumRange = } m")


# -------------------------------------------------------------------

# phase one The Slide

# 0 long arm is vertical - payload is resting at bottom 
# 90 arm is horizontal
startingLongArmAngle = 90 + startingCounterWeightAngle

# Normal Force (N newtons) How much force is pressing down against ground
normalForce = payloadMass * gravity

# (N newtons)
frictionForce = frictionCoefficient * normalForce

# Tnet
netTorqueOnMainAxle = (counterWeightMass * gravity * shortArmLength * math.sin(startingLongArmAngle)) - (frictionForce * longArmLength)

centerOfBeam = ( shortArmLength + longArmLength ) / 2
distanceFromCenterToPivotPoint = longArmLength - centerOfBeam

# -------------------------------------------------------------------

# calculate moment of intertia for beam and system
# moment of interia - rotational equivalent of mass, representing an object's resistance to changes in its rotational speed.

# use parallel axis theorem

# hard it is to rotate the empty swing arm
beamMomentOfInteria = ( (1/12) *  beamMass * math.pow(beamLength, 2) )  + ( beamMass * math.pow(distanceFromCenterToPivotPoint,2) )

# How hard it is to rotate the entire loaded machine
systemMomentOfInteria = beamMomentOfInteria + (counterWeightMass * math.pow(shortArmLength,2) ) + (payloadMass * pow(longArmLength, 2) )

print(f"{beamMomentOfInteria = } Kg/m^2")
print(f"{systemMomentOfInteria = } Kg/m^2")


armAngle = startingLongArmAngle # this will need to be incremented in the loop
slingToArmAngle = startingLongArmAngle # this will also need to be incremented 

# delta time - constant
# 1 is too chopy. Standard physics sims are set to 10 milliseconds. .01 = 10 miliseconds. Will change in later tests.
dt = .01

elapsedTime = 0

# The Slide loop
while elapsedTime < 100 :

    # calculate slingToBeamAngle 
    
    
    # yTip - height of the payload tip of the beam at a given moment
    armTipHeight = baseHeight - (math.cos(180 - armAngle) * longArmLength)

    # note The sine of an angle can never be greater than 1 or less than -1.
    # If Ratio > 1, cap it at 1. If Ratio < -1, cap it at -1.
    ratio = armTipHeight / slingLength
    if ratio > 1:
        ratio = 1

    angleOfGround = math.asin(ratio) # I think this might be in radians # continue here

    # calculate net torque
    # force trying to move rotate machine forward
    # tDrive
    positiveTorque = counterWeightMass * gravity * shortArmLength * math.sin(armAngle)

    # tDrag
    negativeTorque = frictionForce * longArmLength * math.sin(slingToArmAngle)

    # tNet
    netTorque = positiveTorque - negativeTorque

    # a - angular acceleration in rads/s^2
    angularAcceleration = netTorque / systemMomentOfInteria

    angularVelocity += angularAcceleration * dt
    armAngle = armAngle + ( angularVelocity * dt )

    elapsedTime += dt#
    # exit condition


# phase two Lift and Whip

