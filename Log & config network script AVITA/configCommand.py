from netmiko import ConnectHandler
import getpass
import sys
import time


print("--------Avita Network Script--------")
print(" ")
userInput = input("Choose script to run(config or log): ")


#config script 
if userInput.upper() == 'CONFIG':

    i = input("Did you complete the configfile.txt & iplist.txt that is needed for this script?(y/n): ")

    if i.upper() != 'Y' :

        sys.exit("Please complete files")
        
    else:
        device = {
        'device_type': 'cisco_ios', 
        'ip': '',
        'username': '',
        'password': '',
        'secret':''
        }

        ipfile=open("iplist.txt")
        print ("Script for SSH to device, Please enter your credential")
        device['username']=input("User name: ")
        device['password']=getpass.getpass()
        print ("Enter enable password: ")
        device['secret']=getpass.getpass()
        configfile=open("configfile.txt")
        configset=configfile.read()
        configfile.close()

        for line in ipfile:
 
            device['ip']=line.strip("\n")
            print("\n\nConnecting Device ",line)
            net_connect = ConnectHandler(**device)
            net_connect.enable()
            time.sleep(2)
            print ("Passing configuration set ")
            net_connect.send_config_set(configset)
            print ("Device Conigured ")
 

        ipfile.close()
        print("Script Executed Successfully")

    

#log script
elif userInput.upper() == 'LOG':
    i = input("Have you completed device.txt?(y/n): ")

    if i.upper() != 'Y':
        sys.exit("Please complete file")
    else:

        Router = {
         'device_type': 'cisco_ios',
         'ip': '',
         'username': '',
         'password': '',
         'secret': ''
        }

        with open('devices.txt') as routers:
            print ("Script for Logging device, Please enter your credential")
            Router['username']=input("User name: ")
            Router['password']=getpass.getpass()
            print("Enter enable password: ")
            Router['secret']=getpass.getpass()

            for IP in routers:
                Router['ip']=IP.strip("\n")
                print("\n\nConnecting Device ",IP)    
                net_connect = ConnectHandler(**Router)
                net_connect.enable()
                hostname = net_connect.send_command('show run | i host')
                hostname.split(" ")
                hostname, device, *rest = hostname.split(" ")
                print ("Backing up " + device + "...")

                filename = (r'C:\Users\ddennison/') + device + '.txt'
                # to save backup to same folder as script use below line and comment out above line 
                # filename = device + '.txt' 

                showrun = net_connect.send_command('show run')
                showvlan = net_connect.send_command('show vlan')
                showver = net_connect.send_command('show ver')
                log_file = open(filename, "a")   # in append mode
                log_file.write(showrun)
                log_file.write("\n")
                log_file.write(showvlan)
                log_file.write("\n")
                log_file.write(showver)
                log_file.write("\n")
                print(device + " Log Completed")

    # Finally close the connection
        net_connect.disconnect()
        routers.close()
        print("Script Executed Successfully")
    
else:
    #default 
    print("invaild user input, please run again.")
