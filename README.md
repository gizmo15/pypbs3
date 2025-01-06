pyproxmox
=========

## A Python wrapper for the Proxmox Backup Server API

### Installation and dependency

    pip install pypbs3 requests

###### Example usage

1. Import everything from the module

		from pypbs3 import ProxAuth, PyProxmox

2. Create an instance of the prox_auth class by passing in the
url or ip of a server in the cluster, username and password

		INIT_AUTHENT = ProxAuth('vnode01.example.org', 'apiuser@pbs', 'examplePassword')

ATTENTION! The realm can change : @pve or @pam, it depends on your configuration.

3. Create and instance of the pyproxmox class using the auth object as a parameter

		PROXMOX_EXEC = PyProxmox(INIT_AUTHENT)

4. Run the pre defined methods of the pyproxmox class

		STATUS = PROXPROXMOX_EXEC_EXEC.get_nodes()

NOTE They all return data in JSON format.

#### Methods requiring post_data

These methods need to passed a correctly formatted dictionary.
for example, if I was to use the createOpenvzContainer for the above example node
I would need to pass the post_data with all the required variables for proxmox.


Example for lxc :

	POST_DATA = {'ostemplate':'local:vztmpl/debian-10-standard_10.7-1_amd64.tar.gz',
				'vmid':'901','cores':'2','description':'test container',
				'rootfs':'10','hostname':'test.example.org','memory':'1024',
				'password':'testPassword','swap':'1024', 'ostype':'debian',
				'storage':'Stockage1'}

	PROXMOX_EXEC.create_openvz_container('vnode01', POST_DATA)

Example for kvm :

	POST_DATA = {'vmid':'9001', 'cores':'4', 'sockets': 1, 'description':'test kvm',
				'name':'test.example.org', 'memory':'1024', 'scsi0': 'Stockage1:102/vm-102-disk-0.qcow2,size=32G',
				'scsihw': 'virtio-scsi-pci', 'net0': 'virtio,bridge=vmbr1',
				'ide0': 'local:iso/fbsd-122-custom.iso,media=cdrom','ostype':'l26'}

	PROXMOX_EXEC.create_virtual_machine('vnode01', POST_DATA)

For more information on the accepted variables please see http//pve.proxmox.com/pve2-api-doc/

### Current List of Methods

#### GET Methods

##### Node Methods
		get_nodes()
"Get nodes list. Returns JSON"

##### Datasotre Methods
		get_datastore()
"List available datastores. Returns JSON"

		create_datastore(post_data)
"Create new datastore. Returns JSON"
