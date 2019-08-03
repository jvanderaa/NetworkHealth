#!/usr/bin/python
""" Base functions for use by Sun Country scripts.
Author: Josh VanDeraa
Date: 2017/06/23

"""
from __future__ import print_function
import os
import getpass
import json
import requests
import yaml

BASE_NETBOX_URL = "https://netbox.example.com"
def open_file():
    """
    NEEDS TO BE REFACTORED! This is where credentials should be gathered for use
    by the site.

    Return my_vars in the form of a dictionary
    """
    my_vars = {}
    my_vars['username'] = username_func()
    my_vars['password'] = password_func()
    my_vars['netbox_api'] = get_netbox_key()
    my_vars['meraki_key'] = get_meraki_key()

    return my_vars

def get_netbox_api():
    """
    NEED TO REFACTOR
    """
    netbox_api = ''
    return netbox_api

def get_meraki_key():
    """
    NEED TO REFACTOR
    """
    meraki_key = ''
    return meraki_key


def netbox_get_ip_address_id(ipaddress, headers):
    """ Function to return from Netbox the IP address ID. """
    base_url = f'{BASE_NETBOX_URL}/api/ipam/ip-addresses/?q='
    ip_url = base_url + ipaddress
    ipaddress = ipaddress + '/32'

    response = requests.get(ip_url, headers=headers)
    data = response.json()

    # If the IP address does not exist already, create it.
    if data['count'] == 0:
        post_address_url = f'{BASE_NETBOX_URL}/api/ipam/ip-addresses/'
        post_address_dict = {
            "address": ipaddress
        }
        post_address_data = json.dumps(post_address_dict)
        response = requests.post(url=post_address_url, headers=headers, data=post_address_data)
        ipadd_data = response.json()

        return ipadd_data['id']

    return data['results'][0]['id']

def netbox_check_for_ip(ipaddress, headers):
    """ Function to check for an IP address in Netbox.
    Returns True if the IP address exists in Netbox. Returns False if not.
    """
    # Define the URL of the API call
    base_url = f'{BASE_NETBOX_URL}/api/ipam/ip-addresses/?q='
    ip_url = base_url + ipaddress

    response = requests.get(ip_url, headers=headers)
    data = response.json()

    if data['count'] > 0:
        return True

    return False

def netbox_get_interface_id(interface_name, api_key, device_id):
    """ Function to get the interface ID number.
    Returns the interface ID if found, False if not found.
    """
    token = 'Token %s' % api_key
    headers = {'Authorization': token, 'content-type': 'application/json'}

    int_list_url = f'{BASE_NETBOX_URL}/api/dcim/interfaces/?device_id='
    int_list_url = int_list_url + str(device_id)

    response = requests.get(int_list_url, headers=headers)
    data = response.json()

    for result in data['results']:
        if result['name'] == interface_name:
            return result['id']

    return False

def netbox_device_exists(host, api_key):
    """ Function to verify that the host is already defined in Netbox. If so,
    return the relevant information back to the script.
    """
    token = 'Token %s' % api_key
    headers = {'Authorization': token, 'content-type': 'application/json'}

    base_url = f'{BASE_NETBOX_URL}/api/dcim/devices/?name='

    #Check to see if device is in Netbox by checking the count.
    url = base_url + host
    response = requests.get(url, headers=headers)
    data = response.json()

    if data['count'] > 0:
        # Find device id number
        my_id = data['results'][0]['id']

        if data['results'][0]['platform']['name'] == 'Cisco IOS':
            return {'device_type': 'cisco_ios', 'id': my_id}
        elif data['results'][0]['platform']['name'] == 'Cisco ASA':
            return {'device_type': 'cisco_asa', 'id': my_id}
        elif data['results'][0]['platform']['name'] == 'Cisco NX-OS':
            return {'device_type': 'cisco_nxos', 'id': my_id}
        else:
            print('Unable to get device type properly out of Netbox for Netmiko')
            print('Exiting')
            exit()

    return False

def netbox_get_site_id(netdevice):
    """ Function to get the device site ID from Netbox.
    """
    pass

def netbox_get_tenant_id(tenant_name):
    """ Function to get the tenant id from the tenant name.
    """
    pass

def get_netbox_platform(netdevice):
    """ Function to get the platform ID from Netbox based on the device.
    """
    pass

def netbox_post_info(url, data):
    """ Function to post data to Netbox """
    headers = {'Authorization': get_netbox_api, 'content-type': 'application/json'}
    response = requests.post(url, data=data, headers=HEADERS)
    return response.json()

def netbox_get_device_id(host, headers):
    """ Function to get the device ID from Netbox.
    Returns the netbox ID if found.
    Returns False if unable to find an ID.
    """
    url = f'{BASE_NETBOX_URL}/api/dcim/devices/?q=%s' % host
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['results'][0]['id']

def main():
    """ Not used, this is used for function loading only."""
    print('Please do not use as individual application.')

if __name__ == '__main__':
    main()
