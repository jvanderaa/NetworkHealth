"""
# Automation for use on Network Services website.
# Author: Josh VanDeraa
# Date: 2018-01-12
# Updated: 2018-01-17
# Update Made: Completed Linter.
"""
from netmiko import ConnectHandler
from network_func import get_svc_info

def get_command_output(device_name='localhost', command='show cdp neigh'):
    """ Function to send a command to a device and get the output back.
    Update Needed: Instead of passing in just 'cisco_ios', need to get the
    appropriate driver definition.

    INPUTS
    device_name: Name of the device to connect to using DNS, expects that this
    is a valid name.
    command: command to be executed

    RETURN
    output from the command
    """
    username, password = get_svc_info()
    device_info = {
        'device_type': 'cisco_ios',
        'ip': device_name,
        'username': username,
        'password': password,
        'secret': password,
    }

    ssh_conn = ConnectHandler(**device_info)
    ssh_conn.enable()
    output = ssh_conn.send_command(command)
    return output

def main():
    """ Main code execution """
    print(get_command_output())

if __name__ == '__main__':
    main()
