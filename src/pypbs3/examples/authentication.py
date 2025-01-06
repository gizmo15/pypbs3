#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    print("Need the config file in {}".format(INI_CONF))
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
PROXMOX_EXEC.get_nodes()
