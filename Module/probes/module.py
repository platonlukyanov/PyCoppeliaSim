import b0RemoteApi
import time
import math


class Coppelia:

    def __init__(self, api_name="b0RemoteApi"):
        self.client = b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient', api_name)
        self.client.simxSynchronous(True)
        self.client.simxStartSimulation(self.client.simxDefaultPublisher())
        self.call = self.client.simxServiceCall

    def get_position(self, object_name, typeof="degrees"):
        link = self.client.simxGetObjectHandle(object_name, self.call())
        result = self.client.simxGetJointPosition(link[1], self.call())[1]
        if typeof == "degrees":
            result = math.degrees(result)
        if typeof == "radians":
            pass
        elif typeof != "degrees":
            raise ValueError('Invalid typeof "{typeof}". You should use "degrees" or "radians"'.format(typeof=typeof))

        return result

    def set_position(self, object_name, position):
        link = self.client.simxGetObjectHandle(object_name, self.call())
        self.client.simxSetJointPosition(link[1], position, self.call())

    def move(self, object_name, position, typeof="degrees"):
        link = self.client.simxGetObjectHandle(object_name, self.call())
        if typeof == "degrees":
            position = math.radians(position)
            print("position-for-degrees")

        if typeof == "radians":
            # Вычисляем разницу между текущей позицией и желаемой
            current_position = self.get_position(object_name)
            difference_position = current_position - position
            # если он меньше нуля ждем пока будет больше
            if difference_position <= 0:
                while position < current_position:
                    current_position = self.get_position(object_name)
                    print(current_position)
                    self.client.simxSetJointTargetPosition(link[1], position,
                                                           self.call())  # устанавливает угол поворота
                    self.client.simxSynchronousTrigger()  # обновляет время
                    self.client.simxSpinOnce()  # делает следущий "шаг"
            # а иначе ждем меньше
            else:
                while position >= current_position:
                    self.client.simxSetJointTargetPosition(link[1], position,
                                                           self.call())  # устанавливает угол поворота
                    self.client.simxSynchronousTrigger()  # обновляет время
                    self.client.simxSpinOnce()  # делает следущий "шаг"



    # else:
    #     raise ValueError('Invalid typeof "{typeof}". You should use "degrees" or "radians"'.format(typeof=typeof))

    def stop_sim(self):
        self.client.simxStopSimulation(self.client.simxDefaultPublisher())

    def set_speed(self, object_name, speed):
        link = self.client.simxGetObjectHandle(object_name, self.call())
        self.client.simxSetJointTargetVelocity(link[1], speed, self.call())


    def __del__(self):
        self.stop_sim()
        del self.client
