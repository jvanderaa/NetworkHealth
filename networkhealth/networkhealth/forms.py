from django import forms
import requests
from w_func import get_netbox_api

# pylint: disable=W0603, W0604, C0103
NETBOX_BASE_URL = "https://netbox.example.com"

def get_netbox_response(url):
    """
    Function to get the response from netbox
    Returns: Response data.
    """
    response = requests.get(url, headers=HEADERS)
    return response.json()


def netbox_all_sites():
    """ Function to get raw information from Netbox about all sites."""
    url = BASE_URL + 'dcim/sites/'
    data = get_netbox_response(url)
    return data


def netbox_asa_firewalls():
    """ Function to find all ASA Firewalls within Netbox. """
    url = f'{NETBOX_BASE_URL}api/dcim/devices/?device_type_id=14'
    data = get_netbox_response(url)
    return data


SITE_LIST = [
    ('None', '---'),
]

token = 'Token %s' % get_netbox_api()
global HEADERS
HEADERS = {'Authorization': token, 'content-type': 'application/json'}
global BASE_URL
BASE_URL = f'{NETBOX_BASE_URL}/api/'

all_site_list = netbox_all_sites()
for site in all_site_list['results']:
    if site['custom_fields']['SiteType']['value'] == 14:
        SITE_LIST.append((site['name'].lower, site['name']))


# Command lists to be leveraged by the tools. Switch list for switches, router
# List for routers. This is in the form of a tuple, first entry for the tuple
# should be the actual command running on the device, the second half is what
# is shown to the end user of the website.
SWITCH_COMMAND_LIST = (
    ('show mac address | exc CPU', 'Show MAC Address'),
    ('show interfaces', 'Show Interfaces'),
    ('show cdp neigh', 'Show CDP Neighbor'),
    ('show arp', 'Show ARP Table'),
    ('show int status', 'Show Interface Status'),
    ('show ip int brie', 'Show IP Interface Brief'),
    ('show log', 'Show Logs'),
    ('show version | i uptime', 'Find Uptime'),
    ('show proc cpu sorted | exc 0.0', 'Check CPU'),
    ('show clock', 'Show Clock'),
)

ROUTER_COMMAND_LIST = (
    ('show interfaces', 'Show Interfaces'),
    ('show ip bgp summary', 'BGP Summary'),
    ('show clock', 'Show Clock'),
    ('show log', 'Show Logs'),
    ('show ip interface brief', 'Show IP Interfaces Brief'),
    ('show interfaces description', 'Show Interface Descriptions')
)

ASA_COMMAND_LIST = (
    ('show arp', 'Show ARP Table'),
    ('show int ip brie', 'Check Interface Status'),
    ('show ip', 'Check Interface Names'),
)


class JustSiteListForm(forms.Form):
    token = 'Token %s' % get_netbox_api()
    global HEADERS
    HEADERS = {'Authorization': token, 'content-type': 'application/json'}
    global BASE_URL
    BASE_URL = f'{NETBOX_BASE_URL}/api/'

    site_list = [('None', '---')]
    all_site_list = netbox_all_sites()
    for site in all_site_list['results']:
            if site['custom_fields']['SiteType']['value'] == 14:
                site_list.append((site['name'].lower, site['name']))

    site = forms.CharField(
        label='Site', widget=forms.Select(choices=site_list))


class RouterSiteListForm(forms.Form):
    """ Class to define the form for router commands."""
    device_name = forms.CharField(label='Router', widget=forms.TextInput())
    command_choice = forms.CharField(
        label='Router Command', 
        widget=forms.Select(choices=ROUTER_COMMAND_LIST)
        )


class SiteListForm(forms.Form):
    # site = forms.CharField(
    #   label='Site (Not Currently Working)', 
    #   widget=forms.Select(choices=SITE_LIST)
    # )

    #### DEFINE NETBOX API INFORMATION #####
    token = 'Token %s' % get_netbox_api()
    global HEADERS
    HEADERS = {'Authorization': token, 'content-type': 'application/json'}
    global BASE_URL
    BASE_URL = f'{NETBOX_BASE_URL}/api/'
    #### END NETBOX API DEFINITION

    device_name = forms.CharField(
        label='Device name (No error checking yet)', 
        widget=forms.TextInput()
        )
    
    command_choice = forms.CharField(
        label='Command to run', 
        widget=forms.Select(choices=SWITCH_COMMAND_LIST)
        )


class SiteListArpForm(forms.Form):
    token = 'Token %s' % get_netbox_api()
    global HEADERS
    HEADERS = {'Authorization': token, 'content-type': 'application/json'}
    global BASE_URL
    BASE_URL = f'{NETBOX_BASE_URL}/api/'

    site_arp_list = [('None', '---')]
    all_site_list = netbox_all_sites()
    for site in all_site_list['results']:
            if site['custom_fields']['SiteType']['value'] == 14:
                site_arp_list.append((site['name'].lower, site['name']))

    out_command_list = (
        ('show arp', 'Show ARP Table'),
    )

    site = forms.CharField(label='Site', widget=forms.Select(choices=site_arp_list))
    command_choice = forms.CharField(label='Command', widget=forms.Select(choices=out_command_list))


class AsaFirewalls(forms.Form):
    token = 'Token %s' % get_netbox_api()
    global HEADERS
    HEADERS = {'Authorization': token, 'content-type': 'application/json'}
    global BASE_URL
    BASE_URL = f'{NETBOX_BASE_URL}/api/'

    device_list = [('None', '---')]

    asa_list = netbox_asa_firewalls()
    for asa in asa_list['results']:
        if 'OLD' in asa['name']:
            continue
        elif 'ASA' in asa['name']:
            # Exclude old ASA named
            continue
        elif "-2" in asa['name']:
            # Exclude the second firewall in a pair defined.
            continue
        elif "-1" in asa['name']:
            # ASA is part of HA pair, need to include this in the tuple.
            device_list.append((asa['name'].replace('-1', '').lower(), asa['name'].replace('-1', '')))
        else:
            device_list.append((asa['name'].lower(), asa['name']))

    device_name = forms.CharField(
        label='Device', widget=forms.Select(choices=device_list))
    command_choice = forms.CharField(
        label='Command to run', widget=forms.Select(choices=ASA_COMMAND_LIST))
