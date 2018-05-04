import socket               
from random import randint
# next create a socket object
import pdb

def makeIP(addr):
	return str(ord(addr[0])) + '.' + str(ord(addr[1])) + '.' + str(ord(addr[2])) + '.' + str(ord(addr[3]))
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         
port = 53

# Next bind to the port
serverSocket.bind(('10.0.0.100', port))       

# an error occurs
while True:
	message, clientAddress = serverSocket.recvfrom(2048)
	reply = randint(1000, 2000) * 'A'
	serverSocket.sendto(reply, clientAddress)
	print '------------', clientAddress, len(reply)