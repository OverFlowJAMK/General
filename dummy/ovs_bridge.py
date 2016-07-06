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


from neutron.agent.common import ovs_lib
from neutron.plugins.ml2.drivers.openvswitch.agent.common import constants \
        as ovs_consts
from neutron.plugins.ml2.drivers.openvswitch.agent.openflow \
    import br_cookie
from neutron.plugins.ml2.drivers.openvswitch.agent.openflow.dummy \
    import ofswitch


class OVSAgentBridge(ofswitch.OpenFlowSwitchMixin,
                     br_cookie.OVSBridgeCookieMixin, ovs_lib.OVSBridge):
    """Common code for bridges used by OVS agent"""

    def setup_controllers(self, conf):
        #controllers = [
        #    "tcp:%(address)s:%(port)s" % {
        #        "address": conf.OVS.of_listen_address,
        #        "port": conf.OVS.of_listen_port,
        #    }
        #]
        #self.set_protocols(ovs_consts.OPENFLOW13)
        #self.set_controller(controllers)
        pass

    def drop_port(self, in_port):
        pass
