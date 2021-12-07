from os import write
import sys
import random

def remove_repeat(folder, date, time):
    input_file = open('iplookup_entry/'+folder+'/'+date+'_'+time+'.txt', 'r', 1)
    content = input_file.readlines()
    dic = dict()

    output_file = open('iplookup_final/'+folder+'/'+date+'_'+time+'.txt', 'w')
    output_file.write("{:<20} {}".format("Prefix","Next Hop")+"\n")

    for c in content:
        line = list(c.split(' '))
        if dic.get(line[0],None) == None:
            next_hop = str(random.randint(0,255))+"."+str(random.randint(0,255))+"."+str(random.randint(0,255))+"."+str(random.randint(0,255))
            dic[line[0]] = next_hop
            output_file.write("{:<20} {}\n".format(line[0],next_hop))

    input_file.close()
    output_file.close()

folder = ['rrc05']#['rrc00', 'rrc01', 'rrc03', 'rrc04', 'rrc05']
date = ['20211123']#['20211122','20211123']
time = ['1600']#['0800', '1600']

for f in folder:
    for d in date:
        for t in time:
            print(f+" "+d+" "+t+" start.")
            remove_repeat(f,d,t)
    print(f+" is finish.")