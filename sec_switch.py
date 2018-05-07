# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ipv4, ether_types
from ryu.lib.packet import ethernet
import pdb

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.request_path_ip = { 
            1 : {'10.0.0.1': 2},
            2 : { '10.0.0.1': 3, '10.0.0.2': 3},
            3 : { '10.0.0.1': 3, '10.0.0.2': 3, '10.0.0.3': 3},
            4 : {'10.0.0.4': 2},
            5 : {'10.0.0.5': 2},
            6 : {'10.0.0.4': 2, '10.0.0.5': 2,'10.0.0.99': 2,
                 '10.0.0.1': 2, '10.0.0.2': 2, '10.0.0.3': 2},
            7: {
                '10.0.0.1': 1 , '10.0.0.2': 1,
                '10.0.0.3': 1,  '10.0.0.4': 1,
                '10.0.0.5': 1, '10.0.0.99': 1
                }
            }
        self.request_path_mac = { 
            1 : {'00:00:00:00:00:01': 2},
            2 : { '00:00:00:00:00:01': 3, '00:00:00:00:00:02': 3},
            3 : { '00:00:00:00:00:01': 3, '00:00:00:00:00:02': 3, '00:00:00:00:00:03': 3},
            4 : {'00:00:00:00:00:04': 2},
            5 : {'00:00:00:00:00:05': 2},
            6 : {'00:00:00:00:00:04': 2, '00:00:00:00:00:05': 2,'00:00:00:00:00:99': 2},
            7: {
                '00:00:00:00:00:01': 1 , '00:00:00:00:00:02': 1,
                '00:00:00:00:00:03': 1,  '00:00:00:00:00:04': 1,
                '00:00:00:00:00:05': 1, '00:00:00:00:00:99': 1
                }
            }

        self.reply_path_ip = {
            1 : {'10.0.0.1': 1},
            2 : { '10.0.0.1': 2, '10.0.0.2': 1},
            3 : { '10.0.0.1': 2, '10.0.0.2': 2, '10.0.0.3': 1},
            4 : {'10.0.0.4': 1},
            5 : {'10.0.0.5': 1},
            6 : {'10.0.0.4': 3, '10.0.0.5': 4,'10.0.0.99': 1,
                 '10.0.0.1': 1, '10.0.0.2': 1, '10.0.0.3': 1},
            7: {
                '10.0.0.1':  2, '10.0.0.2': 2,
                '10.0.0.3': 2, '10.0.0.4': 3,
                '10.0.0.5': 3, '10.0.0.99': 3
                }
            }
        self.reply_path_mac = {
            1 : {'00:00:00:00:00:01': 1},
            2 : { '00:00:00:00:00:01': 2, '00:00:00:00:00:02': 1},
            3 : { '00:00:00:00:00:01': 2, '00:00:00:00:00:02': 2, '00:00:00:00:00:03': 1},
            4 : {'00:00:00:00:00:04': 1},
            5 : {'00:00:00:00:00:05': 1},
            6 : {'00:00:00:00:00:04': 3, '00:00:00:00:00:05': 4,'00:00:00:00:00:99': 1},
            7: {
                '00:00:00:00:00:01':  2, '00:00:00:00:00:02': 2,
                '00:00:00:00:00:03': 2, '00:00:00:00:00:04': 3,
                '00:00:00:00:00:05': 3, '00:00:00:00:00:99': 3
                }
            }
                  

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        
        # hard-timeout of 5 seconds is set, so that no other flow entry can be 
        # created after that. This cuts the route of the adversary to send the packet through the controller
        self.add_flow(datapath, 0, match, actions, hard_timeout=5)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None, idle_timeout=0,
                hard_timeout=0):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst, idle_timeout=idle_timeout,
                                    hard_timeout=hard_timeout)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst, idle_timeout=idle_timeout,
                                    hard_timeout=hard_timeout)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        eth_dst = eth.dst
        eth_src = eth.src

        ip = pkt.get_protocols(ipv4.ipv4)
        dpid = datapath.id

        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        if ip:
            ip = ip[0]
            ip_src = ip.src
            ip_dst = ip.dst
            # hard-coded flows
            try:
                if eth_dst == '00:00:00:00:01:00' and self.request_path_ip.has_key(dpid):
                    # pdb.set_trace()
                    if self.request_path_ip[dpid].has_key(ip_src):
                        if self.request_path_mac[dpid].has_key(eth_src):
                            match_rq = parser.OFPMatch(in_port=in_port, eth_src=eth_src,
                                        eth_type=0x0800, ip_proto=17, ipv4_src=ip_src, 
                                        ipv4_dst='10.0.0.100', udp_dst=53
                                        )
                            out_port_rq = self.request_path_ip[dpid][ip_src]
                            actions = [parser.OFPActionOutput(out_port_rq)] 
                            self.add_flow(datapath=datapath, priority=100, match=match_rq, actions=actions)

                        else:
                            # would happen if somebody spoofs mac too
                            match_trap = parser.OFPMatch(in_port=in_port, eth_type=0x0800, ip_proto=17, ipv4_dst='10.0.0.100')
                            trap_port = 0
                            actions = [parser.OFPActionOutput(trap_port)] 
                            self.add_flow(datapath=datapath, priority=1000, match=match_trap, actions=actions)
                            
                else:
                    if eth_src == '00:00:00:00:01:00' and self.reply_path_ip.has_key(dpid):
                        if self.reply_path_mac[dpid].has_key(eth_dst):
                            match_rp = parser.OFPMatch(in_port=in_port, eth_dst=eth_dst,
                                        eth_type=0x0800) 
                            out_port_rp = self.reply_path_ip[dpid][ip_dst]
                            actions = [parser.OFPActionOutput(out_port_rp)] 
                            self.add_flow(datapath=datapath, priority=10, match=match_rp, actions=actions)
                        else: 
                            match_trap = parser.OFPMatch(in_port=in_port, eth_dst=eth_dst)
                            trap_port = 0
                            actions = [parser.OFPActionOutput(trap_port)] 
                            self.add_flow(datapath=datapath, priority=1000, match=match_trap, actions=actions)
                        
            except KeyError:
                print "missing " + ip_src + " from datapath s" + str(dpid) 
        else :
            self.mac_to_port.setdefault(dpid, {})

            self.logger.info("packet in %s %s %s %s", dpid, eth_src, eth_dst, in_port)
            # pdb.set_trace()
            # learn a mac address to avoid FLOOD next time.
            self.mac_to_port[dpid][eth_src] = in_port

            if eth_dst in self.mac_to_port[dpid]:
                out_port = self.mac_to_port[dpid][eth_dst]
            else:
                out_port = ofproto.OFPP_FLOOD

            actions = [parser.OFPActionOutput(out_port)]

            # install a flow to avoid packet_in next time
            # if out_port != ofproto.OFPP_FLOOD:
            #     match = parser.OFPMatch(in_port=in_port, eth_dst=eth_dst)
            #     # verify if we have a valid buffer_id, if yes avoid to send both
            #     # flow_mod & packet_out
            #     if msg.buffer_id != ofproto.OFP_NO_BUFFER:
            #         self.add_flow(datapath, 1, match, actions, msg.buffer_id)
            #         return
            #     else:
            #         self.add_flow(datapath, 1, match, actions)
        
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
