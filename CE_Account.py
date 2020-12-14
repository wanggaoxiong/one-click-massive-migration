import csv
import socket
with open("/tmp/temp_CE/Cloudendure_Account_Info.csv",'r') as f:
    reader = csv.reader(f)
    fieldnames = next(reader)
    csv_reader = csv.DictReader(f,fieldnames=fieldnames)
    for row in csv_reader:
        for i in row.keys():
            if str(i) == 'CE_User_Name':
                CE_User_Name= row[i]
            elif str(i) == 'CE_Password':
                CE_Password= row[i]
            elif str(i) == 'CE_Project_Name':
                CE_Project_Name= row[i]
            else: print ("The Cloudendure account entered is incorrect")
    f.close()
host_name= socket.gethostname()
print ("-u %s -p %s -j %s -n %s" %(CE_User_Name,CE_Password,CE_Project_Name,host_name))
