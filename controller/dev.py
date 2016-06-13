########################
#
# Author: Sami Autio
# Date: 13.6.2016
#
########################

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import ipv4
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.ofproto import ofproto_v1_3

import json
import requests

class SwitchLogic(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION] 
      
    def __init__(self, *args, **kwargs):
	super(SwitchLogic, self).__init__(*args, **kwargs)
	self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
	
	# Create default flow for switches which sends packets to controller
	datapath = ev.msg.datapath
	ofproto = datapath.ofproto
	parser = datapath.ofproto_parser
	match = parser.OFPMatch()
	actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
	#print('Added default flow to switch')
	self.add_flow(datapath, 0, 0, match, actions)

    def add_flow(self, datapath, timeout, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

	inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
	if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, hard_timeout=timeout, match=match, priority=priority, buffer_id=buffer_id, instructions=inst)
	else:
            mod = parser.OFPFlowMod(datapath=datapath, hard_timeout=timeout, priority=priority, match=match, instructions = inst)
	#print('Added flow to switch')
        datapath.send_msg(mod)

    # Event listener for packets
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
	datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
	in_port = msg.match['in_port']

	pkt = packet.Packet(msg.data)
	eth = pkt.get_protocols(ethernet.ethernet)[0]
	
	src = eth.src
	dst = eth.dst
	
	dpid = datapath.id
	self.mac_to_port.setdefault(dpid, {})
	
	# Learn a mac address to avoid FLOOD next time
	self.mac_to_port[dpid][src] = in_port
	
	if dst in self.mac_to_port[dpid]:
	    out_port = self.mac_to_port[dpid][dst]
	else:
	    out_port = ofproto.OFPP_FLOOD
	
	# If packet is going to switch 1(dpid=1) and in_port=1
	# check if device is allowed from api
	if dpid == 1 and in_port == 1:

	    # Get list of allowed devices from api
	    devices = []
	    response = requests.get('http://127.0.0.1:5000/network/api/v0.1/devices')
	    jsondata = response.json()
	    for element in jsondata['devices']:
	        devices.append(element['device'])

	    # If source mac-address is not in allowed list then drop packet
	    if src not in devices:
		out_port = None
		actions = [parser.OFPActionOutput(0)]
	    else:
		actions = [parser.OFPActionOutput(out_port)]
	else:
	    actions = [parser.OFPActionOutput(out_port)]
	
	# Install a flow to avoid packet_in next time
	if out_port != ofproto.OFPP_FLOOD:
	    match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
	    print(match)
	    # Verify if we have a valid buffer_id, if yes avoid to send both
	    # flow_mod & packet_out
	    if msg.buffer_id != ofproto.OFP_NO_BUFFER:
		self.add_flow(datapath, 30, 1, match, actions, msg.buffer_id)
	    else:
		self.add_flow(datapath, 30, 1, match, actions)
	data = None
	if msg.buffer_id == ofproto.OFP_NO_BUFFER:
	    data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)


