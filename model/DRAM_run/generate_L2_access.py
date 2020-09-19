#! /usr/bin/env python
from collections import defaultdict
from sets import Set
import os
import sys
import time
def generate_L1_hit_info(SM_numbers,kernel_id):
    for i in range(0,SM_numbers):
        cmd='./243685 L1_cache SM_trace_'+str(i)+'.txt output_'+str(i)+' output_'+str(i)+'_L1_hit.txt read_out_'+str(i)+'_L1_hit.txt'
        os.system(cmd)

def generate_L2_hit_info(kernel_id):
    cmd='./243685 L2_cache L2_trace.txt output_L2 output_L2_access.txt'
    os.system(cmd)


def main(kernel_id):
    analyze_cmd='python ./analyze_memory.py '+str(kernel_id)
    os.system(analyze_cmd)
    SM_numbers=80
    os.system('mkdir kernel_'+str(kernel_id))
    start=time.time()
    generate_L1_hit_info(SM_numbers,kernel_id)
    generate_L2(SM_numbers)
    generate_L2_hit_info(kernel_id)
    generate_PC_miss_info(SM_numbers)
    end=time.time()
    print(end-start)
    cmd_1='rm SM_trace_*'
    os.system(cmd_1)
    cmd_2='L2_trace.txt'
    os.system(cmd_2)
    #for i in range(0,SM_numbers):
    #    cmd_3='rm output_'+str(i)+'_L1_hit.txt'
    #    os.system(cmd_3)


def generate_PC_miss_info(SM_numbers):
    total_access_pc={}
   # L1_miss_pc={}
    L2_miss_pc={}
    pc_read={}
    average_latency={}
    #for i in range(0,SM_numbers):
    #    memory_trace=open('output_'+str(i)+'_L1_hit.txt','r')
    #    warp_id=0
    #    for line in memory_trace:
    #       pc=int(line.split(',')[1])
    #        warp_id=int(line.split(',')[0])
    #        if (total_access_pc.get(pc,0)==0):
    #            total_access_pc[pc]=set()
    #           L1_miss_pc[pc]=set()
    #        total_access_pc[pc].add(warp_id)
    #        if (int(line.split(',')[-1])==0):
    #            L1_miss_pc[pc].add(warp_id)
    L2_trace=open('output_L2_access.txt')
    for line in L2_trace:
            pc=int(line.split(',')[1])
            warp_id=int(line.split(',')[0])
            if(total_access_pc.get(pc,0)==0):
                total_access_pc[pc]=set()
            total_access_pc[pc].add(warp_id)
            if(L2_miss_pc.get(pc,0)==0):
                L2_miss_pc[pc]=set()
            if(int(line.split(',')[-1])==0):
                L2_miss_pc[pc].add(warp_id)
    memory_pc_info=open('pc_miss_info','w')
    #memory_pc_info.write('L1_miss_info\n')
    pc_latency_info=open('pc_latency_info','w')
    for k in total_access_pc:
   #     memory_pc_info.write(str(k)+','+str(len(total_access_pc[k]))+','+str(len(L1_miss_pc[k]))+'\n')
   #     miss_rate=float(len(L1_miss_pc[k]))/float(len(total_access_pc[k]))
        if k in L2_miss_pc:
            L2_miss_rate=float(len(L2_miss_pc[k]))/float(len(total_access_pc[k]))
            latency=L2_miss_rate*420+(1-L2_miss_rate)*120
            print(latency)
            pc_latency_info.write(str(k)+','+str(latency)+'\n')
    memory_pc_info.write('L2_hit_info\n')
    for k in L2_miss_pc:
        memory_pc_info.write(str(k)+','+str(len(L2_miss_pc[k]))+'\n')
    
def generate_L2(SM_numbers):
    Total_miss_list=[]
    for i in range(0,SM_numbers):
        SM_miss_list=[]
        memory_trace=open('./output_'+str(i)+'_L1_hit.txt','r')
        for line in memory_trace:
            access_info=[]
            length=len(line.split(','))
            if(int(line.split(',')[-1])==0):
                for i in range(0,length-1):
                    access_info.append(line.split(',')[i])
                SM_miss_list.append(access_info)
        print(len(SM_miss_list))
        Total_miss_list.append(SM_miss_list) 
    print(len(Total_miss_list))
    j=0
    empty=[]
    for i in range(0,SM_numbers):
        empty.append(0)
    L2_access=[]
    sum=0
    while (sum!=SM_numbers):
        sum=0
        if(len(Total_miss_list[j])!=0):
            L2_access.append(Total_miss_list[j][0])
            Total_miss_list[j].pop(0)
        else:
           empty[j]=1
           for i in range(0,SM_numbers):
                sum=sum+empty[i]
        #Total_miss_list[j].pop(0)
        j=(j+1)%SM_numbers
     #   print(j)
    print(len(L2_access))
    generate_L2_access=open('L2_trace.txt','w')
    for i in range (0,len(L2_access)):
        for k in range(0,len(L2_access[i])-1):
            generate_L2_access.write(L2_access[i][k]+',')
       # generate_L2_access.write('\n')
        generate_L2_access.write(L2_access[i][len(L2_access[i])-1])
        generate_L2_access.write('\n')
      # print 'merge_size_1:%d' % size[0]
      # print 'merge_size_2:%d' % size[1]
      # print 'merge_size_3:%d' % size[2]
      # print 'merge_size_4:%d' % size[3]
      # print 'merge_size_5:%d' % size[4]
      # print 'merge_size_6:%d' % size[5]
      # print 'merge_size_7:%d' % size[6]
      # print 'merge_size_8:%d' % size[7]
       # time=int(line.split(',')[-1])
      # creation_time=int(line.split(',')[-1])
        #queue_time=time-creation_time
        #amount_queue_time+=queue_time
if __name__=='__main__':
   
   main(sys.argv[1])
      
