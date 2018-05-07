from socket import *            
from random import randint
# next create a socket object

serverSocket = socket(AF_INET, SOCK_DGRAM)         
port = 53

# Next bind to the port
serverSocket.bind(('10.0.0.100', port))       
while True:
	s, clientAddress = serverSocket.recvfrom(2048)
	reply = randint(1200, 1450) * 'A'
	serverSocket.sendto(reply, clientAddress)
	print '------------', clientAddress, len(reply)