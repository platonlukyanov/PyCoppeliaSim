import b0RemoteApi
import time
import math

with b0RemoteApi.RemoteApiClient('b0RemoteApi_V-REP', 'b0RemoteApi1') as client:
    client.simxSynchronous(True)
    client.simxStartSimulation(client.simxDefaultPublisher())

    link1 = client.simxGetObjectHandle('Rev74', client.simxServiceCall())

    while True:

        degree = math.degrees(client.simxGetJointPosition(link1[1], client.simxServiceCall())[1])
        print(degree)
        client.simxSetJointTargetPosition(link1[1], math.radians(90), client.simxServiceCall())  # устанавливает угол поворота
        client.simxSynchronousTrigger()  # обновляет время
        client.simxSpinOnce()  # делает следущий "шаг"

