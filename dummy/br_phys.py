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

from neutron.plugins.ml2.drivers.openvswitch.agent.common import constants
from neutron.plugins.ml2.drivers.openvswitch.agent.openflow.dummy \
    import br_dvr_process
from neutron.plugins.ml2.drivers.openvswitch.agent.openflow.dummy \
    import ovs_bridge


class OVSPhysicalBridge(ovs_bridge.OVSAgentBridge,
                        br_dvr_process.OVSDVRProcessMixin):
    """openvswitch agent physical bridge specific logic."""

    # Used by OVSDVRProcessMixin
    dvr_process_table_id = constants.DVR_PROCESS_VLAN
    dvr_process_next_table_id = constants.LOCAL_VLAN_TRANSLATION

    def setup_default_table(self):
        pass

    def provision_local_vlan(self, port, lvid, segmentation_id, distributed):
        pass

    def reclaim_local_vlan(self, port, lvid):
        pass

    def add_dvr_mac_vlan(self, mac, port):
        pass

    def remove_dvr_mac_vlan(self, mac):
        pass
