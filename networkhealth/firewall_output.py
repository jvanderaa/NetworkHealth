import requests
from netmiko import ConnectHandler
from network_func import get_svc_info, get_netbox_api, get_meraki_key

# pylint: disable=W0604, C0325

token = 'Token %s' % get_netbox_api()
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


def get_dashboard_response(url, m_headers):
    """ Function to get response from Meraki Dashboard API """
    response = requests.get(url, headers=m_headers)
    return response.json()


def netbox_all_sites():
    """ Function to get raw information from Netbox about all sites."""
    url = BASE_URL + 'dcim/sites/'
    data = get_netbox_response(url)
    return data


def get_device_serial_from_netbox(site):
    """ Function to get from netbox the serial number of a device. Primarily
    used for Meraki Firewalls to feed into the dashboard. """
    url = BASE_URL + 'dcim/devices/?name=N' + site + 'FW0001'
    return get_netbox_response(url)['results'][0]['serial']


def get_meraki_clients(site):
    """
    Function to get all of the clients for a particular Meraki site.
    Formats the output for display and returns clients on a Meraki network so
    the output looks somewhat similar to a Cisco device output
    """
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
        output += '{:<12s}  {}    {}\n'.format(client['ip'], client['mac'], client['vlan'])

    return output


def get_command_output(device_name='N100MSPFW0001', command='show arp'):
    """ Function to get the command output from an ASA device"""
    username, password = get_svc_info()
    device_info = {
        'device_type': 'cisco_asa',
        'ip': device_name,
        'username': username,
        'password': password,
        'secret': password,
    }

    ssh_conn = ConnectHandler(**device_info)
    # ssh_conn.enable()
    # ssh_conn.send_command('terminal pager 0')
    output = ssh_conn.send_command(command)
    return output


def get_firewall_info(site='MSP1'):
    """ Function to get the firewall type from Netbox based on the site"""
    url = BASE_URL + 'dcim/devices/?name=N' + site + 'FW0001'
    return get_netbox_response(url)['results'][0]['platform']['name']


def find_firewall_info(site, command='show arp'):
    """
    Function to determine the type of firewall that the device is based on info
    in Netbox!
    """
    if site == None:
        return 'No site selected. Please reload'

    local_device = 'N' + site + 'FW0001'

    if get_firewall_info(site) == 'Cisco ASA':
        print(local_device)
        return get_command_output(device_name=local_device, command=command)

    if get_firewall_info(site) == 'Meraki MX':
        return get_meraki_clients(site=site)


def main():
    """ Main code execution """
    print(find_firewall_info('DEN'))
    exit()
    get_firewall_info()

if __name__ == '__main__':
    main()
