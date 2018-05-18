# DNS-based-DDoS-Simulation-and-Prevention
DNS-based DDoS attack simulation and solution using SDN flow monitoring

This repository is created to support the publication at this link.

This repository uses many simple tools to:
  1.  Simulate a Domain-Name-Server
  1.  Simulate a DDoS attack using one adversary node
  2.  Contain its adverse effect on network resources

All files in the repository are commented wherever necessary.

Description of Files:
  1.  **dns.py:** Contains the script to run the Domain Name Server at 10.0.0.100:53
  2.  **client.py:** Contains the script to run the client nodes
  3.  **adversary.py:** Contains the script to run the adversary at a node and start the DDoS.
  4.  **topo.py:** This file runs the network and starts the simulation. 
  5.  **sec_switch.py:** This is a Ryu based SDN controller, with the KarmaNet solution in it.
  6.  **simple_switch.py:** This is a simple Ryu based SDN controller, which already comes with the Ryu package. It works through normal L2 switching.
  7.  **topologies:** This folder contains topologies made in miniedit.py 
  8.  **run.sh:** bash script to run the complete simulation
