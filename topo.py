#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from random import randint
import pdb
import time

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', mac='00:00:00:00:00:01', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', mac='00:00:00:00:00:02', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', mac='00:00:00:00:00:03', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', mac='00:00:00:00:00:04', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', mac='00:00:00:00:00:05', defaultRoute=None)
    adversary = net.addHost('adversary', cls=Host, ip='10.0.0.99', mac='00:00:00:00:00:99', defaultRoute=None)
    dns = net.addHost('dns', cls=Host, ip='10.0.0.100', mac='00:00:00:00:01:00', defaultRoute=None)
    # trap = net.addHost('trap', cls=Host, ip='10.0.0.10', mac='00:00:00:00:00:10', defaultRoute=None)

    info( '*** Add links\n')
    # pdb.set_trace()

    net.addLink(h1, s1, cls=TCLink, **{'bw':2})
    net.addLink(s2, h2, cls=TCLink, **{'bw':2})
    net.addLink(adversary, s6, cls=TCLink, **{'bw':2})
    net.addLink(s4, h4, cls=TCLink, **{'bw':2})
    net.addLink(h5, s5, cls=TCLink, **{'bw':2})
    net.addLink(dns, s7, cls=TCLink, **{'bw':2})
    net.addLink(s3, h3, cls=TCLink, **{'bw':2})
    # net.addLink(s7, trap, cls=TCLink, **{'bw':20})
    
    net.addLink(s1, s2, cls=TCLink, **{'bw':2})
    net.addLink(s2, s3, cls=TCLink, **{'bw':2})
    net.addLink(s3, s7, cls=TCLink, **{'bw':2})
    net.addLink(s6, s7, cls=TCLink, **{'bw':2})
    net.addLink(s6, s4, cls=TCLink, **{'bw':2})
    net.addLink(s6, s5, cls=TCLink, **{'bw':2})

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s6').start([c0])
    net.get('s3').start([c0])
    net.get('s7').start([c0])
    net.get('s1').start([c0])
    net.get('s4').start([c0])
    net.get('s5').start([c0])
    net.get('s2').start([c0])

    info( '*** Post configure switches and hosts\n')
    # pdb.set_trace()

    dns.sendCmd('python dns.py > dnsOut_Adversary_with_sec.txt')
    adversary.sendCmd('python adversary.py')
    client = [h1, h2, h3, h4, h5]
    i = 1
    for c in client:
        c.sendCmd('python client.py > h'+str(i)+'Out_Adversary_with_sec.txt')
        i += 1

    time.sleep(40)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

