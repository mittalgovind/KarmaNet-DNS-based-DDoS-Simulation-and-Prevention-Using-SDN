import socket               
from random import randint
# next create a socket object
import pdb
from impacket import ImpactPacket
# from ImpactPacket import * 
from array import array

serverSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_UDP)         
port = 53

# Next bind to the port
serverSocket.bind(('dns-eth0', 0x0800))       
eth = ImpactPacket.Ethernet()
eth.set_ether_shost(array('B', '\x00\x00\x00\x00\x01\x00'))
eth.set_ether_type(0x0800)
ip = ImpactPacket.IP()
ip.set_ip_src('10.0.0.100')
udp = ImpactPacket.UDP()
udp.set_uh_sport(53)
# an error occurs
while True:
	frame = serverSocket.recv(2048)
	
	reply = randint(1000, 2000) * 'A'
	udp.contains(ImpactPacket.Data(reply))

	dport = ord(frame[34])*256 + ord(frame[35]) 
	udp.set_uh_dport(dport)

	dst = array('B', frame[26:30])
	clientAddress = str(dst[0]) +'.'+str(dst[1])+'.'+str(dst[2])+'.'+str(dst[3])
	ip.set_ip_dst(clientAddress)
	
	eth.set_ether_dhost(array('B', frame[6:12]))
	# pdb.set_trace()

	serverSocket.send(eth.get_packet())
	print '------------', clientAddress, dport, len(reply)