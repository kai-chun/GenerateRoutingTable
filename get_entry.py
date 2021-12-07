from os import write
import sys

def write_entry(folder, date, time):
    input_file = open('iplookup_txt/'+folder+'/bview.'+date+'.'+time+'.txt', 'r', 1)
    content = input_file.readlines()

    output_file = open('iplookup_entry/'+folder+'/'+date+'_'+time+'.txt', 'w')

    for c in content:
        line = list(c.split('|'))
        if ":" in line[5]: continue
        output_file.write(line[5]+" "+line[8]+"\n")

    input_file.close()
    output_file.close()

folder = ['rrc05']#['rrc00', 'rrc01', 'rrc03', 'rrc04', 'rrc05']
date = ['20211122']#['20211123']
time = ['0000']#,'0800', '1600']

for f in folder:
    for d in date:
        for t in time:
            print(f+" "+d+" "+t+" start.")
            write_entry(f,d,t)
    print(f+" is finish.")

'''
entry_num = 50
input_file = open('test.txt', 'r', 1)
content = input_file.readlines()

output_file = open('entry_'+str(entry_num)+'.txt', 'w')

index = 0
for c in content:
    if c[0] == '*' and c[3] != ' ':
        output_file.write(c[3:35]+"\n")
        index += 1
    if index == entry_num:
        break

input_file.close()
output_file.close()

entry_num = 50
input_file = open('test.txt', 'r', 1)
content = input_file.readlines()

output_file = open('entry_'+str(entry_num)+'.txt', 'w')

index = 0
for c in content:
    if c[0] == '>':
        line = list(c.split(' '))
        #print(line[0][1:]+" "+line[1])
        output_file.write(line[0][1:]+" "+line[1]+"\n")
        index += 1
    if index == entry_num:
        break

input_file.close()
output_file.close()
'''