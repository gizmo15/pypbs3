#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A python wrapper for the Proxmox 2.x API.

Example usage:

1) Create an instance of the prox_auth class by passing in the
url or ip of a server, username and password:

a = prox_auth('vnode01.example.org','apiuser@pbs','examplePassword')

2) Create and instance of the pyproxmox class using the auth object as a parameter:

b = pyproxmox(a)

3) Run the pre defined methods of the pyproxmox class.
NOTE: they all return data, usually in JSON format:

status = b.get_clusterStatus('vnode01')

For more information see https://github.com/Daemonthread/pyproxmox.
"""

import sys
import json
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
import requests


# Authentication class
class ProxAuth:
    """
    The authentication class, requires three strings:

    1. An IP/resolvable url (minus the https://)
    2. Valid username, including the @pve or @pam
    3. A password

    Creates the required ticket and CSRF prevention token for future connections.

    Designed to be instanciated then passed to the new pyproxmox class as an init parameter.
    """
    def __init__(self, url, username, password):
        self.url = url
        self.connect_data = {"username": username, "password": password}
        self.full_url = "https://{}:8007/api2/json/access/ticket".format(self.url)

        self.setup_connection()

    def setup_connection(self):
        """Setup connection to api."""
        self.ticket = ""
        self.csrf = ""

        self.response = requests.post(self.full_url,
                                      verify=False,
                                      data=self.connect_data,
                                      timeout=5)
        result = self.response

        if not self.response.ok:
            raise AssertionError('Authentification Error: HTTP Result: \n {}'.format(self.response))

        self.returned_data = {'status': {'code': self.response.status_code, 'ok': self.response.ok,
                                         'reason': self.response.reason}}
        self.returned_data.update(result.json())

        self.ticket = {'PBSAuthCookie': self.returned_data['data']['ticket']}
        self.csrf = self.returned_data['data']['CSRFPreventionToken']


# The meat and veg class
class PyProxmox:
    """
    A class that acts as a python wrapper for the Proxmox 2.x API.
    Requires a valid instance of the prox_auth class when initializing.

    GET and POST methods are currently implemented along with quite a few
    custom API methods.
    """
    # INIT
    def __init__(self, auth_class):
        """Take the prox_auth instance and extract the important stuff"""
        self.auth_class = auth_class
        self.get_auth_data()

    def get_auth_data(self,):
        """Get authentication data."""
        self.url = self.auth_class.url
        self.ticket = self.auth_class.ticket
        self.csrf = self.auth_class.csrf

    def connect(self, conn_type, option, post_data):
        """
        The main communication method.
        """
        self.full_url = "https://{}:8007/api2/json/{}".format(self.url, option)

        httpheaders = {'Accept': 'application/json',
                       'Content-Type': 'application/x-www-form-urlencoded'}
        disable_warnings(InsecureRequestWarning)
        if conn_type == "post":
            httpheaders['CSRFPreventionToken'] = str(self.csrf)
            self.response = requests.post(self.full_url, verify=False,
                                          data=post_data,
                                          cookies=self.ticket,
                                          headers=httpheaders,
                                          timeout=5)

        elif conn_type == "put":
            httpheaders['CSRFPreventionToken'] = str(self.csrf)
            self.response = requests.put(self.full_url, verify=False,
                                         data=post_data,
                                         cookies=self.ticket,
                                         headers=httpheaders,
                                         timeout=5)
        elif conn_type == "delete":
            httpheaders['CSRFPreventionToken'] = str(self.csrf)
            self.response = requests.delete(self.full_url, verify=False,
                                            data=post_data,
                                            cookies=self.ticket,
                                            headers=httpheaders,
                                            timeout=5)
        elif conn_type == "get":
            self.response = requests.get(self.full_url, verify=False,
                                         cookies=self.ticket,
                                         timeout=5)

        try:
            self.returned_data = self.response.json()
            self.returned_data.update({'status': {'code': self.response.status_code,
                                                  'ok': self.response.ok,
                                                  'reason': self.response.reason}})
            return self.returned_data
        except json.JSONDecodeError:
            print("Error in trying to process JSON")
            print(self.response)
            if (self.response.status_code == 401 and
               (not sys._getframe(1).f_code.co_name == sys._getframe(0).f_code.co_name)):
                print("Unexpected error: {} : {}".format(str(sys.exc_info()[0]),
                                                         str(sys.exc_info()[1])))
                print("try to recover connection auth")
                self.auth_class.setup_connection()
                self.get_auth_data()
                return self.connect(conn_type, option, post_data)

    # Methods using the GET protocol to communicate with the Proxmox API.
    # Cluster Methods

    def get_nodes(self):
        """Get cluster status information. Returns JSON"""
        data = self.connect('get', 'nodes', None)
        data_json = json.dumps(data, indent=4, sort_keys=True)
        return json.loads(data_json)


if __name__ == "__main__":
    print("Module to interact with proxmox api")
