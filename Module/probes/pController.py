import b0RemoteApi
import time
import math

with b0RemoteApi.RemoteApiClient('b0RemoteApi_V-REP', 'b0RemoteApi1') as client:
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

    link1 = client.simxGetObjectHandle('Rev74', client.simxServiceCall())

    startTime = time.time()
    while time.time() < startTime + 10:
        if doNextStep:
            doNextStep = False
            client.simxSetJointTargetPosition(link1[1], 9, client.simxServiceCall())
            time.sleep(0)
            client.simxSynchronousTrigger() # обновляет время
        client.simxSpinOnce() # делает следущий "шаг"
    client.simxStopSimulation(client.simxDefaultPublisher())
