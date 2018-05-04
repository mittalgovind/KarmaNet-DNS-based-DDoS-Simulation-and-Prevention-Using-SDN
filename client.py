import socket
from random import randint
import time
import pdb
import sys

SERVER_ADDR = "10.0.0.100"
PORT = 53
PAYLOAD = 32
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = 'A' * PAYLOAD

while (True):
	f = open("vout"+sys.argv[1] ,"a")
	for i in range(10):
		delay = time.time()
		clientSocket.sendto(message, (SERVER_ADDR, PORT))
		reply, s = clientSocket.recvfrom(2048)
		delay = (time.time() - delay)*1000
		f.write("%f\n" %delay)
	time.sleep(0.1 * randint(0, 5))
	f.close()