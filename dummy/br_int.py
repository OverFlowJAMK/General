# Copyright (C) 2014,2015 VA Linux Systems Japan K.K.
# Copyright (C) 2014,2015 YAMAMOTO Takashi <yamamoto at valinux co jp>
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
* references
** OVS agent https://wiki.openstack.org/wiki/Ovs-flow-logic
"""

import netaddr

from neutron_lib import constants as const

from neutron.common import constants as n_const
from neutron.plugins.common import constants as p_const
from neutron.plugins.ml2.drivers.openvswitch.agent.common import constants
from neutron.plugins.ml2.drivers.openvswitch.agent.openflow.dummy \
    import ovs_bridge


class OVSIntegrationBridge(ovs_bridge.OVSAgentBridge):
    """openvswitch agent br-int specific logic."""

    def setup_default_table(self):
        pass

    def setup_canary_table(self):
        pass

    def check_canary_table(self):
        return constants.OVS_NORMAL

    def provision_local_vlan(self, port, lvid, segmentation_id):
        pass

    def reclaim_local_vlan(self, port, segmentation_id):
        pass

    def install_dvr_to_src_mac(self, network_type,
                               vlan_tag, gateway_mac, dst_mac, dst_port):
        pass

    def delete_dvr_to_src_mac(self, network_type, vlan_tag, dst_mac):
        pass

    def add_dvr_mac_vlan(self, mac, port):
        pass

    def remove_dvr_mac_vlan(self, mac):
        pass

    def add_dvr_mac_tun(self, mac, port):
        pass

    def remove_dvr_mac_tun(self, mac, port):
        pass

    def install_icmpv6_na_spoofing_protection(self, port, ip_addresses):
        pass

    def set_allowed_macs_for_port(self, port, mac_addresses=None,
                                  allow_all=False):
        pass

    def install_arp_spoofing_protection(self, port, ip_addresses):
        pass

    def delete_arp_spoofing_protection(self, port):
        pass

    def delete_arp_spoofing_allow_rules(self, port):
        pass
