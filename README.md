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

##### Datastore Methods
		get_datastore()
"List available datastores. Returns JSON"

		get_datastores_usage()
"Get usage of all datastores. Returns JSON"

		create_datastore(post_data)
"Create new datastore. Returns JSON"

		update_datastore_info(datastore_name, post_data)
"Update specific datastore parameters. Returns JSON"

		delete_datastore(datastore_name, post_data)
"Delete specific datastore. Returns JSON"

##### Prune Methods
		get_prune_jobs()
"Get list of scheduled prune jobs. Returns JSON"

		get_prune_job_info()
"Get specific prune job informations. Returns JSON"

		create_prune_job(post_data)
"Create scheduled prune job. Returns JSON"

		update_prune_job_info(prune_id, post_data)
"Update specific prune job parameters. Returns JSON"

		delete_prune_job(prune_id)
"Delete specific prune job. Returns JSON"

##### Sync Methods
		get_sync_jobs()
"Get list of scheduled sync jobs. Returns JSON"

		get_prune_job_info()
"Get specific sync job informations. Returns JSON"

		create_sync_job(post_data)
"Create scheduled sync job. Returns JSON"

		update_sync_job_info(sync_id, post_data)
"Update specific sync job parameters. Returns JSON"

		delete_sync_job(sync_id)
"Delete specific sync job. Returns JSON"

##### Remote Methods
		get_remotes()
"Get list of remotes. Returns JSON"

		get_remote_target_info()
"Get specific remote informations. Returns JSON"

		create_remote_target(post_data)
"Create remote target. Returns JSON"

		update_remote_target(sync_id, post_data)
"Update specific remote target parameters. Returns JSON"

		delete_remote_targety(sync_id)
"Delete specific remote target. Returns JSON"

##### Metrics Methods
		get_server_metrics()
"Get backup server metrics. Returns JSON"

##### Verify Methods
		get_verify_jobs()
"Get list of all verify jobs. Returns JSON"

		get_verify_job_info()
"Get specific verify job informations. Returns JSON"

		create_verify_job(post_data)
"Create verify job. Returns JSON"

		update_verify_job(verify_id, post_data)
"Update specific verify job parameters. Returns JSON"

		delete_verify_job(verify_id)
"Delete specific verify job. Returns JSON"
