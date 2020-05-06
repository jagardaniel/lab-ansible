# lab-ansible

A small lab environment for playing around with Ansible. It uses a dynamic inventory script to find VMs in libvirt with a specific description prefix. This is to only find VMs that has been created by the lab-cli tool. It then parses the description to find the IP address and the Ansible groups it should belong to.


## Installation

Clone git repository
```bash
daniel ~/git $ git clone git@github.com:jagardaniel/lab-ansible.git
```

Create a python virtualenv somewhere and activate it
```bash
daniel ~/git $ python3 -m venv venv
daniel ~/git $ source venv/bin/activate
```

Install python requirements
```bash
(venv) daniel ~/git $ cd lab-ansible
(venv) daniel ~/git/lab-ansible $ pip install -r requirements.txt
```

You should now be able to see your VMs in the inventory
```bash
(venv) daniel ~/git/lab-ansible $ ansible-inventory --list
{
    "_meta": {
        "hostvars": {
            "web01": {
                "ansible_host": "192.168.100.10"
            },
            "web02": {
                "ansible_host": "192.168.100.11"
            }
        }
    },
    "all": {
        "children": [
            "ungrouped",
            "webservers"
        ]
    },
    "webservers": {
        "hosts": [
            "web01",
            "web02"
        ]
    }
}
```

Ansible should also be able to reach them if you have the private key in the right place (default is `~/.ssh/labcli_private`) with correct permissions and if VMs are up and running. The path to the private key can be changed in `ansible.cfg` (private_key_file).
```bash
(venv) daniel ~/git/lab-ansible $ ansible -m ping all
web01 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
web02 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/libexec/platform-python"
    },
    "changed": false,
    "ping": "pong"
}
```

## Run playbooks
...
