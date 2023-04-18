import json
from napalm import get_network_driver
import threading
import pandas as pd

################################################################

def input_file_ip_napalm():
    color.prYellow('**** USER input IP addresses separated by comma ****')       # print a message to the user
    color.prRed('ATTENTION: !!!')  # print a message to the user to inform him that he has only 3 attempts
    color.prYellow('you have 3 attempts only ') 

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
                    device = driver(ip,'u1','cisco', optional_args=en_password)
                    hosts_list.append(device)
                    return hosts_list
        except Exception as e:
            print('Error(', str(e) + ')')
            x += 1
            print(f'You have {3 - x} attempts left')
            if x == 3:
                print('You have exceeded the number of attempts')
                return None
###########################################


def input_user_ip_nap():        # function to get user input for IP addresses separated by comma
    color.prYellow('**** USER input IP addresses separated by comma ****')       # print a message to the user
    color.prRed('ATTENTION: !!!')  # print a message to the user to inform him that he has only 3 attempts
    color.prYellow('you have 3 attempts only ') 

    x=0                     # initialize x to 0 to be used in the while loop to count the number of attempts 
    while x < 3:       # while loop to count the number of attempts 
        try:      # try block to handle exceptions 
            IPS = input("Enter IPS separated by ',': ")         # get user input for IP addresses separated by comma
            hosts = IPS.split(',')          # split the user input by comma and store the result in a list called hosts
            hosts_list = []          # create an empty list called hosts_list 
            for ip in hosts:            # loop through the list hosts
                driver = get_network_driver('ios')
                en_password = {'secret': 'cisco'}
                device = driver(ip, 'u1', 'cisco', optional_args=en_password)
                hosts_list.append(device)

            return hosts_list            # return the list hosts_list
        except Exception as e:           # except block to handle exceptions
            print('Error(', str(e) + ')  \nTry again')      # print a message to the user and return None if an exception is raised
            x += 1                        # increment x by 1 to count the number of attempts
            color.prRed(f'You have {3 - x} attempts left')  # print a message to the user to inform him how many attempts he has left
            if x == 3:                  # if the number of attempts is equal to 3
                # print a message to the user to inform him that he has exceeded the number of attempts   
                color.prRed('You have exceeded the number of attempts')     
                return None          # return None          


################################################################
#arp table
################################################################
def get_arp(host):
    try:
        host.open()
        arptable = host.get_arp_table()
        output = json.dumps(arptable,sort_keys=True,indent=4)
        with open(f"get_arp{host}.txt", 'w') as fi:
            fi.write(output)
        with open(f'g') as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"get_arp{host}.txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df)
        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

def trubleshooting_arp():
    x = 0
    while x < 3:
        try:
            user = input('Enter 1 for file IPs or 2 for user input IPs: ')
            if user == '1':
                hosts_list = input_file_ip_napalm()
                if hosts_list == None:
                    return None
            elif user == '2':
                hosts_list = input_user_ip_nap()
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
        t = threading.Thread(target=get_arp, args=(host,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

################################################################
#interfaces
################################################################
def get_interfases(host):
    try:
        host.open()
        output =host.get_interfaces()
        output = json.dumps(output, sort_keys=True, indent=4)
        with open(f"get_interface{host}.txt", 'w') as f:
            f.write(output)
        with open(f"get_interface{host}.txt") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"get_interface{host}.txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df)



        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

#

def trubleshooting_interfacses():
    x = 0
    while x < 3:
        try:
            user = input('Enter 1 for file IPs or 2 for user input IPs: ')
            if user == '1':
                hosts_list = input_file_ip_napalm()
                if hosts_list == None:
                    return None
            elif user == '2':
                hosts_list = input_user_ip_nap()
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
        t = threading.Thread(target=get_interfases, args=(host,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

################################################################
#get mac address table
################################################################


def get_mac_address_table(host):
    try:
        host.open()
        output = host.get_mac_address_table()
        output = json.dumps(output, sort_keys=True, indent=4)
        with open(f"get_mac_address_table{host}.txt", 'w') as f:
            f.write(output)
        with open(f"get_mac_address_table{host}.txt") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"get_mac_address_table{host}.txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df)

        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

def trubleshooting_get_mac():
    x = 0
    while x < 3:
        try:
            user = input('Enter 1 for file IPs or 2 for user input IPs: ')
            if user == '1':
                hosts_list = input_file_ip_napalm()
                if hosts_list == None:
                    return None
            elif user == '2':
                hosts_list = input_user_ip_nap()
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
        t = threading.Thread(target=get_mac_address_table, args=(host,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

################################################################
# get facts 
################################################################
def get_facts(host):
    try:
        host.open()
        output = host.get_facts()
        output = json.dumps(output, sort_keys=True, indent=4)
        with open(f"get_facts{host}.txt", 'w') as f:
            f.write(output)
        with open(f"get_facts{host}.txt") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"get_facts{host}.txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df)

        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

def trubleshooting_facts():
    x = 0
    while x < 3:
        try:
            user = input('Enter 1 for file IPs or 2 for user input IPs: ')
            if user == '1':
                hosts_list = input_file_ip_napalm()
                if hosts_list == None:
                    return None
            elif user == '2':
                hosts_list = input_user_ip_nap()
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
        t = threading.Thread(target=get_facts, args=(host,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

################################################################
# get bgp neighbors
################################################################
def get_bgp_neighbour(host):
    try:
        host.open()
        output= host.get_bgp_neighbors_detail()
        output = json.dumps(output, sort_keys=True, indent=4)
        with open(f"get_bgp_neighbour{host}.txt", 'w') as f:
            f.write(output)
        with open(f"get_bgp_neighbour{host}.txt") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"get_bgp_neighbour{host}.txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df)

        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def trubleshooting_bgp_neighbour():
    x = 0
    while x < 3:
        try:
            user = input('Enter 1 for file IPs or 2 for user input IPs: ')
            if user == '1':
                hosts_list = input_file_ip_napalm()
                if hosts_list == None:
                    return None
            elif user == '2':
                hosts_list = input_user_ip_nap()
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
        t = threading.Thread(target=get_bgp_neighbour, args=(host,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

################################################################
# get vlan
################################################################
def vlan(host):
    try:
        host.open()
        output =host.get_vlans()
        output = json.dumps(output, sort_keys=True, indent=4)
        with open(f"vlan{host}.txt", 'w') as f:
            f.write(output)
        with open(f"vlan{host}.txt") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"vlan{host}.txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df)

        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def trubleshooting_vlan():
    x = 0
    while x < 3:
        try:
            user = input('Enter 1 for file IPs or 2 for user input IPs: ')
            if user == '1':
                hosts_list = input_file_ip_napalm()
                if hosts_list == None:
                    return None
            elif user == '2':
                hosts_list = input_user_ip_nap()
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
        t = threading.Thread(target=vlan, args=(host,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

################################################################
# get interfaces counters
################################################################
def get_interfaces_counters(host):
    try:
        host.open()
        host = get_network_driver('ios')
        output=host.get_interfaces_counters()
        output=json.dumps(output,sort_keys=True,indent=4)
        with open(f"get_interfaces_counters{host}.txt", 'w') as f:
            f.write(output)
        with open(f"get_interfaces_counters{host}.txt") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"get_interfaces_counters{host}.txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df)

        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def trubleshooting_interfaces_counter():
    x = 0
    while x < 3:
        try:
            user = input('Enter 1 for file IPs or 2 for user input IPs: ')
            if user == '1':
                hosts_list = input_file_ip_napalm()
                if hosts_list == None:
                    return None
            elif user == '2':
                hosts_list = input_user_ip_nap()
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
        t = threading.Thread(target=get_interfaces_counters, args=(host,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

################################################################
# get interfaces ip
################################################################
def get_interfaces_ip(host):
    try:
        host.open()

        output=host.get_interfaces_ip()
        output = json.dumps(output, sort_keys=True, indent=4)
        with open(f"get_interfaces_ip{host}.txt", 'w') as f:
            f.write(output)
        with open(f"get_interfaces_ip{host}.txt") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"get_interfaces_ip{host}.txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df)

        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def trubleshooting_interfave_ip():
    x = 0
    while x < 3:
        try:
            user = input('Enter 1 for file IPs or 2 for user input IPs: ')
            if user == '1':
                hosts_list = input_file_ip_napalm()
                if hosts_list == None:
                    return None
            elif user == '2':
                hosts_list = input_user_ip_nap()
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
        t = threading.Thread(target=get_interfaces_ip, args=(host,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

################################################################
def get_bgp_details(host):
    try:
        host.open()
        host = get_network_driver('ios')
        output=host.get_bgp_neighbors_detail()
        output = json.dumps(output, sort_keys=True, indent=4)
        with open(f"get_bgp_details{host}.txt", 'w') as f:
            f.write(output)
        with open(f"get_bgp_details{host}.txt") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"get_bgp_details{host}.txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df)

        host.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def trubleshooting_bgp_details():
    x = 0
    while x < 3:
        try:
            user = input('Enter 1 for file IPs or 2 for user input IPs: ')
            if user == '1':
                hosts_list = input_file_ip_napalm()
                if hosts_list == None:
                    return None
            elif user == '2':
                hosts_list = input_user_ip_nap()
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
        t = threading.Thread(target=get_bgp_details, args=(host,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
