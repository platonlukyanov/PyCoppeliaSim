from module import Coppelia
import math

copp = Coppelia(api_name="b0RemoteApi1")
client = copp.client

while True:
    copp.set_speed('Rev74', 50)
