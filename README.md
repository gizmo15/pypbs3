pypbs
=========

## A Python wrapper for the Proxmox Backup Server API

### Installation and dependency

    pip install pypbs3 requests

###### Example usage

1. Import everything from the module

		from pypbs3 import ProxAuth, PyProxmox

2. Create an instance of the prox_auth class by passing in the
url or ip of a server in the cluster, username and password

		INIT_AUTHENT = ProxAuth('pbs01.example.org', 'apiuser@pbs', 'examplePassword')

ATTENTION! The realm can change : @pve or @pam, it depends on your configuration.

3. Create and instance of the pyproxmox class using the auth object as a parameter

		PBS_EXEC = PyProxmox(INIT_AUTHENT)

4. Run the pre defined methods of the pyproxmox class

		STATUS = PBS_EXEC.get_datastore()

NOTE They all return data in JSON format.

#### Methods requiring post_data

These methods need to passed a correctly formatted dictionary.
for example, if I was to use the create_datastore for the above example node
I would need to pass the post_data with all the required variables for proxmox.


Example for datastore creation :

	DATA = {
		'name': DATASTORE_NAME,  # mandatory
		'path': DATASTORE_PATH,  # mandatory
		'verify-new': 'true',
	}

	PBS_EXEC.create_datastore(POST_DATA)

For more information on the accepted variables please see [PBS API DOC](https://pbs.proxmox.com/docs/api-viewer/index.html)

### Current List of Methods

#### GET Methods

##### Node Methods
		get_nodes()
"Get nodes list. Returns JSON"

##### Datasotre Methods
		get_datastore()
"List available datastores. Returns JSON"

		get_datastores_usage()
"Get usage of all datastores. Returns JSON"

		create_datastore(post_data)
"Create new datastore. Returns JSON"

		delete_datastore(datastore_name, post_data)
"Delete specific datastore. Returns JSON"
