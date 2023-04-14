import json
from napalm import get_network_driver
import threading

trubleshooting_options = '''
            [?] What do you want to perform?
            --------------------------------
            [1] Get ARP table
            [2] Get interface
            [3] Get MAC address table
            [4] Get facts
            [5] Get BGP neighbors
            [6] Exit
            --------------------------------
            '''

trubleshooting_options_dict = {
    '1': get_arp,
    '2': get_interfases,
    '3': get_mac_address_table,
    '4': get_facts,
    '5': get_bgp_neighbors
    }

# هنعمل تارجت الثريد = تارجت الفانكشن اللي هتعملها لم اليور يختار رقم الفانكشن
#ونضيف دي الشاشه الرئيسيه 
def trubleshooting():
    while True:
        print(trubleshooting_options)
        user_input = input("Enter your choice: ")
        if user_input == '6':
            break
        elif user_input in trubleshooting_options_dict:
            trubleshooting_options_dict[user_input]()
        else:
            print("Invalid input. Please try again.")


def input_user_ip(): # function to get user input for IP addresses
    try:     #  عشان لو حصل ايررور يظهر في الترمنل
        IPS = input("Enter IPS separated by ',': ")
        hosts = IPS.split(',')
        hosts_list = []
        for ip in hosts:
            driver = get_network_driver('ios')
            en_password = {'secret': 'cisco'}
            device = driver(hostname=ip, username='u1', password='u1' ,optional_args=en_password)
            hosts_list.append(device)
            return hosts_list
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')
        return None



def input_file_ip():
    x = 0
    while x < 3:
        try:
            devicefile = input("Enter file name with IP addresses: ")
            with open(devicefile) as f:
                devices = f.read().splitlines()
                hosts_list = []
                for ip in devices:
                    driver = get_network_driver('ios')
                    en_password = {'secret': 'cisco'}
                    device = driver(hostname=ip, username='u1', password='u1' ,optional_args=en_password)
                    hosts_list.append(device)
                    return hosts_list
        except Exception as e:
            print('Error(', str(e) + ')')
            x += 1
            print(f'You have {3 - x} attempts left')
            if x == 3:
                print('You have exceeded the number of attempts')
                return None



def trubleshooting():
    x = 0
    while x < 3:
        try:
            user = input('Enter 1 for file IPs or 2 for user input IPs: ')
            if user == '1':
                hosts_list = input_file_ip()
                if hosts_list == None:
                    return None
            elif user == '2':
                hosts_list = input_user_ip()
                if hosts_list == None:
                    return None
            else:
                print('Error: Invalid input')
                print('please Try again')
                print  # print a blank line to
                continue
            break

        except Exception as e:
            print('Error(', str(e) + ')')
            x += 1
            print(f'You have {3 - x} attempts left')
            if x == 3:
                print('You have exceeded the number of attempts')
                return None

    if hosts_list == None:
        print('No hosts to configure')
        return None
    threads = []
    choose = input('1- Get ARP table\n2- Get interface \nEnter your choice: ')
    if choose == '1':
        target_func = get_arp()
    elif choose == '2':
        target_func = get_interfases()
    else:
        print('Invalid choice')
        return None
    
    for host in hosts_list:
        t = threading.Thread(target=target_func, args=(host,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()




def get_arp(host):
    try:
        host.open()
        arptable = host.get_arp_table()
        output = json.dumps(arptable, sort_keys=True, indent=4)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

def get_interfases(host):
    try:
        host.open()
        host.get_interfaces()
        output = json.dumps(arptable, sort_keys=True, indent=4)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

def get_mac_address_table(host):
    try:
        host.open()
        mac = host.get_mac_address_table()
        output = json.dumps(mac, sort_keys=True, indent=4)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

def get_facts(host):
    try:
        host.open()
        facts = host.get_facts()
        output = json.dumps(facts, sort_keys=True, indent=4)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

def get_bgp_neighbour(host):
    try:
        host.open()
        facts = host.get_bgp_neighbors_detail()
        output = json.dumps(facts, sort_keys=True, indent=4)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

def vlan(host):
    try:
        host.open()
        host=get_network_driver('ios')
        host.get_vlans()
        output = json.dumps(vlan, sort_keys=True, indent=4)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

def get_interfaces_counters(host):
    try:
        host.open()
        host=get_network_driver('ios')
        host.get_interfaces_counters()
        output = json.dumps(vlan, sort_keys=True, indent=4)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

def get_interfaces_ip(host):
    try:
        host.open()
        host=get_network_driver('ios')
        host.get_interfaces_ip()
        output = json.dumps(vlan, sort_keys=True, indent=4)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

def get_bgp_details(host):
    try:
        host.open()
        host=get_network_driver('ios')
        host.get_bgp_neighbors_detail()
        output = json.dumps(vlan, sort_keys=True, indent=4)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

def get_bgp_config(host):
    try:
        host.open()
        host=get_network_driver('ios')
        host.get_bgp_config()
        output = json.dumps(vlan, sort_keys=True, indent=4)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

def ping(host):
    try:
        host.open()
        host=get_network_driver('ios')
        host.ping()
        output = json.dumps(vlan, sort_keys=True, indent=4)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

def traceroute(host):
    try:
        host.open()
        host=get_network_driver('ios')
        host.traceroute()
        output = json.dumps(vlan, sort_keys=True, indent=4)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

