import xml.etree.ElementTree as ET

from ansible.errors import AnsibleError
from ansible.plugins.inventory import BaseInventoryPlugin

try:
    import libvirt
except ImportError:
    raise AnsibleError('The labcli inventory plugin requires libvirt-python.')


class InventoryModule(BaseInventoryPlugin):
    NAME = 'labcli'

    def verify_file(self, path):
        return True

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)

        conn = libvirt.openReadOnly('qemu:///system')

        for dom in conn.listAllDomains():
            tree = ET.fromstring(dom.XMLDesc())
            desc = tree.find('description')

            if desc is not None:
                if desc.text.startswith('labcli:'):
                    address, groups = desc.text.split(':')[1:]
                    if ',' in groups:
                        groups = groups.split(',')
                    else:
                        groups = [groups]

                    for group in groups:
                        self.inventory.add_group(group)
                        self.inventory.add_host(host=dom.name(), group=group)

                    self.inventory.set_variable(dom.name(), 'ansible_host', address)

        conn.close()

