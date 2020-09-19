#! /usr/bin/env python
from collections import defaultdict
import os
import sys
import math
import kmeans
import numpy
import numpy as np
class interval(object):
    def __init__(self):
        self.numMshrs=128.0
        self.avg_stall_cycles=175
        self.exp_reqs=0
        self.read_list=[] #READ MISS in representative warp
        self.DRAM_READ_LIST=[]
        self.DRAM_WRITE_LIST=[]
        self.NoC_read_list=[]
        self.NoC_write_list=[]
        self.queuing_delay_noc=[]
        self.region_instructions={}
        self.warp_pc_list={}
        self.warp_index=0
        self.queuing_delay_mshr=[]
        self.queuing_delay_mshr_base=[]
        self.queuing_delay_dram=[]
        self.nonoverlap_insts=0
        self.accum_inst=0
        self.accum_stall=0
        self.warp_numbers=44
        self.dram_bandwidth=0
        self.noc_bandwidth=1050.0
        self.queuing_delay_mshr_optimal=[]
        self.queuing_delay_mshr_optimal_new=[]
        self.activeCores=28
        self.freq_core=1.4
        self.max_issue=1.0
        self.issue_prob=0
        self.X=[]
        self.MPL=0
        self.L2_miss_rate=0.0
        self.Clusters=2
        self.total_instruction_counts=0
        self.ipc_list=[]
        self.instruction_counts_list=[]
    def reset_DRAM(self,DRAM_size):
        self.dram_bandwidth=DRAM_size
        self.queuing_delay_mshr_optimal=[]
        self.queuing_delay_mshr_optimal_new=[]
        self.queuing_delay_dram=[]
        self.queuing_delay_noc=[]
        self.queuing_delay_mshr_base=[]
        self.queuing_delay_mshr=[]
    def calculate_avg_stall_cycles(self):
        i=0
        total_access=0
        miss=0
        L2_total=open('./output_L2','r')
        for line in L2_total:
            i+=1
            if(i==1):
                total_access=int(line.split(':')[-1])
                print(total_access)
            if((i==3)or(i==5)):
                miss+=int(line.split(':')[-1])
        miss_rate=float(miss)/float(total_access)
        self.L2_miss_rate=miss_rate
        self.avg_stall_cycles=120*(1-miss_rate)+220*miss_rate
        #self.avg_stall_cycles=390
        print(self.avg_stall_cycles)
    def multi_threading(self):
        i=0
        while(i<len(self.region_instructions[self.warp_index])-1):
            self.accum_inst+=self.region_instructions[self.warp_index][i]
            self.accum_stall+=self.region_instructions[self.warp_index][i+1]
            i+=2
        print("accum")
        print(self.accum_inst)
        print(self.accum_stall)
        self.issue_prob=float(self.accum_inst)/(float(self.accum_inst)/self.max_issue+float(self.accum_stall))
           
    
    def RR_regioninsts(self):
        i=0
        while(i<len(self.region_instructions[self.warp_index])-1):
            current_inst=self.region_instructions[self.warp_index][i]
            self.nonoverlap_insts+=(self.warp_numbers-1)*(current_inst-1)
            if (self.region_instructions[self.warp_index][i+1]<(self.warp_numbers-1)/self.max_issue):
                self.nonoverlap_insts+=(self.warp_numbers-1)/self.max_issue-self.region_instructions[self.warp_index][i+1]
            i+=2
        #issue_ration=float(self.accum_inst)/(float(self.accum_inst)/self.max_issue+float(self.accum_stall))*self.warp_numbers
        #issue_ration=float(self.accum_inst)/float(self.accum_inst)/self.max_issue+float(self.accum_stall)
        #if (self.issue_probissue_ration>self.max_issue):
        #    issue_ration=self.max_issue
        self.nonoverlap_insts=self.nonoverlap_insts*self.issue_prob
        return self.nonoverlap_insts
    
    def TotalRegionCycles_GTO(self):                
        total_cycles = 0
        remain_cycles = 0
        nonoverlapped_insts = 0
        i=0
        self.avg_inst=float(self.accum_inst)/(float(len(self.region_instructions[self.warp_index]))/2.0)       
        while(i<len(self.region_instructions[self.warp_index])-1):
            print('interval_info')
            print(self.region_instructions[self.warp_index][i])
            print(self.region_instructions[self.warp_index][i+1])
        #for region in self.regions[benchName][self.warpIdx]:                                    
            issue_prob_in_stall = min(1.0, self.issue_prob * self.region_instructions[self.warp_index][i+1])  
            if(self.region_instructions[self.warp_index][i+1]==0):
                issue_prob_in_stall=1.0
            #issue_prob_in_stall=min(1.0, issue_prob * stall_cycles)
            #issue_insts_in_stall = issue_prob_in_stall * (self.warp_numbers-1)*self.avg_inst
            issue_insts_in_stall=issue_prob_in_stall*(self.warp_numbers-1)*self.avg_inst
            if (issue_insts_in_stall - self.max_issue*self.region_instructions[self.warp_index][i+1] > 0):
                self.nonoverlap_insts += (issue_insts_in_stall - self.region_instructions[self.warp_index][i+1]*self.max_issue)
                print(self.nonoverlap_insts)
            i=i+2
        print(self.nonoverlap_insts)
           # total_cycles += (region["Latency"] + region["Size"])            
                        
        #total_cycles += nonoverlapped_insts        
        # print "GTO", total_insts, total_cycles, nonoverlapped_insts
        # if self.activeWarps[benchName] == 30:
        #     print "GTO", total_insts, nonoverlapped_insts, self.activeWarps[benchName]
        
       # if delay == 1:
       #     return total_cycles + self.queuing_delay
       # else:
       #     return total_cycles

#def multi_RR(nonoverlap_insts,warp_numbers):
    def IPC_full(self):
        print("naive_ipc")
        ipc=float(self.accum_inst)/(float(self.accum_inst)/self.max_issue+float(self.accum_stall))*self.warp_numbers
        if(ipc>self.max_issue):
            ipc=self.max_issue
        print(ipc)
        print('Multithreading_IPC')
        print(self.accum_inst)
        print(self.accum_stall)
        print(self.nonoverlap_insts)
        multi_ipc=float(self.accum_inst)/(float(self.accum_inst)/self.max_issue+float(self.accum_stall)+float(self.nonoverlap_insts)/self.max_issue)*self.warp_numbers
        if(multi_ipc>self.max_issue):
            ipc=self.max_issue
        print(multi_ipc)
        print("With MSHR modeling")
        MSHR_delay_total=0
        optimal_MSHR_delay_total=0
        GPUMech_MSHR_total=0
        for i in self.queuing_delay_mshr_base:
            GPUMech_MSHR_total+=i
        for i in self.queuing_delay_mshr:
            MSHR_delay_total+=i
        for i in self.queuing_delay_mshr_optimal:
            optimal_MSHR_delay_total+=i
        optimal_MSHR_delay_total_new=0
        for i in self.queuing_delay_mshr_optimal_new:
            optimal_MSHR_delay_total_new+=i
        DRAM_delay_total=0
        for j in self.queuing_delay_dram:
            DRAM_delay_total+=j
        GPUMech_cycles=float(self.accum_inst)/self.max_issue+float(self.accum_stall)+float(self.nonoverlap_insts)/self.max_issue+float(GPUMech_MSHR_total)+float(DRAM_delay_total)
        GPUMech_ipc=float(self.accum_inst)*self.warp_numbers/float(GPUMech_cycles)
        NoC_delay_total=0
        for k in self.queuing_delay_noc:
            NoC_delay_total+=k
        print(NoC_delay_total)
        Our_model_cycles=float(self.accum_inst)/self.max_issue+float(self.accum_stall)+float(self.nonoverlap_insts)/self.max_issue+float(optimal_MSHR_delay_total)+float(NoC_delay_total)
        Our_model_ipc=float(self.accum_inst)*self.warp_numbers/float(Our_model_cycles)
        print(self.total_instruction_counts)
       # result=open('result_delay_model+optimal_MSHR_'+str(self.noc_bandwidth),'a')
       # result.write(str(Our_model_ipc)+','+str(self.total_instruction_counts)+'\n')
        MPL_result=open('MPL','a')
        MPL_result.write(str(self.MPL)+'\n')
        delay_result=open('GPUMech+_'+str(self.dram_bandwidth),'a')
        cycle_delay_model=float(self.accum_inst)/self.max_issue+float(self.accum_stall)+float(self.nonoverlap_insts)/self.max_issue+float(MSHR_delay_total)+float(NoC_delay_total)
        ipc_delay_model=float(self.accum_inst)*self.warp_numbers/float(cycle_delay_model)
        delay_result.write(str(ipc_delay_model)+','+str(self.total_instruction_counts)+'\n')
        new_MSHR_result=open('MDM-MSHR_'+str(self.dram_bandwidth),'a')
        cycle_ceiling_MSHR=float(self.accum_inst)/self.max_issue+float(self.accum_stall)+float(self.nonoverlap_insts)/self.max_issue+float(optimal_MSHR_delay_total_new)+float(NoC_delay_total)
        ipc_ceiling_MSHR=float(self.accum_inst)*self.warp_numbers/float(cycle_ceiling_MSHR)
        new_MSHR_result.write(str(ipc_ceiling_MSHR)+','+str(self.total_instruction_counts)+'\n')
    def kmeans_operation(self):
        KmeansInstance=kmeans.Kmeans()
        self.rep_warp,self.weights=KmeansInstance.RunKmeans(self.X,self.Clusters)
        self.warp_index=0
        weight=0
        for i in range(0,len(self.rep_warp)):
            if(self.weights[i]>weight):
                weight=self.weights[i]
                self.warp_index=self.rep_warp[i]
        print(self.warp_index)
        #self.warp_index=100
    def generate_feature_vector(self):
    	ipc_list=[]
    	instruction_counts=[]
    	interval_profile=open('./warp_perf.txt','r')
    	for line in interval_profile:
        	ipc_list.append(float(line.split(',')[0]))
        	instruction_counts.append(int(line.split(',')[1]))
    	ipc_avg=np.mean(ipc_list)
    	print('MIN_IPC')
    	print(min(ipc_list))
    	print('MAX_IPC')
    	print(max(ipc_list))
    	print(ipc_avg)
    	instruction_counts_avg=np.mean(instruction_counts)
    	print(instruction_counts_avg)
    	for i in range(0,len(ipc_list)):
        	a=[float(ipc_list[i])/float(ipc_avg),float(instruction_counts[i])/float(instruction_counts_avg)]
        	self.X.append(a)
     	

    

    def Get_DRAM_info(self):
           L2_info=open('./output_L2_access.txt','r')
           instruction_index=0
           print('DRAM info')
           for i in range(0,len(self.region_instructions[self.warp_index])/2):
                self.DRAM_READ_LIST.append(0)
                self.DRAM_WRITE_LIST.append(0)
           for line in L2_info:
                warp_id=int(line.split(',')[0])
                if(warp_id==self.warp_index):
                    pc=int(line.split(',')[1])
                    if (int(line.split(',')[-1])==0): #L2_miss
                       # print(pc)
                        while(instruction_index<len(self.warp_pc_list[warp_id])):
                            if(pc!=self.warp_pc_list[warp_id][instruction_index]):
                                instruction_index+=1
                            else:
                                break
                        temp=0
                        accum=0
                        while(accum<instruction_index):
                            accum+=self.region_instructions[warp_id][temp]
                            temp+=2
                        index=(temp-2)/2
                        if(line.split(',')[2]=='R'):
                            self.DRAM_READ_LIST[index]+=1
                        else:
                            self.DRAM_WRITE_LIST[index]+=1
           #print(self.DRAM_READ_LIST)
           #print(self.DRAM_WRITE_LIST)
    

    def Get_NoC_info(self):
           i=(self.warp_index/self.warp_numbers)%self.activeCores
           L1_info=open('./output_'+str(i)+'_L1_hit.txt','r')
           instruction_index=0
           print('NoC info')
           for i in range(0,len(self.region_instructions[self.warp_index])/2):
                self.NoC_read_list.append(0)
                self.NoC_write_list.append(0)
           for line in L1_info:
                warp_id=int(line.split(',')[0])
                if(warp_id==self.warp_index):
                    pc=int(line.split(',')[1])
                    if(int(line.split(',')[-1])==0):
                        while(instruction_index<len(self.warp_pc_list[warp_id])):
                            if(pc!=self.warp_pc_list[warp_id][instruction_index]):
                                instruction_index+=1
                            else:
                                break
                        temp=0
                        accum=0
                        while(accum<instruction_index):
                            accum+=self.region_instructions[warp_id][temp]
                            temp+=2
                        index=(temp-2)/2
                        if((line.split(',')[2]=='R')):
                            self.NoC_read_list[index]+=1
                        else:
                            self.NoC_write_list[index]+=1
           print(self.NoC_read_list)
           print(self.NoC_write_list)
    def calculate_MPL(self):
        Miss_numbers=[]
        for i in self.NoC_read_list:
            if(i>1):
                Miss_numbers.append(i)
        if(len(Miss_numbers)>0):
            self.MPL=np.mean(Miss_numbers)
        else:
            self.MPL=0
    def warp_vector(self):
        for i in self.region_instructions:
            instruction_numbers=0
            total_cycles=0
            for j in range(0,len(self.region_instructions[i])/2):
                instruction_numbers+=self.region_instructions[i][2*j]
                total_cycles+=float(self.region_instructions[i][2*j])/self.max_issue+float(self.region_instructions[i][2*j+1])
            ipc=float(instruction_numbers)/float(total_cycles)
            self.ipc_list.append(ipc)
            self.instruction_counts_list.append(instruction_numbers)
        avg_ipc=np.mean(self.ipc_list)
        avg_instruction_counts=np.mean(self.instruction_counts_list)
        self.total_instruction_counts=np.sum(self.instruction_counts_list)
        for i in range(0,len(self.ipc_list)):
            a=[float(self.ipc_list[i])/float(avg_ipc),float(self.instruction_counts_list[i])/float(avg_instruction_counts)]
            self.X.append(a)
        print(len(self.X))
    
    
    
    
    def contention_DRAM_modeling(self):
        
        for i in range(0,len(self.region_instructions[self.warp_index])/2):
            if (self.DRAM_READ_LIST[i] + self.DRAM_WRITE_LIST[i]) >= 1.0:
                # self.dram_bandwidth = 192.0
                waiting_time = 0.0                

                # self.exp_reqs = (regionInfo["DRAMReads"] + regionInfo["DRAMWrites"]) * self.activeWarps[benchName]                
                
                all_reqs = (min(self.DRAM_READ_LIST[i]*self.warp_numbers,self.numMshrs) +\
                                self.DRAM_WRITE_LIST[i] * self.warp_numbers )* self.activeCores

                service_time = 128.0 / self.dram_bandwidth*self.freq_core

               # service_time = 128.0/self.dram_bandwidth

                service_time_sum = all_reqs * service_time

                service_time_sum2 = all_reqs * math.pow(128.0 / self.dram_bandwidth, 2)

                if self.avg_stall_cycles == 0:
                    self.avg_stall_cycles = 400                

                #utilization = float(service_time_sum) / self.avg_stall_cycles
                utilization = float(service_time_sum) /float(self.region_instructions[self.warp_index][2*i]+self.region_instructions[self.warp_index][2*i+1])
                # print utilization, service_time_sum, self.avg_stall_cycles
                if utilization > 1.0:
                    utilization = 0.99
                    # service_time_Es2 = service_time_sum2 / all_reqs;
                    # arrival_rate = all_reqs / self.avg_stall_cycles
                    # delay_dram = arrival_rate * service_time_Es2 / (2 * (1.0 - utilization));
                    delay_dram = service_time * all_reqs / 2.0                    
                else:
                    if all_reqs > 0:
                        service_time_Es2 = service_time_sum2 / all_reqs;
                    else:
                        service_time_Es2 = 0
                    arrival_rate = all_reqs/float(self.region_instructions[self.warp_index][2*i]/self.max_issue+self.region_instructions[self.warp_index][2*i+1])
                   # arrival_rate = all_reqs / self.avg_stall_cycles
                    delay_dram = arrival_rate * service_time_Es2 / (2 * (1.0 - utilization));
                
                # print delay_dram, all_reqs
                                                        
                self.queuing_delay_dram.append(delay_dram)                
            else:
                self.queuing_delay_dram.append(0)
    
    '''
    def contention_DRAM_modeling(self):
        
        for i in range(0,len(self.region_instructions[self.warp_index])/2):
            self.queuing_delay_dram.append(0)
            accume_write=0
            if(self.NoC_read_list[i])<1: #non_ld_interval
                accume_write+=self.DRAM_WRITE_LIST[i]
            else:
                batch=math.ceil(self.NoC_read_list[i]*self.warp_numbers/self.numMshrs)
                if (self.DRAM_READ_LIST[i] + accume_write) >= 1.0:

                # self.exp_reqs = (regionInfo["DRAMReads"] + regionInfo["DRAMWrites"]) * self.activeWarps[benchName]                
                
                    all_reqs = (self.DRAM_READ_LIST[i]*self.warp_numbers +accume_write* self.warp_numbers )* self.activeCores/batch

                    service_time = 128.0 / self.dram_bandwidth*self.freq_core
                    #service_time=

               # service_time = 128.0/self.dram_bandwidth

                    service_time_sum = all_reqs * service_time

                    service_time_sum2 = all_reqs * math.pow(128.0 / self.dram_bandwidth, 2)

                    if self.avg_stall_cycles == 0:
                        self.avg_stall_cycles = 400                

                    utilization = float(service_time_sum) / self.avg_stall_cycles
                #     utilization = 1.0
                #utilization = float(service_time_sum) /float(self.region_instructions[self.warp_index][2*i]+self.region_instructions[self.warp_index][2*i+1])
                #print('utiliation')
                #print(utilization)
                # print utilization, service_time_sum, self.avg_stall_cycles
                    if utilization > 1.0:
                        utilization = 0.99
                    # service_time_Es2 = service_time_sum2 / all_reqs;
                    # arrival_rate = all_reqs / self.avg_stall_cycles
                    # delay_dram = arrival_rate * service_time_Es2 / (2 * (1.0 - utilization));
                        delay_dram = service_time * all_reqs                     
                    else:
                        if all_reqs > 0:
                            service_time_Es2 = service_time_sum2 / all_reqs;
                        else:
                            service_time_Es2 = 0
                        arrival_rate = all_reqs/float(self.region_instructions[self.warp_index][2*i]/self.max_issue+self.region_instructions[self.warp_index][2*i+1])
                   # arrival_rate = all_reqs / self.avg_stall_cycles
                        delay_dram = arrival_rate * service_time_Es2 / (2 * (1.0 - utilization));
                
                # print delay_dram, all_reqs
                                                        
                    print(delay_dram)
                    self.queuing_delay_dram[i]=delay_dram            
    '''
    def contention_NoC_modeling(self):
         for i in range(0,len(self.region_instructions[self.warp_index])/2):
            if(self.NoC_read_list[i]+self.NoC_write_list[i])>=1.0:
            #if (self.read_list[i] + self.NoC_write_list[i]) >= 1.0:
                # self.dram_bandwidth = 192.0
                waiting_time = 0.0                

                # self.exp_reqs = (regionInfo["DRAMReads"] + regionInfo["DRAMWrites"]) * self.activeWarps[benchName]                
                
                read_reqs = min(self.NoC_read_list[i]*self.warp_numbers,self.numMshrs)*self.activeCores 
                #if self.NoC_read_list[i]*self.warp_numbers> self.numMshrs:
                #    write_reqs=float(self.NoC_write_list[i]*self.warp_numbers)/float(math.ceil(self.NoC_read_list[i]*self.warp_numbers/self.numMshrs))* self.activeCores
                #else:
                write_reqs=float(self.NoC_write_list[i]*self.warp_numbers)*self.activeCores
                all_reqs=read_reqs+write_reqs

                service_time_noc = 128.0 / self.noc_bandwidth*self.freq_core
                
                service_time_dram = 128.0 /self.dram_bandwidth *self.freq_core

                service_time=service_time_noc+self.L2_miss_rate*service_time_dram

               # service_time = 128.0/self.dram_bandwidth



                #utilization = float(service_time_sum) /float(self.region_instructions[self.warp_index][2*i]+self.region_instructions[self.warp_index][2*i+1])
                # print utilization, service_time_sum, self.avg_stall_cycles
                    # service_time_Es2 = service_time_sum2 / all_reqs;
                    # arrival_rate = all_reqs / self.avg_stall_cycles
                    # delay_dram = arrival_rate * service_time_Es2 / (2 * (1.0 - utilization));
                #if(self.NoC_read_list[i]*self.warp_numbers>self.numMshrs):
                #if(self.NoC_read_list[i]>0):
                #    delay_noc = service_time *(self.numMshrs*self.activeCores+float(write_reqs)) 
                #else:
                delay_noc= service_time *all_reqs/2.0
                   # arrival_rate = all_reqs/float(self.region_instructions[self.warp_index][2*i]+self.region_instructions[self.warp_index][2*i+1])
                  #  print(delay_noc)
                # print delay_dram, all_reqs
                #print(delay_noc)                                        
                self.queuing_delay_noc.append(delay_noc)
            else:
                self.queuing_delay_noc.append(0)
    def dram_queue_length(self):
         total_latency=0
         total_mem=0
         for i in range(0,len(self.region_instructions[self.warp_index])/2):
             if(self.DRAM_READ_LIST[i]+self.DRAM_WRITE_LIST[i])>=1.0:
                total_request=(min(self.DRAM_READ_LIST[i]*self.warp_numbers,self.numMshrs)+self.DRAM_WRITE_LIST[i])*self.activeCores
                request_per_bank=total_request/32.0
                latency=request_per_bank/2*100*32.0
                total_latency+=latency
                total_mem+=total_request
         print(total_latency)
         print(total_mem)
         avg_delay=total_latency/total_mem
         print(avg_delay)


    
    def contention_modeling_MSHR(self):                
        self.exp_reqs = 0
      #  self.avg_stall_cycles=367
      #  N = self.activeWarps[benchName]
      #  avg_req = 0.0        
      #  prob = 0.0
      #  utilization = 0.0
      #  region_read=[]
        #self.queuing_delay_mshr = []
        #self.queuing_delay_dram = []
        #for i in range(0,len(self.read_list)):
        for i in range(0,len(self.region_instructions[self.warp_index])/2):
            if(self.NoC_read_list[i]>=1):
                delay_mshr = 0
                delay_mshr_base=0
                #avg_stall_cycles=1050
                avg_stall_cycles=self.avg_stall_cycles+self.queuing_delay_noc[i]
                #print("avg_stall_cycles")
                #print(avg_stall_cycles)
                #if(self.DRAM_READ_LIST[i]>=1):
                #    avg_stall_cycles=self.avg_stall_cycles+self.queuing_delay_dram[i]
                #print(self.queuing_delay_dram[i])
                #print(self.queuing_delay_noc[i])
               # avg_stall_cycles=400
                #avg_stall_cycles=self.avg_stall_cycles
                # self.exp_reqs = regionInfo["Reads"] * self.activeWarps[benchName] / float(regionInfo["Read_Insts"])
                self.exp_reqs =self.NoC_read_list[i] * self.warp_numbers
                if self.exp_reqs > self.numMshrs:                
                    for j in range(1, int(self.exp_reqs + 1)):
                        if self.exp_reqs > 0:                            
                            delay_mshr += float(avg_stall_cycles * (math.ceil(float(j) / self.numMshrs)) * 1.0) / float(self.exp_reqs)
                            delay_mshr_base+=float(self.avg_stall_cycles*(math.ceil(float(j)/self.numMshrs))*1.0)/float(self.exp_reqs)
                        else:
                            delay_mshr = 0                    
                            delay_mshr_base=0                       
                    # print "mshrs", self.numMshrs
                    # delay_mshr = (delay_mshr - self.avg_stall_cycles) * regionInfo["Read_Insts"]
                    delay_mshr -=avg_stall_cycles
                    delay_mshr_base-=self.avg_stall_cycles
                   # a=len(self.queuing_delay_mshr)
                   # for i in range(0, len(self.queuing_delay_mshr)):
                
                   #     if(self.queuing_delay_mshr[i]>:
                    #        delay_mshr+=self.queuing_delay_mshr[i]-(a-i-2)*self.avg_stall_cycles
                # print self.exp_reqs, self.numMshrs, delay_mshr
                self.queuing_delay_mshr.append(delay_mshr)
                self.queuing_delay_mshr_base.append(delay_mshr_base)
                    #        delay_mshr+=self.queuing_delay_mshr[i]-(a-i-2)*self.avg_stall_cycles
                # print self.exp_reqs, self.numMshrs, delay_mshr
      
    
    def contention_modeling_MSHR_optimal(self):                
        self.exp_reqs = 0
      #  self.avg_stall_cycles=367
      #  N = self.activeWarps[benchName]
      #  avg_req = 0.0        
      #  prob = 0.0
      #  utilization = 0.0
      #  region_read=[]
        #self.queuing_delay_mshr = []
        #self.queuing_delay_dram = []
        #for i in range(0,len(self.read_list)):
        for i in range(0,len(self.region_instructions[self.warp_index])/2):
            if(self.NoC_read_list[i]>=1):
                delay_mshr_optimal = 0
                delay_mshr_new_optimal=0
                avg_stall_cycles=self.avg_stall_cycles+self.queuing_delay_noc[i]
                self.exp_reqs =self.NoC_read_list[i] * self.warp_numbers
                if self.exp_reqs > self.numMshrs:                
                    delay_mshr_optimal=float(avg_stall_cycles)*float(self.exp_reqs)/float(self.numMshrs)
                    delay_mshr_new_optimal=float(avg_stall_cycles)*math.ceil(float(self.exp_reqs)/self.numMshrs)
                    delay_mshr_optimal -=float(avg_stall_cycles)
                    delay_mshr_new_optimal-=float(avg_stall_cycles)
                self.queuing_delay_mshr_optimal.append(delay_mshr_optimal)
                self.queuing_delay_mshr_optimal_new.append(delay_mshr_new_optimal)
                   # a=len(self.queuing_delay_mshr)

    def warp_interval_profile(self,kernel_id):
           warp_interval={}
           warp_max_issue_cycle={}
           pc_list=[]
           latency_list={}
           interval_inst={}
           dependence_trace=open('../interval_info_'+str(kernel_id)+'.txt','r')
           pc_latency=open('./pc_latency_info','r')
           for line in pc_latency:
               pc=int(line.split(',')[0])
               pc_list.append(int(line.split(',')[0]))
               latency_list[pc]=float(line.split(',')[1])
      # output_trace=open('single_warp_info.txt','w')
           for line in dependence_trace:
                warp_id=int(line.split(',')[0])
                if ((warp_id==0)and(self.warp_pc_list.get(1000,0)!=0)):
                    break
                if(warp_interval.get(warp_id,0)==0):
                     warp_interval[warp_id]={}
                     self.region_instructions[warp_id]=[]
                     interval_inst[warp_id]=0
                     warp_max_issue_cycle[warp_id]=0
                     self.warp_pc_list[warp_id]=[]
                pc=int(line.split(',')[1])
                self.warp_pc_list[warp_id].append(pc)
                if(warp_interval[warp_id].get(pc,0)==0):
                     warp_interval[warp_id][pc]=[]
                latency=int(line.split(',')[-1])
                if(pc in pc_list):
                    latency=latency_list[pc]
                issue_cycle=warp_max_issue_cycle[warp_id]+1
                dependence_pc_list=[]
                for i in range(3,len(line.split(','))-1):
                    dependence_pc_list.append(int(line.split(',')[i]))
                for j in range(0,len(dependence_pc_list)):
                    dep_pc=dependence_pc_list[j]
                    if(warp_interval[warp_id].get(dep_pc,0)!=0):
                        if(len(warp_interval[warp_id][dep_pc])>0):
                            done_cycle=warp_interval[warp_id][dep_pc][-1]
                            if((done_cycle+1)>(issue_cycle)):
                                 issue_cycle=done_cycle+1
                if((issue_cycle-warp_max_issue_cycle[warp_id])<10):
                    interval_inst[warp_id]+=1
                else:
                    stall_cycles=issue_cycle-warp_max_issue_cycle[warp_id]
                    self.region_instructions[warp_id].append(interval_inst[warp_id])
                    self.region_instructions[warp_id].append(stall_cycles)
                    interval_inst[warp_id]=1
                warp_interval[warp_id][pc].append(issue_cycle)
                warp_interval[warp_id][pc].append(issue_cycle+latency)
         # output_trace.write(str(warp_id)+','+str(pc)+','+str(issue_cycle)+',')
          # output_trace.write(str(issue_cycle+latency))
          # output_trace.write('\n')
                warp_max_issue_cycle[warp_id]=issue_cycle
           for warp in self.region_instructions:
                self.region_instructions[warp].append(interval_inst[warp])
                self.region_instructions[warp].append(0)
       # get the MSHR access numbers for each interval
           
          

    def MSHR_info(self):
           print(self.warp_index)
           i=(self.warp_index/64)%self.activeCores
           print(i)          
           L1_hit_info=open('./read_out_'+str(i)+'_L1_hit.txt','r')
           instruction_index=0
           line_number=0
           pre_warp_id=-1
           miss=0
           #for i in range(0,len(self.region_instructions[self.warp_index])/2):
           #     self.read_list.append(0)
           for line in L1_hit_info:
                warp_id=int(line.split(',')[0])
                if(warp_id==self.warp_index):
                    pc=int(line.split(',')[1])
                    if ((int(line.split(',')[-1])==0)): #L1 miss
                        miss=miss+1
                        if(pre_warp_id==self.warp_index):
                            self.read_list[len(self.read_list)-1]+=1
                        else:
                            self.read_list.append(int(1))
                if((warp_id!=self.warp_index)or(int(line.split(',')[-1])==0)):
                    pre_warp_id=warp_id
           print(self.read_list)
           #print(miss)
           print(np.mean(self.read_list))                                     
                                      
    



def main(kernel_id):
    intervalInstance=interval()
    intervalInstance.calculate_avg_stall_cycles()
    intervalInstance.warp_interval_profile(kernel_id)
    intervalInstance.warp_vector()
   # intervalInstance.generate_feature_vector()
    intervalInstance.kmeans_operation()
    intervalInstance.multi_threading()
    intervalInstance.TotalRegionCycles_GTO()
   # intervalInstance.MSHR_info()
   # intervalInstance.contention_modeling_MSHR()
    intervalInstance.Get_NoC_info()
    intervalInstance.calculate_MPL()
    intervalInstance.Get_DRAM_info()
   # intervalInstance.contention_DRAM_modeling()
    #intervalInstance.Get_NoC_info()
    DRAM_config=[480.0,720.0,980.0]
    for i in range(0,3):
        DRAM_size=DRAM_config[i]
        intervalInstance.reset_DRAM(DRAM_size)
        intervalInstance.contention_NoC_modeling()
        intervalInstance.contention_DRAM_modeling()
        intervalInstance.contention_modeling_MSHR()
        intervalInstance.contention_modeling_MSHR_optimal()
   # intervalInstance.dram_queue_length()
   #intervalInstance.Get_NoC_info()
        intervalInstance.IPC_full()
   
   
   # RR_regioninsts(region_instructions,512,24)
     # warp_feature=open('warp_vector.txt','w')
      # for warp in warp_interval:
      #     instruction_count=0
      #    for pc in warp_interval[warp]:
      #          instruction_count+=len(warp_interval[warp][pc])/2
      #     IPC=float(instruction_count)/float(warp_max_issue_cycle[warp])
      #     warp_feature.write(str(IPC)+','+str(instruction_count)+'\n')
      # interval_profile=open('warp_interval_profile.txt','w')
      # for warp in region_instructions:
      #     for j in range(0,len(region_instructions[warp])):
      #         if warp==0:
      #             print(region_instructions[warp])
              # interval_profile.write(str(warp)+','+str(region_instructions[warp][j])+','+str(region_instructions[warp][j+1])+'\n')
              # j+=2 

if __name__=='__main__':
   main(sys.argv[1])
      
