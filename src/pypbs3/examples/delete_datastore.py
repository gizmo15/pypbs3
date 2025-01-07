#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test proxmox api access."""

import json
import sys
import pathlib
from configparser import ConfigParser
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from pypbs3 import ProxAuth, PyProxmox

# Read conf.ini
INI_CONF = "./proxmox_api.ini"

if not pathlib.Path(INI_CONF).exists():
    print("Config file not found!")
    print(f"Need the config file in {INI_CONF}")
    sys.exit(1)

CONFIG = ConfigParser()
CONFIG.read(INI_CONF)

# DB parameters
URL = CONFIG.get('api', 'ipaddress')
USERAPI = CONFIG.get('api', 'user')
PASSWORD = CONFIG.get('api', 'passwd')

DATASTORE_NAME = 'backups'

disable_warnings(InsecureRequestWarning)

INIT_AUTHENT = ProxAuth(URL, USERAPI, PASSWORD)
PROXMOX_EXEC = PyProxmox(INIT_AUTHENT)

DATASTORES_LIST = PROXMOX_EXEC.get_datastore()

for DATASTORE in DATASTORES_LIST['data']:
    if DATASTORE_NAME not in DATASTORE['name']:
        print(f"Datastore {DATASTORE_NAME} not found !")
        sys.exit(1)
    else:
        print(f"Datastore {DATASTORE_NAME} found, deleting...")

DATA = {
    'destroy-data': 'true',
    'keep-job-configs': 'true',
}
STATUS = PROXMOX_EXEC.delete_datastore(DATASTORE_NAME, DATA)
STATUS_JSON = json.loads(STATUS)
RESULT_DATA = STATUS_JSON['data']
RESULT_CODE = STATUS_JSON['status']['code']
RESULT_REASON = STATUS_JSON['status']['reason']
print(RESULT_DATA)
print(RESULT_CODE)
print(RESULT_REASON)
