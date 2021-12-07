from os import write
import sys
import random
import re
import math

sort_routing_table = []
for i in range(32):
    sort_routing_table.append(dict())

def get_prefix_bin(rule, mask):
    raw = rule.split('.')
    mask_len = int(mask) / 8
    remain = int(mask) % 8

    ip = ""
    for i in range(mask_len):
        part_ip_bin = bin(int(raw[i]))[2:]
        part_ip_bin = '0'*(8-len(part_ip_bin)) + part_ip_bin
        ip += part_ip_bin
    
    if remain != 0:
        part_ip_bin = bin(int(raw[i+1]))[2:]
        #print("raw[i]",part_ip_bin)
        part_ip_bin = '0'*(8-len(part_ip_bin)) + part_ip_bin
        ip += part_ip_bin[:remain]

    return ip

def random_ip(rule_list, rule, mask):
    raw = rule.split('.')
    mask_len = int(mask) / 8
    remain = int(mask) % 8

    ip = ""
    for i in range(mask_len):
        ip += raw[i]+"."
        
    for i in range(mask_len,4):
        if remain != 0:
            part_ip_bin = bin(int(raw[i]))[2:]
            part_ip_bin = '0'*(8-len(part_ip_bin)) + part_ip_bin
            part_ip_bin = part_ip_bin[:remain]
            for j in range(remain,8):
                part_ip_bin += str(random.randint(0,1))
            part_ip = int(part_ip_bin,2)
            remain = 0
            ip += str(part_ip)
        else:
            ip += str(random.randint(0,255))
        if i != 3:
            ip += "."
    
    #print("ip " + ip)
    ip_bin = get_prefix_bin(ip, 32)
    next_hop = ""
    for j, mask_list in enumerate(sort_routing_table):
        ip_bin_part = ip_bin[:32-j]
        #print("mask_list",mask_list)
        #print(ip_bin_part)
        if mask_list.get(ip_bin_part, None) != None: 
            #print("get "+ip_bin_part)
            next_hop = mask_list[ip_bin_part]
            break
    return (ip, next_hop)

def generate_trace(folder, date, time):
    input_file = open('iplookup_final/'+folder+'/'+date+'_'+time+'.txt', 'r', 1)
    content = input_file.readlines()
    routing_table = dict()

    size = 10
    count_entry = 0

    # get all entry
    for c in content:
        if count_entry == 0: # ignore the first line
            count_entry += 1
            continue
        line = list(re.split('[ /]', c))
        mask = line[1]
        next_hop = line[-1][0:-1]
        if routing_table.get(line[0], None) == None:
            routing_table[line[0]] = []
        routing_table[line[0]].append((mask, next_hop))
        count_entry += 1

        # sort routing table
        if int(mask) == 0: continue
        entry = get_prefix_bin(line[0], mask)
        sort_routing_table[32-int(mask)][entry] = next_hop
        #if count_entry > 5: break
    #print(routing_table)
    #print('==========')
    #print(sort_routing_table)

    trace = []
    for i in range(size):
        for j in routing_table:
            for rule in routing_table[j]:
                if rule[0] == '0':
                    sample = ('0.0.0.0', rule[1])
                else:
                    sample = random_ip(routing_table[j], j, rule[0])
                trace.append(sample)
        #print("trace",trace)
    
    random.shuffle(trace)
    
    # write trace into file
    output_file = open('trace/'+folder+'/'+date+'_'+time+'.txt', 'w')
    output_file.write("{:<20} {}".format("IP Address","Next Hop")+"\n")

    for entry in trace:
        output_file.write("{:<20} {}\n".format(entry[0],entry[1]))

    input_file.close()
    output_file.close()


folder = ['rrc00']#['rrc00', 'rrc01', 'rrc03', 'rrc04', 'rrc05']
date = ['20211122']#['20211122','20211123']
time = ['0000']#['0800', '1600']

for f in folder:
    for d in date:
        for t in time:
            print(f+" "+d+" "+t+" start.")
            generate_trace(f,d,t)
    print(f+" is finish.")