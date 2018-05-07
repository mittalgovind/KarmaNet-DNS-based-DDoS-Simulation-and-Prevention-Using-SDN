from random import randint
import time
import pdb
import sys
from socket import *
SERVER_ADDR = "10.0.0.100"
PORT = 53
PAYLOAD = 32
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = 'A' * PAYLOAD

recvsocket = socket(AF_PACKET, SOCK_RAW, IPPROTO_UDP)
recvsocket.bind(('h'+ sys.argv[1]+'-eth0', 0x0800))

while (True):
	f = open("vout"+sys.argv[1] ,"a")
	for i in range(10):
		delay = time.time()
		clientSocket.sendto(message, (SERVER_ADDR, PORT))
		reply, s = recvsocket.recvfrom(2048)
		# pdb.set_trace()
		delay = (time.time() - delay)*1000
		# print delay
		f.write("%f\n" %delay)
	time.sleep(0.1 * randint(0, 5))
	f.close()