""" PyTest testing 

On the test_GetDeviceSerialFromNetbox() test, make sure to set a valid firewall
"""
from firewall_output import *

def test_GetAsaInfo():
    """ Site info passes a three letter upper case site. """
    assert get_firewall_info('Site1') == 'Cisco ASA'

def test_GetMerakiInfo():
    """ Site info passes a three letter upper case site. """
    assert get_firewall_info('Site2') == 'Meraki MX'

def test_GetDeviceSerialFromNetbox():
    """ Function to test getting serial number from Netbox """
    assert get_device_serial_from_netbox('Site2') == 'Q2AS-DUAH-7S78'

def test_GetDeviceInfoAsa():
    """ Function to test full functionality. """
    assert '2737.26d6.ad51' in find_firewall_info('Site1')

def test_GetDeviceInfoMeraki():
    """ Function to test functionality of Meraki equivelant of ARP """
    assert '00:af:f2:36:6f:d9' in find_firewall_info('Site2')
