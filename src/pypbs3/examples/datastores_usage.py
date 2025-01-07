#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test proxmox api access."""

import sys
import pathlib
from configparser import ConfigParser
from time import strftime, localtime
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from pypbs3 import ProxAuth, PyProxmox


def convert_size(entry_size):
    """Convert size octets to gigabytes."""
    output_size = entry_size / 1024 / 1024 / 1024
    return output_size


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

disable_warnings(InsecureRequestWarning)

INIT_AUTHENT = ProxAuth(URL, USERAPI, PASSWORD)

PROXMOX_EXEC = PyProxmox(INIT_AUTHENT)

STATUS = PROXMOX_EXEC.get_datastores_usage()
for DATASTORE in STATUS['data']:
    print(DATASTORE['store'])
    DATASTORE_SIZE_TOTAL = DATASTORE['total']
    DATASTORE_SIZE_TOTAL_GB = round(convert_size(DATASTORE_SIZE_TOTAL), 2)
    DATASTORE_SIZE_USER = DATASTORE['used']
    DATASTORE_SIZE_USER_GB = round(convert_size(DATASTORE_SIZE_USER), 2)
    print(f"Datastore size : {DATASTORE_SIZE_TOTAL_GB}G")
    print(f"Datastore used : {DATASTORE_SIZE_USER_GB}G")
    FULL_TIME = strftime('%Y-%m-%d', localtime(DATASTORE['estimated-full-date']))
    print(f"Datastore full : {FULL_TIME}")
