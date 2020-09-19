#! /usr/bin/env python
from collections import defaultdict
import os
import sys
def main(kernel_id):
       SM_access=[]
       SM_numbers=28
       warp_numbers=44
       max_warp=0
       for i in range(0,SM_numbers):
           warp_access=[]
           for j in range(0,10000):
               addr_list=[]
               warp_access.append(addr_list)
           SM_access.append(warp_access)
       memory_trace=open('../memory_access_'+str(kernel_id)+'.txt','r')
       for line in memory_trace:
            access_info=[]
            length=len(line.split(','))
            for i in range(0,length-1):
                access_info.append(line.split(',')[i])
            warp_id=int(line.split(',')[0])
            if (warp_id>max_warp):
                max_warp=warp_id
            if((warp_id==0)and(max_warp>100)):
                break
            pc=int(line.split(',')[1])
            SM_id=(warp_id/warp_numbers)%SM_numbers
            round=warp_id/(warp_numbers*SM_numbers)
            warp=round*warp_numbers+(warp_id%warp_numbers)
            if (warp<10000):
                SM_access[SM_id][warp].append(access_info)
            #if(warp_id<10000):
               # warp_access[warp_id].append(access_info)
    
       print(len(warp_access))
       for i in range(0,SM_numbers):
           SM_access_trace=open('SM_trace_'+str(i)+'.txt','w')
           for j in range(0,len(SM_access[i])/warp_numbers):
                    k=0
                    empty=0
                    while(empty<warp_numbers):
                        if(len(SM_access[i][j*warp_numbers+k])>0):
                            list=SM_access[i][j*warp_numbers+k][0]
                            warp_id=list[0]
                            pc=list[1]
                            W_R=list[2]
                            for n in range(3,len(list)):
                                SM_access_trace.write(warp_id+','+pc+','+W_R+','+list[n]+'\n')
                            SM_access[i][j*warp_numbers+k].pop(0)
                        else:
                            empty+=1
                        k=(k+1)%warp_numbers
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
      
