#!/usr/bin/env python 
import os
import sys
def main(kernel_numbers):
    noc_config=[177.0,320.0,480.0,720.0,980.0]
    for i in range(0,5):
        noc_bandwidth=noc_config[i]
        result=open('./GPUMech_'+str(noc_bandwidth),'r')
        accum_cycle=0
        accum_inst=0
        for line in result:
            ipc=float(line.split(',')[0])
            instruction_count=float(line.split(',')[1])
            cycle=instruction_count/ipc
            accum_cycle=accum_cycle+cycle
            accum_inst=accum_inst+instruction_count
        total_ipc=float(accum_inst)/float(accum_cycle)
        print('dram_bandwidth:'+str(noc_bandwidth))
        print('GPUMech_ipc')
        print(total_ipc)
        result=open('./GPUMech+_'+str(noc_bandwidth),'r')
        accum_cycle=0
        accum_inst=0
        for line in result:
            ipc=float(line.split(',')[0])
            instruction_count=float(line.split(',')[1])
            cycle=instruction_count/ipc
            accum_cycle=accum_cycle+cycle
            accum_inst=accum_inst+instruction_count
        total_ipc=float(accum_inst)/float(accum_cycle)
        print('dram_bandwidth:'+str(noc_bandwidth))
        print('GPUMech+_ipc')
        print(total_ipc)
        result=open('./MDM-Queue_'+str(noc_bandwidth),'r')
        accum_cycle=0
        accum_inst=0
        for line in result:
            ipc=float(line.split(',')[0])
            instruction_count=float(line.split(',')[1])
            cycle=instruction_count/ipc
            accum_cycle=accum_cycle+cycle
            accum_inst=accum_inst+instruction_count
        total_ipc=float(accum_inst)/float(accum_cycle)
        print('dram_bandwidth:'+str(noc_bandwidth)+'\n')
        print('MDM-Queue_')
        print(total_ipc)
        result=open('./MDM-MSHR_'+str(noc_bandwidth),'r')
        accum_cycle=0
        accum_inst=0
        for line in result:
            ipc=float(line.split(',')[0])
            instruction_count=float(line.split(',')[1])
            cycle=instruction_count/ipc
            accum_cycle=accum_cycle+cycle
            accum_inst=accum_inst+instruction_count
        total_ipc=float(accum_inst)/float(accum_cycle)
        print('dram_bandwidth:'+str(noc_bandwidth)+'\n')
        print('MDM_MSHR_:')
        print(total_ipc)
        result=open('./MDM_'+str(noc_bandwidth),'r')
        accum_cycle=0
        accum_inst=0
        for line in result:
            ipc=float(line.split(',')[0])
            instruction_count=float(line.split(',')[1])
            cycle=instruction_count/ipc
            accum_cycle=accum_cycle+cycle
            accum_inst=accum_inst+instruction_count
        total_ipc=float(accum_inst)/float(accum_cycle)
        print('MDM:')
        print(total_ipc)
if __name__== '__main__':
    main(sys.argv[1])
