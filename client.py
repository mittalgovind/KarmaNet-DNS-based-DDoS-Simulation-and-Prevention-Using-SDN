import socket
from random import randint
import time
import pdb

SERVER_ADDR = "10.0.0.100"
PORT = 53
PAYLOAD = 32

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = 'A' * PAYLOAD
# flag = 0
while (True):
	for i in range(10):
		delay = time.time()
		clientSocket.sendto(message, (SERVER_ADDR, PORT))
		# if flag >= 
		reply, s = clientSocket.recvfrom(2048)
		# flag += 1
		delay = (time.time() - delay)*1000
		print 'delay = '+ str(int(delay)) +' millis'
	time.sleep(0.1 * randint(0, 5))
