import socket               
from random import randint
# next create a socket object
from impacket import ImpactPacket
from array import array

serverSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_UDP)         
port = 53

# Next bind to the physical interface
# the ethertype = 0x0800 = the enclosing packet by the ethernet frame will be an IP packet.
serverSocket.bind(('dns-eth0', 0x0800))       

eth = ImpactPacket.Ethernet()
# the source mac = 00:00:00:00:01:00 -- check topo.py
eth.set_ether_shost(array('B', '\x00\x00\x00\x00\x01\x00'))
eth.set_ether_type(0x0800)
ip = ImpactPacket.IP()
ip.set_ip_src('10.0.0.100')
udp = ImpactPacket.UDP()
udp.set_uh_sport(53)

while True:
	# receive a raw ethernet frame
	frame = serverSocket.recv(2048)
	# create a random payload
	reply = randint(1200, 1450) * 'A'
	udp.contains(ImpactPacket.Data(reply))
	# extract the source port of the received frame
	dport = ord(frame[34])*256 + ord(frame[35]) 
	udp.set_uh_dport(dport)

	# extract the source IP
	dst = array('B', frame[26:30])
	clientAddress = str(dst[0]) +'.'+str(dst[1])+'.'+str(dst[2])+'.'+str(dst[3])
	ip.set_ip_dst(clientAddress)
	ip.contains(udp)
	eth.set_ether_dhost(array('B', frame[6:12]))
	eth.contains(ip)
	# send raw eth frame after putting data layer, by layer as shown above
	serverSocket.send(eth.get_packet())
	print '------------', clientAddress, dport, len(reply)
