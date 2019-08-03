#!/usr/bin/python3
""" Script to log determine health of a link to a site."""
import datetime
import requests
from multiprocessing import Process, Manager, Pool
import random
import pprint
import time
from netmiko import ConnectHandler
from network_func import get_netbox_api, get_svc_info, get_meraki_key
from firewall_output import get_device_serial_from_netbox
# pylint: disable=C0325, W0601, E1305, W0703

def run_ping_test(dest_ip, ping_count, size, source_int):
    """ Function to run ping test """
    username, password = get_svc_info()
    device = {
        'device_type': 'cisco_ios',
        'ip': 'network_test_device',
        'username': username,
        'password': password,
    }
    net_connect = ConnectHandler(**device)
    # except:
    #     print('SSH Exception for: %s' % dest_ip)

    # Run a quick test to see if the site is online
    command = 'ping {} repeat 4'.format(dest_ip)
    output = net_connect.send_command(command)
    if '100 percent' not in output:
        print('Site may be down: %s' % dest_ip)
        return 'Site may be down.'

    # Run the full test
    command = 'ping {} repeat {} size {}'.format(dest_ip, ping_count, size, source_int)
    print('Sending command: \n{}'.format(command))
    try:
        output = net_connect.send_command(command)
        print(output)
    except IOError as myerror:
        print('In Error detection')
        print(output, myerror)
        output = 'Timeout Error Occurred.'

    net_connect.disconnect()
    return output


def get_dashboard_response(url, m_headers):
    """ Function to get response from Meraki Dashboard API """
    response = requests.get(url, headers=m_headers)
    return response.json()


def get_meraki_clients(site):
    """ Function to get the list of clients from the Meraki Dashboard."""
    m_key = get_meraki_key()
    m_base = 'https://dashboard.meraki.com/api/v0/'
    m_headers = {
        'X-Cisco-Meraki-API-Key': m_key,
        'Content-Type': 'application/json'
    }
    url = m_base + \
        'devices/%s/clients?timespan=500' % get_device_serial_from_netbox(site)
    client_list = get_dashboard_response(url, m_headers)
    output = '{:<12s}    {}      {}\n'.format(
        'IP Address', 'MAC Address', 'VLAN')
    for client in client_list:
        output += '{:<12s}  {}  VLAN{}\n'.format(
            client['ip'], client['mac'], client['vlan'])

    return output


def set_netbox_globals():
    """ Function to set globals when not used on main() function."""
    token = 'Token {}'.format(get_netbox_api())
    global HEADERS
    HEADERS = {'Authorization': token, 'content-type': 'application/json'}
    global BASE_URL
    BASE_URL = 'http://netbox.example.com/api/'


def get_netbox_response(url):
    """
    Function to get the response from netbox
    Returns: Response data.
    """
    response = requests.get(url, headers=HEADERS)
    return response.json()


def get_firewall_info(site='AUS'):
    """ Function to get the firewall type from Netbox based on the site"""
    set_netbox_globals()
    device_name = get_proper_firewall_name(site)
    print(device_name)
    url = BASE_URL + 'dcim/devices/?name={}'.format(device_name.upper())
    return get_netbox_response(url)['results'][0]['platform']['name']


def get_command_output(device_name='localhost', command='show arp'):
    """ Function to get the command output from a firewall."""
    username, password = get_svc_info()
    device_info = {
        'device_type': 'cisco_asa',
        'ip': device_name,
        'username': username,
        'password': password,
        'secret': password,
    }

    ssh_conn = ConnectHandler(**device_info)

    output = ssh_conn.send_command(command)
    return output


def get_proper_firewall_name(site):
    """
    Placeholder function to sanitize data based on custom business logic, such
    as normally all devices only have a single FW ending in FW01, except that
    other site because they had a wierd cutover during a life cycle, so they
    have FW02 type scenario.

    Returns the proper name as a string.
    """
    sites_with_custom = []
    if site in sites_with_custom:
        local_device = 'N{}FW0002'.format(site)
    else:
        local_device = 'N{}FW0001'.format(site)

    return local_device


def netbox_get_device_ip(site):
    """
    Function to get the device IP address for pinging. When calling the
    Netbox API, the format will come back as x.x.x.x/yy. So we also need to
    split this to being just the IP address.
    """
    # Set the Netbox global vars to be used.
    set_netbox_globals()

    # Set device name to upper case in case a lower case comes in
    site = site.upper()


    device_name = get_proper_firewall_name(site)

    url = '{}dcim/devices/?q={}'.format(BASE_URL, device_name)
    return get_netbox_response(url)['results'][0]['primary_ip']['address'].split('/')[0]


def check_arp_health(site):
    """
    Function to check the health and return True for ARP entries existing and
    False when there are not ARP entries in VLAN3, VLAN4, CUTE, , TKT or PCI
    """
    valid_arp_nets = ['VLAN3', 'VLAN4', 'inside']
    firewall_type = get_firewall_info(site)
    if firewall_type == 'Cisco ASA':
        arp_table = get_command_output(
            device_name=get_proper_firewall_name(site),
            command='show arp'
        )
    if firewall_type == 'Meraki MX':
        arp_table = get_meraki_clients(site)

    # Return True for some sort of address in the proper inside network segment
    if any(x in arp_table for x in valid_arp_nets):
        return True

    return False


def check_ping_health(site):
    """
    Function to check the health and return True for healthy, false for not
    healthy from a ping perspective.
    """
    ping_count = 200
    ping_test_results = run_ping_test(
        netbox_get_device_ip(site), ping_count, 1400, 'Loopback1')

    if ('{0}/{0}'.format(ping_count)) in ping_test_results or\
        ('{}/{}'.format(ping_count - 1, ping_count)) in ping_test_results:
        return True

    return False


def determine_health(site):
    """
    Function to get the health of the site, do any custom parsing of files, and
    report back True for a healthy site, False for an unhealthy site.
    """
    site_health = {}
    site = site.upper()

    site_health['arp'] = check_arp_health(site)
    try:
        site_health['ping'] = check_ping_health(site)
    except Exception as myexc:
        print(myexc)
        site_health['ping'] = False

    try:
        return_dict[site] = site_health
    except:
        pass
    # print(get_proper_firewall_name(site), site_health)
    return site_health, get_proper_firewall_name(site), site


def determine_health_all_sites():
    """
    Function to get the health of all sites at once. Setting up multi-processing
    of the determine_health() function. Leverages detemine_health() to figure
    out what the individual site health is.
    """
    global return_dict
    return_dict = {}
    site_list = make_site_list()
    queue_depth = 8

    jobs = []
    pool = Pool(queue_depth)
    my_return = (pool.map(determine_health, site_list))

    print(my_return)
    return my_return


def netbox_all_sites():
    """ Function to get raw information from Netbox about all sites."""
    set_netbox_globals()
    url = BASE_URL + 'dcim/sites/'
    data = get_netbox_response(url)
    return data


def make_site_list():
    """ Function to get all sites, then parse down to only the remote"""
    all_site_list = netbox_all_sites()
    site_list = []
    for site in all_site_list['results']:
        if site['custom_fields']['SiteType']['value'] == 4:
            site_list.append(site['name'])

    return site_list


def main():
    """ Main code execution when executed from prompt"""
    start_time = datetime.datetime.now()
    determine_health_all_sites()
    print('Time to complete: %s' % (datetime.datetime.now() - start_time))


if __name__ == '__main__':
    main()
