import sys
import random
import time
from socket import socket, AF_INET, SOCK_DGRAM

SERVER_IP   = '192.168.0.105'
PORT_NUMBER = 6006
SIZE = 1024

mySocket = socket( AF_INET, SOCK_DGRAM )

while True:
    data = ""
    for i in range(3):
        data = data + str(random.random()) + " "
    mySocket.sendto(data,(SERVER_IP,PORT_NUMBER))
    time.sleep(1)
