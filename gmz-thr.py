import threading
from netmiko import ConnectHandler , NetmikoTimeoutException, NetmikoAuthenticationException ,NetmikoBaseException
from datetime import datetime
import  time , os , sys , pathlib , logging , ipaddress  , json , threading , requests ,schedule
from napalm import get_network_driver 
from napalm.base.exceptions import ConnectionException  , ConnectAuthError
import pandas as pd 


"""
extra  usefull functions

"""
def send_to_telegram(message):      # this function will send a message to telegram and take the message as a parameter 

    apiToken = '5803750722:AAGLa0rDUryF3lfsHWI1ycONlkpbR32V0dQ'     # get the token from @BotFather 
    chatID = '-1001694983867'                                       # get the chat id from @getmyid_bot
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'    # create the api url

    try:            # try to send the message 
        requests.post(apiURL, json={'chat_id': chatID, 'text': message})     # send the message
        print("sending to Telegram...")             # print a message
    except Exception as e:      # if there is an error
        e = 'Error'         # set the error message
        print(e)       # print the error message


class color:       # this class will print the text in different colors 
    def prRed(skk): print("\033[91m {}\033[00m" .format(skk))  # this function will print the text in red color
    def prGreen(skk): print("\033[92m {}\033[00m" .format(skk)) # this function will print the text in green color
    def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))    # this function will print the text in yellow color
    def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))  # this function will print the text in light purple color
    def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))   # this function will print the text in purple color
    def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))   # this function will print the text in cyan color
    def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))      # this function will print the text in light gray color
    def pr(skk): print('{}'.format(skk))

green="\033[1;32m"  # this variable will print the text in green color
red = "\033[1;31m"    # this variable will print the text in red color
yellow = "\033[1;33m"   # this variable will print the text in yellow color
purple = "\033[1;35m"  # this variable will print the text in purple color 
cyan = "\033[1;36m" # this variable will print the text in cyan color
blue = "\033[1;34m" # this variable will print the text in blue color
reset = "\033[0m"  # this variable will reset the color to default color


##########################################################################################
# This is a decorator function that will handle exceptions in netmiko module functions
# and will print a message to the user and return None if an exception is raised in the
# netmiko module functions
# This function will be used to decorate the following functions:
# 1. input_user_ip()
# 2. input_file_ip()
# 3. config_file()
# 4. configure_device_same()
# 5. configure_device_unique()
# 6. backup_device()
# and any other function that uses netmiko module functions

##########################################################################################
##########################################################################################


def netmiko_exception_handler(func):           # This is a decorator function takes a function as an argument
    start_time = time.time()
    def wrapper(*args, **kwargs):          # This is a wrapper function that will handle exceptions in netmiko module functions
            try:
                return func(*args, **kwargs)  # This will execute the function that is decorated by this decorator function
            except NetmikoTimeoutException as e:           # This will handle timeout errors
                print(f"Connection error: {str(e)} \nTry again'")  # and will print a message to the user and return None if an exception is raised in the
                return None
            except NetmikoAuthenticationException as e:  # this will handle authentication errors
                print(f"Authentication error: {str(e)}")
                return None                      # and will print a message to the user and return None if an exception is raised 
            except NetmikoBaseException as e:         # this will handle other errors during connection establishment
                print('Error(', str(e) + ')  \nTry again')
                return None    
            except Exception as e:             # this will handle other errors like :error message, retry the connection, or terminate the program.
                print(f"Error: {str(e)} \nTry again")
                return None
            finally:
                end_time = time.time()
                print(f"the {func.__name__} took "+ green+ f"{end_time - start_time}"+reset+ "seconds to run.")
                input("\033[1;33mPress Enter to return to the menu.\033[0m")
    return wrapper


##########################################################################################
"****************************************************************************************"
def napalm_exception_handler(func):
    start_time = time.time()
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except ConnectionException as e:
            print(f"Connection error: {str(e)}")
        except ConnectAuthError as e :
            print(f"Authentication error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            end_time = time.time()
            print(f"the {func.__name__} took "+ green+ f"{end_time - start_time}"+reset+ "seconds to run.")
            input("\033[1;33mPress Enter to return to the menu.\033[0m")
    return wrapper
##########################################################################################
# 1. Create a function that will take user input for IP addresses
# 2. Create a function that will take user input for IP file
# 3. Create a function that will take user input for configuration file
# 4. Create a function that will validate IP address
##########################################################################################
# @netmiko_exception_handler      # This will decorate the input_user_ip() function
def input_user_ip():        # function to get user input for IP addresses separated by comma
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
                cisco_device = {                # create a dictionary called cisco_device for each IP address in the list hosts
                    "device_type": "cisco_ios",
                    "ip": ip,
                    "username": "u1",               # username
                    "password": "cisco",           # password
                    'secret': 'cisco',            # enable password
                    'port': 22,                   # optional, defaults to 22 
                    'verbose': True              # set the verbose flag to True to print the output of the commands to the console
                }
                hosts_list.append(cisco_device)     # append the dictionary cisco_device to the list hosts_list
            return hosts_list            # return the list hosts_list
        except Exception as e:           # except block to handle exceptions
            print('Error(', str(e) + ')  \nTry again')      # print a message to the user and return None if an exception is raised
            x += 1                        # increment x by 1 to count the number of attempts
            color.prRed(f'You have {3 - x} attempts left')  # print a message to the user to inform him how many attempts he has left
            if x == 3:                  # if the number of attempts is equal to 3
                # print a message to the user to inform him that he has exceeded the number of attempts   
                color.prRed('You have exceeded the number of attempts')     
                return None          # return None          




#
#@netmiko_exception_handler     # This will decorate the input_file_ip() function
def input_file_ip():              # function to get user input for IP file
    color.prYellow('**** USER input file name with IP addresses ****')  # print a message to the user
    color.prRed('ATTENTION: !!!')       # print a message to the user to inform him that he has only 3 attempts
    color.prYellow('you have 3 attempts only ')
    x = 0                        # initialize x to 0 to be used in the while loop to count the number of attempts
    while x < 3:                # while loop to count the number of attempts
        try:                         # try block to handle exceptions
            devicefile = input("Enter file name with IP addresses: ")        # get user input for file name
            with open(devicefile) as f:                   # open the file and read the content
                devices = f.read().splitlines()               # split the content by line and store the result in a list called devices
                hosts_list = []                        # create an empty list called hosts_list
                for ip in devices:                  # loop through the list devices 
                    cisco_device = {                    # create a dictionary called cisco_device for each IP address in the list devices
                        'device_type': 'cisco_ios',     
                        'ip': ip,
                        'username': "u1",
                        'password': "cisco",
                        'port': 22,
                        'secret': "cisco",          # enable password
                        'verbose': True                
                    }
                    hosts_list.append(cisco_device)          # append the dictionary cisco_device to the list hosts_list
                return hosts_list           # return the list hosts_list
        except Exception as e:              # except block to handle exceptions
            print('Error(', str(e) + ')')           # print a message to the user and return None if an exception is raised
            x += 1                  # increment x by 1 to count the number of attempts
            color.prRed(f'You have {3 - x} attempts left')          # print a message to the user to inform him how many attempts he has left
            if x == 3:          # if the number of attempts is equal to 3
                color.prRed('You have exceeded the number of attempts')    # print a message to the user to inform him that he has exceeded the number of attempts
                time.sleep(1.5)
                return None             # return None
            
##########################################################################################

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
                    ip = ip.strip()
                    ip=str(ip)
                    hosts_list.append(ip)
                return hosts_list
        except Exception as e:
            print('Error(', str(e) + ')')
            x += 1
            print(f'You have {3 - x} attempts left')
            if x == 3:
                print('You have exceeded the number of attempts')
                return None
###########################################


def input_user_ip_napalm():        # function to get user input for IP addresses separated by comma
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
                ip = ip.strip()
                ip=str(ip)
                hosts_list.append(ip)
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
def config_file():           # function to get user input for configuration file
    color.prYellow('**** USER input file name with configuration ****')     # print a message to the user
    color.prRed('ATTENTION: !!!')
    color.prYellow('you have 3 attempts only ')
    x = 0
    while x < 3:
        try:
            config_file = input("Enter file name with configuration: ") 
            with open(config_file) as f:
                color.prGreen(f'{config_file} loaded successfully')
                return config_file
        except Exception as e:
            print('Error(', str(e) + ')')
            x += 1
            color.prRed(f'You have {3 - x} attempts left')
            print
            if x == 3:
                color.prRed('You have exceeded the number of attempts')
                return None

def validate_ip_address(address):   
    while True:                # Loop until a valid IP address is entered
        try:               # Try to create an IP address object
            ip = ipaddress.ip_address(address)       # If successful,
            color.prGreen("IP address {} is valid".format(address))   # print a message      
            return str(ip)                 # return the IP address as a string (for netmiko)
        except ValueError:              # If unsuccessful,
            color.prRed("IP address {} is not valid".format(address))     # print an error message
            address = input("Enter a valid IP address: ")    # and ask the user to enter a valid IP address
            continue
        else:
            break

"****************************************************************************************"
##########################################################################################
# 1. Create a function that configures multiple devices with same configuration file
##########################################################################################
def configure_device_same(host, configfile):
    color.prLightPurple(f'**** Configure device {host["ip"]} with same configuration file ****')
    try:
        connection = ConnectHandler(**host)
        color.prGreen(f'Connected to {host["ip"]}')
        prompt = connection.find_prompt()
        print(prompt)
        if '>' in prompt:
            connection.enable()
            print('Enable mode enabled')
        
        output = connection.send_config_from_file(configfile)
        print(output)
        color.prGreen(f'Configuration file {configfile} loaded successfully on {host["ip"]}')
        with open('output.txt', 'a') as f:
            f.write(output)
        
        connection.disconnect()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def multi_device_same_config():
    color.prYellow('**** Configure multiple devices with same configuration file ****')
    color.prRed('ATTENTION: !!!')
    color.prYellow('you have 3 attempts only ')
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

    configfile = config_file()

    if configfile == None:
        color.prRed('Failed to load config file')
        color.prRed('No config file to configure')
        return None
    
    threads = []
    color.prYellow('Configuring devices')
    color.prYellow('Please wait... starting multi threads')
    for host in hosts_list:
        t = threading.Thread(target=configure_device_same, args=(host, configfile))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()


"****************************************************************************************"
##########################################################################################
# 1. Create a function that configures multiple devices with a unique configuration file
#        for each device
##########################################################################################
def configure_device_unique(host):
    try:

        connection = ConnectHandler(**host)
        prompt = connection.find_prompt()
        print(prompt)
        if '>' in prompt:
            connection.enable()
            print('Enable mode enabled')
        color.prYellow(f'**** Configure device {host["ip"]} with unique configuration file ****')
        configfile=config_file()
        output = connection.send_config_from_file(configfile)
        print(output)
        color.prGreen(f'Configuration file {configfile} loaded successfully on {host["ip"]}')
        connection.disconnect()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


def multi_device_unique_config():
    """
    Prompt user for a list of device IPs, connect to each device,
    and send a configuration file to each device
    """
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
                print ('please Try again')
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
        t = threading.Thread(target=configure_device_unique, args=(host,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()




"****************************************************************************************"
##########################################################################################
# 1. Create a function that configures bgp on multiple devices
# un complete + missing some parameters  -edit later
'* fix it *' 
''' multi mpgb threads'''
##########################################################################################
def bgp():
    
    ip=validate_ip_address(input('enter router ip to connect :'))

    st=input('enter start vlan id :')
    end=input('enter end vlan id :')
    i = input('enter increment for vlan :')
    neighbor=validate_ip_address(input('enter neighbor ip :'))
    neighbor_as=input('enter neighbor AS :')
    
    cisco_device = {                  # Create the device object    
            "device_type": "cisco_ios",
            "ip":ip,
            "username": "u1",
            "password": "cisco",
            "secret": "cisco",
            "port": 22,
            "verbose": True
        }
    connection=ConnectHandler(**cisco_device) #connect to device
    promt =connection.find_prompt() #find prompt
    print(promt)  
    if '>' in promt:    #if prompt is > enter enable mode
            connection.enable()        #enter enable mode
            print('Enable mode enabled')
        
    connection.send_command_timing('conf t') #enter config terminal
    connection.send_command_timing('router bgp 1 ') #enter bgp
    connection.send_command_timing(f'neighbor {neighbor} remote-as {neighbor_as}')
    connection.send_command_timing(f'no auto-summary')
    for vlan in range(int(st),int(end),int(i)):
        connection._send_command_timing_str(f'net 192.168.{vlan}.0 mask 255.255.255.0')
        print("done")

    connection.disconnect()

def mp_bgp():
    
    ip=validate_ip_address(input('enter router IP to connect :'))
    ebgp_neighbour = input('enter ebgp neighbour ip :')
    ibgp_neighbour = input('enter ibgp neighbours ip seprated by , :')
    ibgp_neighbours=ibgp_neighbour.split(',') 
    cisco_device = {                  # Create the device object
            "device_type": "cisco_ios",
            "ip":ip,
            "username": "u1",
            "password": "cisco",
            "secret": "cisco",
            "port": 22,
            "verbose": True
        }
    connection=ConnectHandler(**cisco_device) #connect to device
    
    connection.enable()        #enter enable mode
    connection.send_command_timing('conf t') #enter config terminal
    connection.send_command_timing(f'router bgp 300 ')
    for ibgp in ibgp_neighbours:
        print(ibgp)
        connection.send_command_timing(f'neighbor {ibgp} remote-as 300 ')
        connection.send_command_timing(f'neighbor {ibgp} update-source lo0 ')
        connection.send_command_timing('address-family vpnv4 ')
        connection.send_command_timing(f'neighbor {ibgp} activate ')
        connection.send_command_timing(f'neighnor {ibgp} send-community both ')
        connection.send_command_timing('exit-address-family ')
        print("done")
    connection.send_command_timing('address-family ipv4 vrf net ')
    connection.send_command_timing(f'neighbor {ebgp_neighbour} remote-as 1 ')
    connection.send_command_timing(f'neighbor {ebgp_neighbour} activate ')
    connection.send_command_timing(f'neighbor {ebgp_neighbour} as override ')
    print("All done")
    connection.disconnect()




"***************************************************************************************"
##########################################################################################
# 1. Create a function that configures vlan on multiple devices  and eable dhcp pool
#######******** un complete * add multi threading * Error handling *********##############
'* fix it *'
##########################################################################################

def create_vlan(host,st,end,i):
    color.prYellow('********** Create VLANs **********')

    connection=ConnectHandler(**host)
    promt =connection.find_prompt()
    print(promt)
    if '>' in promt:
        connection.enable()
        print('enter enable mode')
    connection.send_command_timing ("conf t ")
    promt = connection.find_prompt()
    print(promt)
    for vlan in range(int(st),int(end),int(i)):
        send="vlan "+str(vlan)+" "
        print (send)
        print ("*"*5)
        print(f'{send} {host["ip"]}') 
        output=connection.send_command_timing(send)
        print(output)
    connection.disconnect()

@netmiko_exception_handler
def vlan_create():
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
    st = input('enter start vlan id :')
    end = input('enter end vlan id :')
    i = input('enter increment for vlan :')

    threads = []
    for host in hosts_list:
        t = threading.Thread(target=create_vlan, args=(host,st,end,i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    color.prGreen('********** VLANs created **********')


#def int_vlan(ip):  

def int_vlan():
    color.prYellow('********** configure interface vlan **********')
    ip=validate_ip_address(input('enter ip address :'))
    getway=validate_ip_address(input('enter getway ip address :'))       
    st=input('enter start vlan id :')
    end=input('enter end vlan id :')
    i = input('enter increment for vlan :')
    cisco_device = {                  # Create the device object    
            "device_type": "cisco_ios",
            "ip":ip,
            "username": "u1",
            "password": "cisco",
            "secret": "cisco",
            "port": 22,
            "verbose": True
        }
    connection=ConnectHandler(**cisco_device) #connect to device
    promt =connection.find_prompt() #find prompt
    print(promt)  
    if '>' in promt:    #if prompt is > enter enable mode
            connection.enable()        #enter enable mode
            print('entering enable mode...')    
    connection.send_command_timing('conf t')         #enter config terminal
    connection.send_command_timing(f'ip route 0.0.0.0 255.255.255.255 '+getway) #add default route
    ask=input('enter active or standby:') #ask for active or standby
    for vlan in range(int(st),int(end),int(i)): #loop for vlan id 
            print(vlan) 
            vlan=str(vlan)
            if ask=='active' or ask=='Active'or ask=='A' or ask=='a': 
                
                connection.send_command_timing(f'sppaning tree vlan {vlan} root primary')
                connection.send_command_timing(f'interface vlan {vlan}')
                connection.send_command_timing(f'ip address 192.168.{vlan}.1')
                connection.send_command_timing(f'ip helper-address {getway}')
                connection.send_command_timing(f'standby {vlan} priorty 150')
                connection.send_command_timing(f'standby {vlan} ip 192.168.{vlan}.3')
                connection.send_command_timing('no shut')
                print(vlan + ' is done')
                
            elif ask=='standby' or ask=='Standby'or ask=='S' or ask=='s':
                
                connection.send_command_timing(f'sppaning tree vlan {vlan} root secondary')
                connection.send_command_timing(f'interface vlan {vlan}')
                connection.send_command_timing(f'ip address 192.168.{vlan}.2')
                connection.send_command_timing(f'ip helper-address {getway}')
                connection.send_command_timing(f'standby {vlan} priorty 100')
                connection.send_command_timing(f'standby {vlan} ip 192.168.{vlan}.3')
                connection.send_command_timing('no shut')

            else:
                print('wrong input')
                break

    connection.disconnect()


#define function for dhcp  pool 

def dhcp():
    color.prYellow('''********** DHCP **********''')
    ip=validate_ip_address(input('enter router IP to connect :'))

    st=input('enter start vlan id :')
    end=input('enter end vlan id :')
    i = input('enter increment for vlan :')
    cisco_device = {                  # Create the device object
            "device_type": "cisco_ios",
            "ip":ip,
            "username": "u1",
            "password": "cisco",
            "secret": "cisco",
            "port": 22,
            "verbose": True
        }
    connection=ConnectHandler(**cisco_device)
    promt =connection.find_prompt()
    print(promt)
    if '>' in promt:
            connection.enable()
            print('enter enable mode')
    connection.send_command_timing('conf t')
    for vlan in range(int(st),int(end),int(i)):   #loop for vlan id 
            print(vlan)
            vlan=str(vlan)
            connection.send_command_timing(f'ip dhcp excluded-address 192.168.{vlan}.1 192.168.{vlan}.10')
            connection.send_command_timing(f'ip dhcp pool data{vlan}')
            connection.send_command_timing(f'network 192.168.{vlan}.0')
            connection.send_command_timing(f'default-router 192.168.{vlan}.3')
            print(vlan + ' is done')
    
    connection.disconnect()

##########################################################################################
##########################################################################################
##########################################################################################
""" NAPALM """
##########################################################################################

################################################################
#arp table
################################################################
def get_arp(host):
    try:
        driver = get_network_driver('ios')
        en_password = {'secret': 'cisco'}
        device = driver(hostname= host,username='u1',password='cisco', optional_args=en_password)
        device.open()
        arptable = device.get_arp_table()
        output = json.dumps(arptable,sort_keys=True,indent=4)
        with open(f"get_arp {host}.txt", 'w') as fi:
            fi.write(output)
        with open(f"get_arp {host}.txt" ,"r") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"get_arp {host}.txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df.to_string())
        device.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

@napalm_exception_handler
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
        driver = get_network_driver('ios')
        en_password = {'secret': 'cisco'}
        device = driver(hostname= host,username='u1',password='cisco', optional_args=en_password)
        device.open()
        interface =device.get_interfaces()
        output = json.dumps(interface, sort_keys=True, indent=4)
        with open(f"get_interface {host}.txt", 'w') as f:
            f.write(output)
        with open(f"get_interface {host}.txt") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"get_interface{host}.txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df.to_string())
        device.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

@napalm_exception_handler
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
        driver = get_network_driver('ios')
        en_password = {'secret': 'cisco'}
        device = driver(hostname= host,username='u1',password='cisco', optional_args=en_password)
        device.open()
        mac_add = device.get_mac_address_table()
        output = json.dumps(mac_add, sort_keys=True, indent=4)
        with open(f"get_mac_address_table {host}.txt", 'w') as f:
            f.write(output)
        with open(f"get_mac_address_table {host}.txt") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"get_mac_address_table {host}.txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df.to_string())
        device.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

@napalm_exception_handler
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
        driver = get_network_driver('ios')
        en_password = {'secret': 'cisco'}
        device = driver(hostname= host,username='u1',password='cisco', optional_args=en_password)
        device.open()
        output = device.get_facts()
        output = json.dumps(output, sort_keys=True, indent=4)
        with open(f"get_facts {host}.txt", 'w') as f:
            f.write(output)
        with open(f"get_facts {host}.txt") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"get_facts {host}.txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df.to_string())

        device.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

@napalm_exception_handler
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
        t = threading.Thread(target=get_facts, args=(host,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


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
        t = threading.Thread(target=get_facts, args=(host,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

################################################################
# get vlan
################################################################
def vlan(host):
    try:
        driver = get_network_driver('ios')
        en_password = {'secret': 'cisco'}
        device = driver(hostname= host,username='u1',password='cisco', optional_args=en_password)
        device.open()
        output =device.get_vlans()
        output = json.dumps(output, sort_keys=True, indent=4)
        with open(f"vlan{host} .txt", 'w') as f:
            f.write(output)
        with open(f"vlan{host} .txt") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"vlan{host} .txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df.to_string())

        device.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')


@napalm_exception_handler
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
        driver = get_network_driver('ios')
        en_password = {'secret': 'cisco'}
        device = driver(hostname= host,username='u1',password='cisco', optional_args=en_password)
        device.open()
        output=device.get_interfaces_counters()
        output=json.dumps(output,sort_keys=True,indent=4)
        with open(f"get_interfaces_counters {host}.txt", 'w') as f:
            f.write(output)
        with open(f"get_interfaces_counters {host}.txt") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"get_interfaces_counters {host}.txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df.to_string())

        device.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

@napalm_exception_handler
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
        driver = get_network_driver('ios')
        en_password = {'secret': 'cisco'}
        device = driver(hostname= host,username='u1',password='cisco', optional_args=en_password)
        device.open()
        output=device.get_interfaces_ip()
        output = json.dumps(output, sort_keys=True, indent=4)
        with open(f"get_interfaces_ip {host}.txt", 'w') as f:
            f.write(output)
        with open(f"get_interfaces_ip {host}.txt") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"get_interfaces_ip {host}.txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df.to_string())

        device.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

@napalm_exception_handler
def trubleshooting_interface_ip():
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
        t = threading.Thread(target=get_interfaces_ip, args=(host,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

################################################################
def get_bgp_details(host):
    try:
        driver = get_network_driver('ios')
        en_password = {'secret': 'cisco'}
        device = driver(hostname= host,username='u1',password='cisco', optional_args=en_password)
        device.open()
        output=device.get_bgp_neighbors_detail()
        output = json.dumps(output, sort_keys=True, indent=4)
        with open(f"get_bgp_details {host}.txt", 'w') as f:
            f.write(output)
        with open(f"get_bgp_details {host}.txt") as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
        print(df)
        with open(f"get_bgp_details {host}.txt", 'w') as fi:
            fi.seek(0)
            fi.truncate()
            fi.write(df.to_string())

        device.close()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

@napalm_exception_handler
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
        t = threading.Thread(target=get_bgp_details, args=(host,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


################################################################
""" monitoring + backup """
##########################################################################################
# 1. Create a function that will backup the configuration of multiple devices
#    to a folder on the local machine with the name of the device and the date and time
#     of the backup at same time
##########################################################################################

def configure_device_backup(host ,newpath,hour,minute,second):
    try:
                connection = ConnectHandler(**host)
                print(f"connecting to device {host['ip']}")
                
                prompt = connection.find_prompt()
                if '>' in prompt:
                    connection.enable()
                color.prPurple(f"Entered enable mode on {host['ip']}")
                backup_config = connection.send_command('show run')
    
                print(f"connected to device{host['ip']}")
                file_name = f"{newpath}" + f"\\{host['ip']}__{hour}-{minute}-{second}.txt"     # create a new file in the new folder
                with open(file_name, 'w') as f:         # w: write, r: read, a: append
                    f.write(backup_config)         # write the output of the show run command to the file
                print(f"Backup completed for device{host['ip']}")
                send_to_telegram(f"Backup completed for device{host['ip']}")
                connection.disconnect()
            
    except Exception as e:
        print(f"Connection failed to device{host['ip']}")
        print("Backup failed")
        print('Error(', str(e) + ')  \nTry again')

def backup_all():
    try:
        with open('devices') as f:          # reading the devices ip address from a file into a list (each ip on its own line)
            devices = f.read().splitlines()     # reading the devices ip address from a file into a list (each ip on its own line)

        device_list = list()            # creating an empty list
        for ip in devices:                  # iterating over the list with the devices ip addresses
            cisco_device = {                     # Create the device object
                'device_type': 'cisco_ios',     
                'ip': ip,
                'username': 'u1',
                'password': 'cisco',
                'port': 22,
                'secret': 'cisco' , #this is the enable password
                'verbose': True      # optional, for troubleshooting
            }
            device_list.append(cisco_device)
        date = datetime.now()       # get the current date and time
        year = date.year           # get the year    
        month = date.month         # get the month
        day = date.day           # get the day
        hour = date.hour           # get the hour
        minute = date.minute       # get the minute
        second = date.second       # get the second
        path=pathlib.Path(__file__).parent.resolve()     # get the path of this script
                # print(path)                                     # print the path of this script
        newpath = rf'{path}\backup {year}-{month}-{day}'        # create a new folder in the same directory with this script
        if not os.path.exists(newpath):     # check if the folder exists
            os.makedirs(newpath)        # if not, create it
            print(f'\ncreate backup folder at {newpath}')         # print the path of the new folder
        else:
            print(f'\nbackup folder already exists at {newpath}')
        threads = []
        print(threads)
        for host in device_list:
            t = threading.Thread(target=configure_device_backup, args=(host,newpath,hour,minute,second ))
            threads.append(t)
            t.start()
        print(threads)
        for t in threads:
            
            t.join()
    except Exception as e:
        print('Error(', str(e) + ')  \nTry again')

@netmiko_exception_handler
def schedule_backup():
    ask = input('Do you want to schedule daily backup? (y/n): ')
    if ask == 'y'or ask == 'Y'or ask == 'yes' or ask == 'Yes':
        hour = int(input("Enter the hour (0-23) to schedule the backup: "))
        minute = int(input("Enter the minute (0-59) to schedule the backup: "))
        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(backup_all)
        color.prGreen(f"Scheduled daily backup for {hour:02d}:{minute:02d}")
        while True:
            schedule.run_pending()
            time.sleep(1)
    elif ask == 'n' or ask == 'N' or ask == 'no' or ask == 'No':
        color.prYellow('start ONE TIME backup')
        backup_all()
    else:
        color.prRed('Invalid input')
        schedule_backup()


"****************************************************************************************"
##########################################################################################
# 1 . Create a function that will monitor if any of the interfaces on a device goes down
#     and if it does, try to bring it back up again using the "no shut" command
#     and if it doesn't work, send an alart to the network team
##########*********           un completed yet      ************* #############
'* fix it *'

##########################################################################################

def monitor_interfaces(host):   
    
    connection = ConnectHandler(**host)
    while True:
        try:
            output = connection.send_command('show ip interface brief')
            print(output) 
            print('*********************************')
            interfaces = output.splitlines()  # split the output into a list of interfaces
        #    print(interfaces)
        #    print('---------------------------------')
            interfaces.pop(0)  # remove the first line of the output
          #  print(interfaces)
            for interface in interfaces:
            #    print(interface)
                if not "unassigned" in interface :

                    if 'down' in interface:
                        down_interface = interface.split()[0]
                        print(f'Interface {down_interface} is down')
                        print('---------------------------------')

                        down_strip = down_interface.strip()   
                        print(down_strip)
                        print('---------------------------------')
 #                      if "FastEthernet" in down_strip:
  #                     out = "f " + down_strip[12:]
   #                    print(out)
    #                   elif "GigabitEthernet" in down_strip:
     #                   out = "g " + down_strip[15:]
      #                 elif "Ethernet" in down_strip:
       #                 out = "e " + down_strip[8:]
        #               elif "Loopback" in down_strip:
         #               out = "loopback" + down_strip[8:]
          #             elif "Serial" in down_strip:
           #             out = "s " + down_strip[6:]

                        print(connection.find_prompt())
                        connection.enable()        
                        connection.send_command_timing('conf t ') #
                        connection.send_command_timing(f'int {down_strip} ')
                        connection.send_command_timing('no shut ')
                        connection.send_command_timing('end ')
                        print(f'Interface {down_interface} is up')
                        send_to_telegram(f'Interface {down_interface} is up')
                # send an alert email, text message, or any other action
            time.sleep(10)       #error in this line
        except:
            print("Error in monitoring interfaces")
            break 


                    #     if in_errors > 100:          # test for input errors on the interface
                    #       print(f"Interface {intf} on {device['hostname']} has {in_errors} input errors.")

##########################
@netmiko_exception_handler
def monitor_interfaces_th():   
        color.prYellow('**** Configure multiple devices with same configuration file ****')
        color.prRed('ATTENTION: !!!')
        color.prYellow('you have 3 attempts only ')
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
            color.prRed('No hosts to monitor')
            return None
    

    
        threads = []
        color.prYellow('monitoring devices')
        color.prYellow('Please wait... starting multi threads')
        for host in hosts_list:
            t = threading.Thread(target=monitor_interfaces, args=(host,))
            threads.append(t)
            t.start()
    
        for t in threads:
            t.join()


                    #     if in_errors > 100:          # test for input errors on the interface
                    #       print(f"Interface {intf} on {device['hostname']} has {in_errors} input errors.")

#----------------------------



###########################################################################################
# Main program  cli interface
###########################################################################################


def logo():     # this function will print the logo of the tool
    hti = cyan+'''  
 _    _ _______ _____ 
| |  | |__   __|_   _|
| |__| |  | |    | |  
|  __  |  | |    | |  
| |  | |  | |   _| |_ 
|_|  |_|  |_|  |_____|
Electrical  Engineering 
          &
 Computers  Department
  Graduation Project
''' + reset+green+'''
         A-M-Z 
Network Management Tool '''+reset + '\n' # this is the logo of the tool
   
    terminal_width = os.get_terminal_size().columns - 10 # Get the width of the terminal window to center the logo 

    # Calculate the number of spaces needed to center the logo
    num_spaces = (terminal_width - len(hti.split("\n")[0])) // 2

    # Add the spaces to the beginning of each line of the logo string
    centered_HTI = "\n".join([" " * num_spaces + line for line in hti.split("\n")])     # this will center the logo

    centered_logo = centered_HTI+ '\n' +red+'\n''[+]'+blue+ ''' Coded By:'''+ yellow+"    Ahmed - Mariam - Alzhraa"+red+'\n' + red + '[+]'+blue+''' supervised by :'''+ yellow+'''    Dr. ESLAM SAMY EL-MOKADEM '''+red+'\n'+red+'[+]'+blue+''' Version:'''+yellow+'''    1.0'''+red+'\n'+red+'[+]'+blue+''' Description:'''+yellow+'''    AUTOMATED NETWORK CONFIGURATION MANAGEMENT , MONITORING AND BACKUP TOOL'''+reset+'\n'
    return centered_logo # return the logo to the main program

###########################################################################################
''' fix the bug in the menu function
choose no and the program will exit not working'''

def menu():
    while True:
        choice = str(input(yellow+'\n [?] Do you want to continue? \n> '+ reset)).lower()
        if choice[0] == 'y':
            return
        elif choice[0] == 'n':
            print(red+'[!] Exiting...'+reset)
            sys.exit(0)
        else:
            print('[!]'+red+'Please enter a valid choice'+reset)
            continue

# options menu 
main_options = '''
            [?] What do you want to do?
            \033[1;31m--------------------------------\033[0m
            [1] Configure devices
            [2] trubleshooting devices
            [3] Monitoring devices
            [4] Backup devices
            [5] Exit
            \033[1;31m--------------------------------\033[0m
            '''
main_dict = {
    "1" : lambda:None,
    "2" : lambda:None,
    "3" : monitor_interfaces_th,
    "4" : schedule_backup,
    "5" : lambda: sys.exit()
    }   
conf_option = '''
            [?] What do you want to perform?
            \033[1;31m--------------------------------\033[0m
            [1] Multi device same config
            [2] Multi device unique config
            [3] BGP
            [4] MP-BGP
            [5] Create VLAN
            [6] Interface VLAN
            [7] DHCP
            [8] \033[1;33mBack to main menu\033[0m
            \033[1;31m--------------------------------\033[0m
            '''

# options menu commands and functions 
conf_dic = {
	"1" : multi_device_same_config,
	"2" : multi_device_unique_config,
    "3" : bgp,
    "4" : mp_bgp,
    "5" : vlan_create,
    "6" : int_vlan,
    "7" : dhcp ,
    "8" : lambda : None,
}

trubleshooting_option = '''
            [?] What do you want to perform?
            \033[1;31m--------------------------------\033[0m
            [1] Get Arp table
            [2] Get Mac address table
            [3] Get interface status
            [4] Get interface counters
            [5] Get interface ip address
            [6] Get vlans
            [7] Get bgp neighbors
            [8] Get Facts
            [9] \033[1;33mBack to main menu\033[0m
            \033[1;31m--------------------------------\033[0m
            '''

trubleshooting_dic = {
    "1" : trubleshooting_arp,
    "2" : trubleshooting_get_mac,
    "3" : trubleshooting_interfacses,
    "4" : trubleshooting_interfaces_counter,
    "5" : trubleshooting_interface_ip,
    "6" : trubleshooting_vlan,
    "7" : trubleshooting_bgp_details,
    "8" : trubleshooting_facts,
    "9" : lambda : None,
}


def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')   # clear the screen 
        color.pr(logo())    # print the logo of the tool

        try:   # try to get the choice from the user
            choice = input("\n%s" % main_options + blue+'[+] You choose: ' + reset)                 # get the choice from the user
            if choice not in main_dict:                       # if the user enter a wrong choice
                print ('[!]'+ red+'Invalid Choice' + reset)             # print a message
                input(yellow+'[!] Press Enter to start over'+reset)
                continue                    # continue the loop
            # if the user enter a valid choice
            if choice == '1':           # if user selects submenu
                while True:             # submenu loop
                    os.system('cls' if os.name == 'nt' else 'clear')
                    color.pr(logo())    # print the logo of the tool
                    try:
                        conf_choice = input("\n%s" % conf_option + blue + '[+] You choose: ' + reset)
                        if conf_choice == '8':  # exit submenu and go back to main menu
                            break
                        conf_dic.get(conf_choice)()  # call function based on sub_choice
                    except KeyboardInterrupt:
                        print(red + '[!] Ctrl + C detected\n[!] Exiting' + reset)
                        sys.exit(0)
                    except EOFError:
                        print(red + '[!] Ctrl + D detected\n[!] Exiting' + reset)
                        sys.exit(0)
                    except:
                        print('[!]' + red + 'Invalid Choice' + reset)
                        input(red + '[!] Press Enter to start over' + reset)
                        continue
            elif choice == '2':  # if user selects submenu
                while True:  # submenu loop
                    os.system('cls' if os.name == 'nt' else 'clear')
                    color.pr(logo())  # print the logo of the tool
                    try:
                        trub_choice = input("\n%s" % trubleshooting_option + blue + '[+] You choose: ' + reset)
                        if trub_choice == '9':  # exit submenu and go back to main menu
                            break
                        trubleshooting_dic.get(trub_choice)()  # call function based on sub_choice
                    except KeyboardInterrupt:
                        print(red + '[!] Ctrl + C detected\n[!] Exiting' + reset)
                        sys.exit(0)
                    except EOFError:
                        print(red + '[!] Ctrl + D detected\n[!] Exiting' + reset)
                        sys.exit(0)
                    except:
                        print('[!]' + red + 'Invalid Choice' + reset)
                        input(red + '[!] Press Enter to start over' + reset)
                        continue
            main_dict.get(choice)()          # call the function of the choice
        except KeyboardInterrupt:            # if the user press ctrl + c
            print (red+'[!] Ctrl + C detected\n[!] Exiting'+ reset)        # print a message
            sys.exit(0)             # exit the program
        except EOFError:            # if the user press ctrl + d
            print (red+'[!] Ctrl + D detected\n[!] Exiting' +reset )            # print a message
            sys.exit(0)
        except:
            print ('[!]'+ red+'Invalid Choice' + reset)             # print a message
            input(red+'[!] Press Enter to start over'+reset)
            continue


def type_out(string):
    for char in string:
        print(char, end="", flush=True  )
        time.sleep(0.007)
def welcome():
    type_out(yellow+"      Welcome!        to our        AMZ TOOL\n" + reset)
    type_out("      --------------------------------------\n" )
    type_out(yellow+"This tool is designed to help you to manage your network devices\n" + reset)
    type_out("----------------------------------------------------------------\n" )
    type_out(logo())
    type_out(main_options+blue+'[+] You choose: ' + reset)
    time.sleep(.01)





if __name__ == "__main__":          # if the program is running directly
    main()
