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

import re

from oslo_log import log as logging

from neutron._i18n import _LW

LOG = logging.getLogger(__name__)

# Field name mappings (from Ryu to ovs-ofctl)
_keywords = {
    'eth_src': 'dl_src',
    'eth_dst': 'dl_dst',
    'ipv4_src': 'nw_src',
    'ipv4_dst': 'nw_dst',
    'table_id': 'table',
}


class OpenFlowSwitchMixin(object):
    """Mixin to provide common convenient routines for an openflow switch."""

    @staticmethod
    def _conv_args(kwargs):
        for our_name, ovs_ofctl_name in _keywords.items():
            if our_name in kwargs:
                kwargs[ovs_ofctl_name] = kwargs.pop(our_name)
        return kwargs

    def dump_flows(self, table_id):
        return self.dump_flows_for_table(table_id)

    def dump_flows_all_tables(self):
        return self.dump_all_flows()

    def install_goto_next(self, table_id):
        pass

    def install_output(self, port, table_id=0, priority=0, **kwargs):
        pass

    def install_normal(self, table_id=0, priority=0, **kwargs):
        pass

    def install_goto(self, dest_table_id, table_id=0, priority=0, **kwargs):
        pass

    def install_drop(self, table_id=0, priority=0, **kwargs):
        pass

    def delete_flows(self, **kwargs):
        pass

    def _filter_flows(self, flows):
        pass

    def cleanup_flows(self):
        pass
