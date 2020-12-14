# coding: utf-8
import csv
import sys
import os
import threading
import time
import fabric
from fabric import Connection, task

#local_script_path = 'C:/Users/Administrator/Downloads/migration-test/oneclick'
local_script_path = os.path.dirname(__file__)
port = 22

def migration(servers_login):
    print ("launthing thread...")
    #print str(servers_login)
    for i in servers_login.keys():
        if str(i) == 'Password':
            passw= servers_login[i]
        elif str(i) == 'Login_IP':
            host= servers_login[i]
        elif str(i) == 'User_Name':
            user= servers_login[i]
        elif str(i) == 'Key_Path':
            key_filename= servers_login[i]
        elif str(i) == 'Login_Port':
            port = servers_login[i]
        else: print ("load source servers info, failed")
    print ("Import the source servers information, Finished")
    print ("start the multi thread migration service...\n")
    conn = fabric.Connection(host = host, user= user, port=port, connect_kwargs={"key_filename": key_filename, "password":passw})
    conn.run('mkdir -p /tmp/temp_CE')

    conn.put(local_script_path+'/aws_model', '/tmp/temp_CE/aws_model')
    conn.put(local_script_path+'/aws-instances.csv', '/tmp/temp_CE/aws-instances.csv')
    conn.put(local_script_path+'/vlookup.sh', '/tmp/temp_CE/vlookup.sh')
    conn.put(local_script_path+'/get-source-instance-type-2.py', '/tmp/temp_CE/get-source-instance-type.py')
    conn.put(local_script_path+'/get-CPU-MEM.sh', '/tmp/temp_CE/get-CPU-MEM.sh')
    conn.put(local_script_path+'/deletion_duplication.py', '/tmp/temp_CE/deletion_duplication.py')
    conn.put(local_script_path+'/CloudEndure.py', '/tmp/temp_CE/CloudEndure.py')
    conn.put(local_script_path+'/Cloudendure_Account_Info.csv', '/tmp/temp_CE/Cloudendure_Account_Info.csv')
    conn.put(local_script_path+'/CE_Account.py', '/tmp/temp_CE/CE_Account.py')
    #conn.get('/tmp/temp_CE/get-login-info.py', local_script_path+'/get_login_info.py')

    conn.run("sudo python /tmp/temp_CE/get-source-instance-type.py $(. /tmp/temp_CE/get-CPU-MEM.sh)")
    conn.run("sudo python /tmp/temp_CE/deletion_duplication.py")
    conn.run("sudo sh /tmp/temp_CE/vlookup.sh /tmp/temp_CE/aws_model /tmp/temp_CE/b /tmp/temp_CE/c")
    conn.run("cat /tmp/temp_CE/c|sed -n 1p |cut -d \"'\" -f 8-8 > /tmp/temp_CE/d")
    conn.run("sudo python /tmp/temp_CE/CloudEndure.py $(sudo python /tmp/temp_CE/CE_Account.py)")
    #conn.run("sudo python /tmp/temp_CE/CloudEndure.py -u CE_User_Name -p CE_Password  -n ${HOSTNAME} -j CE_Project_Name")

    conn.close()
with open(local_script_path+"/Source_Servers_Info.csv",'r') as f:
    reader = csv.reader(f)
    fieldnames = next(reader)
    csv_reader = csv.DictReader(f,fieldnames=fieldnames)
    j=0
    for row in csv_reader:
        j=j+1
    print ("\nReady for migration %d Servers from your source environment totally... \n" %j)
    f.close()

source_servers = []
with open(local_script_path+"/Source_Servers_Info.csv",'r') as f:
    reader = csv.reader(f)
    fieldnames = next(reader)
    csv_reader = csv.DictReader(f,fieldnames=fieldnames)
    for row in csv_reader:
        server = threading.Thread(target=migration, args=(row,))
        source_servers.append(server)
    f.close()
for server in source_servers:
    server.start()
for server in source_servers:
    server.join()

