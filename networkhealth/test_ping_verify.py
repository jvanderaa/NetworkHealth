""" PyTest testing """
from ping_verify import *

def test_GetAsaIpAddressOfRemoteDevice():
    """ Pass in site code and get back the IP address to test against. """
    assert netbox_get_device_ip('Site1') == '192.0.2.82'

def test_GetAsaIpAddressOfRemoteDeviceUniqueSite():
    """
    Pass in the site code and get back the IP address to test
    against.
    """
    assert netbox_get_device_ip('Site3') == '192.0.2.64'

def test_GetMerakiIPAddressofRemoteDevice():
    """
    Pass in the site code and get back the IP address to test
    against.
    """
    assert netbox_get_device_ip('Site4') == '198.51.100.2'

def test_GetDeviceInfoAsa():
    """ Function to test full functionality. of GetDeviceInfoAsa """
    assert '0000.0c07.ac51' in find_firewall_info('')


def test_RunPingTestAgainstLoopback():
    """
    Run test against the IP address of the loopback
    """
    assert 'Success rate' in run_ping_test('203.0.113.1', 5, 1450, 'Loopback1')


def test_GetAsaInfo():
    """ Site info passing a Site Name. """
    assert get_firewall_info('Site1') == 'Cisco ASA'


def test_GetMerakiInfo():
    """ Site info passing a Site Name. """
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

def test_CheckArpHealthDEN():
    """ Function to test functionality of Site3 ARP Table"""
    assert True == check_arp_health('Site3')


def test_CheckArpHealthIFP():
    """ Function to test functionality of Site7 ARP Table"""
    assert True == check_arp_health('Site7')

def test_CheckArpHealthTUS():
    """ Function to test functionality of Site8 ARP Table"""
    assert True == check_arp_health('Site8')

def test_CheckArpHealthAUS():
    """ Function to test functionality of Site9 ARP Table"""
    assert True == check_arp_health('Site9')

def test_RunTestAgainstRemoteSite1():
    """
    Test ping of device against remote site type 1 (Site1). This will run for 100
    pings to keep testing time to a minimal
    """
    site = 'Site1'
    assert 'Success rate is 100 percent' in run_ping_test(
        netbox_get_device_ip(site), 100, 1400, 'Loopback1')

def test_RunTestAgainstRemoteSite2():
    """
    Test ping of device against remote site type 2 (Site1). This will run for 100
    pings to keep testing time to a minimal
    """
    site = 'Site2'
    assert 'Success rate is 100 percent' in run_ping_test(
        netbox_get_device_ip(site), 100, 1400, 'Loopback1')

def test_RunTestAgainstRemoteAUS():
    """
    Test ping of device against Remote type 1 (Site1). This will run for 100
    pings to keep testing time to a minimal
    """
    site = 'Site4'
    assert 'Success rate is 100 percent' in run_ping_test(
        netbox_get_device_ip(site), 100, 1400, 'Loopback1')


def test_VerifyHealthofSite3():
    """ Test of function for site health """
    assert determine_health('Site3') == {'ping': True, 'arp': True}


def test_VerifyHealthofSite4():
    """ Test of function for site health """
    assert determine_health('Site4') == {'ping': True, 'arp': True}
