import socket               
from random import randint
# next create a socket object
import pdb

def makeIP(addr):
	return str(ord(addr[0])) + '.' + str(ord(addr[1])) + '.' + str(ord(addr[2])) + '.' + str(ord(addr[3]))
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         
print "Socket successfully created"

# reserve a port on your computer in our
port = 53

# Next bind to the port
serverSocket.bind(('10.0.0.100', port))       
print "socket binded to %s" %(port)

# an error occurs
while True:
	message, clientAddress = serverSocket.recvfrom(2048)
	reply = randint(1000, 2000) * 'A'
	# pdb.set_trace()
	# if clientAddress[0] == '10.0.0.99':
	# 	clientAddress = (makeIP(message[12:16]), clientAddress[1])
	print '------------', clientAddress, len(reply)
	serverSocket.sendto(reply, clientAddress)