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

# create a raw socket, so as to send and receive packets without interfering with ethernet frames.
recvsocket = socket(AF_PACKET, SOCK_RAW, IPPROTO_UDP)
# binding the raw socket, with the ethernet interface of the client
# here every client has interfaces, as h1-eth0, h2-eth0, therefore client number is taken as an argument
recvsocket.bind(('h'+ sys.argv[1]+'-eth0', 0x0800))

while (True):
	# the delay is saved onto a file named vout<client_no>
	f = open("vout"+sys.argv[1] ,"a")
	# the bombarding power of the client is fixed at 10
	for i in range(10):
		delay = time.time()
		clientSocket.sendto(message, (SERVER_ADDR, PORT))
		reply, s = recvsocket.recvfrom(2048)
		delay = (time.time() - delay)*1000
		# print delay
		f.write("%f\n" %delay)
	time.sleep(0.1 * randint(0, 5))
	f.close()
