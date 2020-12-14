import csv
import sys
with open("/tmp/temp_CE/aws-instances.csv",'r') as f:
    reader = csv.reader(f)
    fieldnames = next(reader)
#    print(fieldnames)
    csv_reader = csv.DictReader(f,fieldnames=fieldnames)
    for row in csv_reader:
        d={}
        for k,v in row.items():
         d[k]=v
#        print(d)
#        print k,v
         a=sys.argv[1]
         if a == v:
             print row
             write_file_b=open('/tmp/temp_CE/bb',mode='a')
             write_file_b.write(str(row)+'\n')
             write_file_b.close()
    f.close()
