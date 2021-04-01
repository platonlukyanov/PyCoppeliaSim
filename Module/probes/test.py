from module import Coppelia
import math
copp = Coppelia(api_name="b0RemoteApi1")
client = copp.client
copp.move("Rev74", 180, typeof="degrees")