#!/usr/bin/env python 
import os
import sys
def main(kernel_numbers):
    MSHR_config=[480.0,720.0,980.0]
    for i in range(0,3):
        MSHR_size=MSHR_config[i]
        result=open('./GPUMech_'+str(MSHR_size),'r')
        accum_cycle=0
        accum_inst=0
        for line in result:
            ipc=float(line.split(',')[0])
            instruction_count=float(line.split(',')[1])
            cycle=instruction_count/ipc
            accum_cycle=accum_cycle+cycle
            accum_inst=accum_inst+instruction_count
        total_ipc=float(accum_inst)/float(accum_cycle)
        print('MSHR_size:'+str(MSHR_size))
        print('GPUMech_ipc')
        print(total_ipc)
        #result=open('./MDM-MSHR_'+str(MSHR_size),'r')
        #accum_cycle=0
        #accum_inst=0
        #for line in result:
        #    ipc=float(line.split(',')[0])
        #    instruction_count=float(line.split(',')[1])
        #    cycle=instruction_count/ipc
        #    accum_cycle=accum_cycle+cycle
        #    accum_inst=accum_inst+instruction_count
        #total_ipc=float(accum_inst)/float(accum_cycle)
        #print('MSHR_size:'+str(MSHR_size)+'\n')
        #print('ipc_delay_model')
        #print(total_ipc)
        result=open('./MDM_'+str(MSHR_size),'r')
        accum_cycle=0
        accum_inst=0
        for line in result:
            ipc=float(line.split(',')[0])
            instruction_count=float(line.split(',')[1])
            cycle=instruction_count/ipc
            accum_cycle=accum_cycle+cycle
            accum_inst=accum_inst+instruction_count
        total_ipc=float(accum_inst)/float(accum_cycle)
        print('ipc_delay_model+optimal_MSHR')
        print(total_ipc)
if __name__== '__main__':
    main(sys.argv[1])
