#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test proxmox api access."""

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

disable_warnings(InsecureRequestWarning)

INIT_AUTHENT = ProxAuth(URL, USERAPI, PASSWORD)

PBS_EXEC = PyProxmox(INIT_AUTHENT)

STATUS = PBS_EXEC.get_nodes()
print(STATUS['data'])
