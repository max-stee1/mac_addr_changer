import subprocess
import optparse
import re

"""This function used for gettign arguments"""
def get_arguments():
    parser = optparse.OptionParser()
    """arguments to get the interface"""
    parser.add_option("-i", "--interface", dest="interface", help="Use this for select interface")
    """arguments to get the new mac"""
    parser.add_option("-m", "--mac", dest="mac", help="Specify A new mac addr.Mac Addr look like **:**:**:**:**:**")
    (options, args) = parser.parse_args()
    "This part of code is using to confirm every arguments have been Inputted by the user"
    if not options.interface:
        parser.error("Please specify a Interface, Use --help for more Info.")
    elif not options.mac:
        parser.error("Please specify a Mac Addr, Use --help for more Info")
    return options

""""This function used for changing the mac"""
def mac_change(interface, mac_addr):
    print("Changing mac addr for " + interface + " to " + mac_addr)
    """Used for disable the interface"""
    subprocess.call(['sudo', 'ifconfig', interface, 'down'])
    """Used for changing the mac"""
    subprocess.call(['sudo', 'ifconfig', interface, 'hw', 'ether', mac_addr])
    """"Used for enable the interface"""
    subprocess.call(['sudo', 'ifconfig', interface, 'up'])

"""This fuction used for get current mac"""
def get_current_mac(interface):
    """used for get the ifconfig result"""
    ifconfig_result = subprocess.check_output(['ifconfig', interface])
    """split the mac address from ifconfig result"""
    mac_addr_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    """"checking Is the program found a mac addr or not"""
    if mac_addr_search_result:
        """returning the result"""
        return mac_addr_search_result.group(0)
    else:
        print("[+]Could found the mac addr")

"""call function for understood the arguments"""
options = get_arguments()
"""call function for get current mac before changed"""
current_mac = get_current_mac(options.interface)
"""Checking the mac addr before change and print it."""
print("Current Mac = " + str(current_mac))
"""call function for change the mac"""
mac_change(options.interface, options.mac)
"""checking mac address after  change"""
current_mac = get_current_mac(options.interface)
"""comparing the mac addr to decide either it's change or not. then print it"""
if current_mac == options.mac:
    print("Your Mac was Successfully Changed to " + options.mac)
else:
    print("Your Mac was not changed!!")
