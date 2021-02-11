import b0RemoteApi

def simulationStepStarted(msg):
	simTime = msg[1][b'simulationTime']
	print('Simulation step started. Simulation time: ', simTime)

def simulationStepDone(msg):
	simTime = msg[1][b'simulationTime']
	print('Simulation step done. Simulation time: ', simTime)
	doNextStep = True


class Coppelia:
	doNextStep = True
	def __init__(self, stepStartedFunc=simulationStepStarted, stepDoneFunc=simulationStepDone):

		self.client = b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient', 'b0RemoteApi')
		self.client.simxSynchronous(True)
		self.client.simxGetSimulationStepStarted(self.client.simxDefaultSubscriber(stepStartedFunc))
		self.client.simxGetSimulationStepDone(self.client.simxDefaultSubscriber(stepDoneFunc))
		self.client.simxStartSimulation(self.client.simxDefaultPublisher()) 
	

def stop_sim(self):
	self.client.simxStopSimulation(self.client.simxDefaultPublisher())

def __del__(self):
	self.stop_sim()
	del self.client
if __name__ == '__main__':
	copp = Coppelia()
	print(copp.client)
	del copp
