import b0RemoteApi
import time
import math
from threading import *
import logging


class Coppelia:

    def __init__(self, api_name="b0RemoteApi"):
        self.client = b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient', api_name)
        self.client.simxSynchronous(True)
        self.client.simxStartSimulation(self.client.simxDefaultPublisher())
        self.call = self.client.simxServiceCall
        logging.basicConfig(filename='debug.log', level=logging.DEBUG, filemode='w',
                            format='%(name)s - %(asctime)% - %(levelname)s - %(message)s')
        t = Thread(target=self._timer)
        t.start()

    def _timer(self):
        while True:
            self.client.simxSynchronousTrigger()  # обновляет время
            self.client.simxSpinOnce()

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

        if typeof == "radians":
            pass

        elif typeof not in ["radians", "degrees"]:
            raise ValueError('Invalid typeof "{typeof}". You should use "degrees" or "radians"'.format(typeof=typeof))
        print("position", position)
        current_position = self.get_position(object_name)
        difference_position = current_position - position
        # если он меньше нуля ждем пока будет больше
        print("diff", difference_position)
        if difference_position <= 0:
            print("current_position 1: ", current_position)
            print("position 1: ", position)
            while position < current_position:
                current_position = self.get_position(object_name)
                self.client.simxSetJointTargetPosition(link[1], position,
                                                       self.call())  # устанавливает угол поворота
        # а иначе ждем меньше
        else:
            print("current_position 2: ", current_position)
            print("position 2: ", position)
            while position >= current_position:
                self.client.simxSetJointTargetPosition(link[1], position,
                                                       self.call())  # устанавливает угол поворота
                self.client.simxSynchronousTrigger()  # обновляет время
                self.client.simxSpinOnce()  # делает следущий "шаг"

    def stop_sim(self):
        self.client.simxStopSimulation(self.client.simxDefaultPublisher())

    def set_speed(self, object_name, speed):
        link = self.client.simxGetObjectHandle(object_name, self.call())
        self.client.simxSetJointTargetVelocity(link[1], speed, self.call())

    def __del__(self):

        self.stop_sim()
        del self.client
