import json
from napalm import get_network_driver
import threading
from netmiko import ConnectHandler
#################
## هدمج الاتنين مع بعض في واجهه واحده واحل مشكله الواجهه 
#######################
def input_user_ip_napalm():  # function to get user input for IP addresses
    try:  # عشان لو حصل ايررور يظهر في الترمنل
        IPS = input("Enter IPS separated by ',': ")
        hosts = IPS.split(',')
        hosts_list = []
        for ip in hosts:
            driver = get_network_driver('ios')
            en_password = {'secret': 'cisco'}
            device = driver(hostname=ip, username='u1', password='u1', optional_args=en_password)
            hosts_list.append(device)
            return hosts_list
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')
        return None


def input_file_ip_napalm():
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
                    device = driver(hostname=ip, username='u1', password='u1', optional_args=en_password)
                    hosts_list.append(device)
                    return hosts_list
        except Exception as e:
            print('Error(', str(e) + ')')
            x += 1
            print(f'You have {3 - x} attempts left')
            if x == 3:
                print('You have exceeded the number of attempts')
                return None


def arp_table():
    x = 0
    while x < 3:
        try:
            user = input('Enter 1 for file IPs or 2 for user input IPs: ')
            if user == '1':
                hosts_list = input_file_ip_napalm()
                if hosts_list == None:
                    return None
            elif user == '2':
                hosts_list = input_user_ip_napalm()
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
        interfaces =host.get_interfaces()
        output = json.dumps(interfaces, sort_keys=True, indent=4)
        print(output)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def get_mac_address_table(host):
    try:
        host.open()
        mac = host.get_mac_address_table()
        output = json.dumps(mac, sort_keys=True, indent=4)
        print(output)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def get_facts(host):
    try:
        host.open()
        facts = host.get_facts()
        output = json.dumps(facts, sort_keys=True, indent=4)
        print(output)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def get_bgp_neighbour(host):
    try:
        host.open()
        bgp_neighbour = host.get_bgp_neighbors_detail()
        output = json.dumps(bgp_neighbour, sort_keys=True, indent=4)
        print(output)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def vlan(host):
    try:
        host.open()
        vlan =host.get_vlans()
        output = json.dumps(vlan, sort_keys=True, indent=4)
        print(output)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def get_interfaces_counters(host):
    try:
        host.open()
        host = get_network_driver('ios')
        interfaces_counters=host.get_interfaces_counters()
        output = json.dumps(interfaces_counters, sort_keys=True, indent=4)
        print(output)

        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def get_interfaces_ip(host):
    try:
        host.open()

        interfaces_ip=host.get_interfaces_ip()
        output = json.dumps(interfaces_ip, sort_keys=True, indent=4)
        print(output)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def get_bgp_details(host):
    try:
        host.open()
        host = get_network_driver('ios')
        bgp_neighbors=host.get_bgp_neighbors_detail()
        output = json.dumps(bgp_neighbors, sort_keys=True, indent=4)
        print(output)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def get_bgp_config(host):
    try:
        host.open()
        host = get_network_driver('ios')
        bgp_config=host.get_bgp_config()
        output = json.dumps(bgp_config, sort_keys=True, indent=4)
        print(output)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def ping(host):
    try:
        host.open()
        host = get_network_driver('ios')
        ping=host.ping()
        output = json.dumps(ping, sort_keys=True, indent=4)
        print(output)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def traceroute(host):
    try:
        host.open()
        host = get_network_driver('ios')
        traceroute =host.traceroute()
        output = json.dumps(traceroute, sort_keys=True, indent=4)
        print(output)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

### netmiko
def show_runnig_protocol(host):
    try:
                connection = ConnectHandler(**host)
                prompt = connection.find_prompt()
                if '>' in prompt:
                    connection.enable()
                color.color.prPurple(f'Entered enable mode on ' + {host['host']})
                backup_config = connection.send_command('show ip protocols')
                connection.disconnect()
            
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

def show_runnig_protocol_thr():
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
                x += 1
                color.prRed('Error: Invalid input')
                color.prRed(f'You have {3 - x} attempts left')
                if x == 3:
                    color.prRed('You have exceeded the number of attempts')
                    return None
                
                print  # print a blank line to
                continue
            break

        except Exception as e:
            # fix this error print to red
            print('Error(', str(e) + ')')
            x += 1
            color.prRed(f'You have {3 - x} attempts left')
            if x == 3:
                color.prRed('You have exceeded the number of attempts')
                return None
            
    if hosts_list == None:
        color.prRed('Failed to load hosts')
        color.prRed('No hosts to configure')
        return None
    
    threads = []
    color.prYellow('Configuring devices')
    color.prYellow('Please wait... starting multi threads')
    for host in hosts_list:
        t = threading.Thread(target=show_runnig_protocol, args=(host,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()


#########################################################
def show_routing_table(host):
    try:
                connection = ConnectHandler(**host)
                prompt = connection.find_prompt()
                if '>' in prompt:
                    connection.enable()
                color.color.prPurple(f'Entered enable mode on ' + {host['host']})
                backup_config = connection.send_command('show ip route')
                connection.disconnect()
            
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

def show_routing_table_thr():
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
                x += 1
                color.prRed('Error: Invalid input')
                color.prRed(f'You have {3 - x} attempts left')
                if x == 3:
                    color.prRed('You have exceeded the number of attempts')
                    return None
                
                print  # print a blank line to
                continue
            break

        except Exception as e:
            # fix this error print to red
            print('Error(', str(e) + ')')
            x += 1
            color.prRed(f'You have {3 - x} attempts left')
            if x == 3:
                color.prRed('You have exceeded the number of attempts')
                return None
            
    if hosts_list == None:
        color.prRed('Failed to load hosts')
        color.prRed('No hosts to configure')
        return None
    
    threads = []
    color.prYellow('Configuring devices')
    color.prYellow('Please wait... starting multi threads')
    for host in hosts_list:
        t = threading.Thread(target=show_routing_table, args=(host,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

#########################################################

trubleshooting_options = '''
            [?] What do you want to perform?
            --------------------------------
            [1] Get ARP table
            [2] Get interface
            [3] Get MAC address table
            [4] Get facts
            [5] Get BGP neighbors 
            [6] Get vlan 
            [7] ping 
            [8] traceroute
            [9] Get BGP config
            [10] Get interface counter 
            [11] Exit
            --------------------------------
            '''

trubleshooting_options_dict = {
    '1': get_arp,
    '2': get_interfases,
    '3': get_mac_address_table,
    '4': get_facts,
    '5': get_bgp_neighbour,
    '6': vlan,
    '7': ping,
    '8': traceroute,
    '9': get_bgp_config ,
    '10': get_interfaces_counters,
    '11': exit,
    }

# هنعمل تارجت الثريد = تارجت الفانكشن اللي هتعملها لم اليور يختار رقم الفانكشن
#ونضيف دي الشاشه الرئيسيه 
def trubleshooting():
    while True:
        print(trubleshooting_options)
        user_input = input("Enter your choice: ")
        if user_input == '11':
            break
        elif user_input in trubleshooting_options_dict:
            trubleshooting_options_dict[user_input]()
        else:
            print("Invalid input. Please try again.")


