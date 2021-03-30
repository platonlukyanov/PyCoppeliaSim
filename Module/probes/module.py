import b0RemoteApi
import time


def simulationStepStarted(msg):
    simTime = msg[1][b'simulationTime']
    print('Simulation step started. Simulation time: ', simTime)


def simulationStepDone(msg):
    simTime = msg[1][b'simulationTime']
    print('Simulation step done. Simulation time: ', simTime)
    doNextStep = True


class Coppelia:
    doNextStep = True

    def __init__(self, stepStartedFunc=simulationStepStarted, stepDoneFunc=simulationStepDone, api_name="b0RemoteApi"):
        self.client = b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient', api_name)
        self.client.simxSynchronous(True)
        self.client.simxGetSimulationStepStarted(self.client.simxDefaultSubscriber(stepStartedFunc))
        self.client.simxGetSimulationStepDone(self.client.simxDefaultSubscriber(stepDoneFunc))
        self.client.simxStartSimulation(self.client.simxDefaultPublisher())

    def set_position(self, object_name, position):
        link = self.client.simxGetObjectHandle(object_name, self.client.simxServiceCall())
        self.client.simxSetJointPosition(link[1], position, self.client.simxServiceCall())

    def stop_sim(self):
        self.client.simxStopSimulation(self.client.simxDefaultPublisher())

    def __del__(self):
        self.stop_sim()
        del self.client
