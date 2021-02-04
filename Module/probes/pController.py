# Make sure to have CoppeliaSim running, with followig scene loaded:
#
# scenes/pControllerViaRemoteApi.ttt
#
# Do not launch simulation, and make sure that the B0 resolver
# is running. Then run this script
#
# The client side (i.e. this script) depends on:
#
# b0RemoteApi (Python script), which depends several libraries present
# in the CoppeliaSim folder


# import b0RemoteApi
# import math
# import time


# with b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient', 'b0RemoteApi') as client:
#     client.doNextStep = True
#     client.jointAngle = 0
#     client.targetAngle = 0
#     client.maxForce = 100

#     def simulationStepStarted(msg):
#         simTime = msg[1][b'simulationTime']

#     def simulationStepDone(msg):
#         simTime = msg[1][b'simulationTime']
#         client.doNextStep = True

#     def jointAngleCallback(msg):
#         client.jointAngle = msg[1]

#     def moveToAngle(jointH, angle):
#         client.targetAngle = angle
#         while abs(client.jointAngle-client.targetAngle) > 0.1*math.pi/180:
#             if client.doNextStep:
#                 client.doNextStep = False
#                 vel = computeTargetVelocity()
#                 client.simxSetJointTargetVelocity(
#                     jointH, vel, client.simxDefaultPublisher())
#                 client.simxSetJointMaxForce(
#                     jointH, client.maxForce, client.simxDefaultPublisher())
#                 client.simxSynchronousTrigger()
#             client.simxSpinOnce()

#     def computeTargetVelocity():
#         dynStepSize = 0.005
#         velUpperLimit = 360*math.pi/180
#         PID_P = 0.1
#         errorValue = client.targetAngle-client.jointAngle
#         sinAngle = math.sin(errorValue)
#         cosAngle = math.cos(errorValue)
#         errorValue = math.atan2(sinAngle, cosAngle)
#         ctrl = errorValue*PID_P

#         # Calculate the velocity needed to reach the position in one dynamic time step:
#         velocity = ctrl/dynStepSize
#         if (velocity > velUpperLimit):
#             velocity = velUpperLimit

#         if (velocity < -velUpperLimit):
#             velocity = -velUpperLimit

#         return velocity

#     jointHandle = client.simxGetObjectHandle('joint', client.simxServiceCall())
#     client.simxSetJointTargetVelocity(
#         jointHandle[1], 360*math.pi/180, client.simxServiceCall())
#     client.simxGetJointPosition(
#         jointHandle[1], client.simxDefaultSubscriber(jointAngleCallback))
#     client.simxGetSimulationStepStarted(
#         client.simxDefaultSubscriber(simulationStepStarted))
#     client.simxGetSimulationStepDone(
#         client.simxDefaultSubscriber(simulationStepDone))

#     client.simxSynchronous(True)

#     client.simxStartSimulation(client.simxDefaultPublisher())

#     moveToAngle(jointHandle[1], 45*math.pi/180)
#     moveToAngle(jointHandle[1], 90*math.pi/180)
#     # no -90, to avoid passing below
#     moveToAngle(jointHandle[1], -89*math.pi/180)
#     moveToAngle(jointHandle[1], 0*math.pi/180)

#     client.simxStopSimulation(client.simxDefaultPublisher())

import b0RemoteApi
import time
import math
with b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient', 'b0RemoteApi') as client:
    doNextStep = True

    def simulationStepStarted(msg):
        simTime = msg[1][b'simulationTime']
        print('Simulation step started. Simulation time: ', simTime)

    def simulationStepDone(msg):
        simTime = msg[1][b'simulationTime']
        print('Simulation step done. Simulation time: ', simTime)
        global doNextStep
        doNextStep = True

    client.simxSynchronous(True)
    client.simxGetSimulationStepStarted(client.simxDefaultSubscriber(simulationStepStarted))
    client.simxGetSimulationStepDone(client.simxDefaultSubscriber(simulationStepDone))
    client.simxStartSimulation(client.simxDefaultPublisher())

    link1 = client.simxGetObjectHandle('BIG_Link1', client.simxServiceCall())
    link2 = client.simxGetObjectHandle('BIG_Link2', client.simxServiceCall())

    link1_pos = client.simxGetJointPosition(link1[1], client.simxServiceCall())
    link2_pos = client.simxGetJointPosition(link2[1], client.simxServiceCall())
    print(link1_pos)
    print(link2_pos)
    
    link1_pos[1] = (link1_pos[1])*180/math.pi
    link2_pos[1] = (link2_pos[1])*180/math.pi
    startTime = time.time()
    while link1_pos[1] < 150:
        if doNextStep:
            doNextStep = False
            link1_pos[1] = link1_pos[1]+1
            link2_pos[1] = link2_pos[1]+1
            client.simxSetJointPosition(link1[1], link1_pos[1]*180/math.pi, client.simxServiceCall())
            client.simxSetJointPosition(link2[1], link2_pos[1]*180/math.pi, client.simxServiceCall())
            client.simxAddDrawingObject_cubes(34, )
            time.sleep(0.01)
            client.simxSynchronousTrigger()
        client.simxSpinOnce()
    client.simxStopSimulation(client.simxDefaultPublisher())
