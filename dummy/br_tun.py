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

# Copyright 2011 VMware, Inc.
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

import functools

import netaddr

from neutron.agent.common import ovs_lib
from neutron.plugins.ml2.drivers.openvswitch.agent.common \
    import constants
from neutron.plugins.ml2.drivers.openvswitch.agent.openflow.dummy \
    import br_dvr_process
from neutron.plugins.ml2.drivers.openvswitch.agent.openflow.dummy \
    import ovs_bridge


class OVSTunnelBridge(ovs_bridge.OVSAgentBridge,
                      br_dvr_process.OVSDVRProcessMixin):
    """openvswitch agent tunnel bridge specific logic."""

    # Used by OVSDVRProcessMixin
    dvr_process_table_id = constants.DVR_PROCESS
    dvr_process_next_table_id = constants.PATCH_LV_TO_TUN

    def setup_default_table(self, patch_int_ofport, arp_responder_enabled):
        pass

    def provision_local_vlan(self, network_type, lvid, segmentation_id,
                             distributed=False):
        pass

    def reclaim_local_vlan(self, network_type, segmentation_id):
        pass

    def install_flood_to_tun(self, vlan, tun_id, ports, deferred_br=None):
        pass

    def delete_flood_to_tun(self, vlan, deferred_br=None):
        pass

    def install_unicast_to_tun(self, vlan, tun_id, port, mac,
                               deferred_br=None):
        pass

    def delete_unicast_to_tun(self, vlan, mac, deferred_br=None):
        pass

    def install_arp_responder(self, vlan, ip, mac, deferred_br=None):
        pass

    def delete_arp_responder(self, vlan, ip, deferred_br=None):
        pass

    def setup_tunnel_port(self, network_type, port, deferred_br=None):
        pass

    def cleanup_tunnel_port(self, port, deferred_br=None):
        pass

    def add_dvr_mac_tun(self, mac, port):
        pass

    def remove_dvr_mac_tun(self, mac):
        pass

    def deferred(self):
        return self
