#!/usr/bin/env python
# coding: utf-8

# ### pseudocode for calculator
# * define raw resources / node type 
# * usable = raw-overhead
# * define desired hardware tier
# * total resources per execution = (hardware tier def + execution overhead) 
# * max executions = int(min(usable cpu/total cpu per execution, usable mem/total mem per execution))
# * define overhead for cpu, memory
# * produce overhead metrics
# * define idle cpu, memory
# * produce utilization metrics

# In[1]:


import pandas as pd
import sys
import os


######## Init ################

global node_overhead_cpu
global node_overhead_mem
global exec_overhead_cpu
global exec_overhead_mem

#node_overhead_cpu = 1.5 #cores
#node_overhead_mem = 2  #GiB
#node_overhead_cpu = reserved_cpu(hw_cpu)
#node_overhead_mem = reserved_mem(hw_mem)

exec_overhead_cpu = 1. #cores
exec_overhead_mem = 1. #GiB

req_cpu = float(sys.argv[1])
req_mem = float(sys.argv[2])


######## Import Data ################

df = pd.read_csv(sys.argv[3])
hw_tier_catalogue = df[['Instance','vCPU*','Mem (GiB)']]

print('number of node types to size with: '+str(len(hw_tier_catalogue)))


######### notes #############
'''define raw resources / node type
usable = raw-overhead
define desired hardware tier
total resources per execution = (hardware tier def + execution overhead)
max executions = int(min(usable cpu/total cpu per execution, usable mem/total mem per execution))
define overhead for cpu, memory
produce overhead metrics
define idle cpu, memory
produce utilization metrics'''


######### Functions ############

def reserved_mem(mem):
    
    kubelet_eviction_reserve = .100
    
    if mem <=1.0:
        #255 MiB of memory for machines with less than 1 GB of memory
        reserved = 0.255
    elif (mem >1.0 and mem<=4.0):
        #25% of the first 4GB of memory
        reserved = .25*mem
    elif (mem >4.0 and mem <=8.0):
        #20% of the next 4GB of memory (up to 8GB)
        reserved = .25*(4.0) + .20*(mem-4.0)
    elif (mem >8.0 and mem <=16.0):
        #10% of the next 8GB of memory (up to 16GB)
        reserved = .25*(4.0) + .20*(4.0) + .10*(mem-8.0)
    elif (mem >16.0 and mem <=128.0):
        #6% of the next 112GB of memory (up to 128GB)
        reserved = .25*(4.0) + .20*(4.0) + .10*(8.0) + .06*(mem-16.0)
    else: 
        #2% of any memory above 128GB
        reserved = .25*(4.0) + .20*(4.0) + .10*(8.0) + .06*(112.0) + .02*(mem-128.0)
    
    node_overhead_mem = reserved + kubelet_eviction_reserve
    return node_overhead_mem
    
def reserved_cpu(cpu):
    if cpu <=1.0:
        #6% of the first core
        reserved = .06*cpu
    elif (cpu >1.0 and cpu<=2.0):
        #1% of the next core (up to 2 cores)
        reserved = .06*1.0 + .01*(cpu-1.0)
    elif (cpu >2.0 and cpu <=4.0):
        #0.5% of the next 2 cores (up to 4 cores)
        reserved = .06*1.0 + .01*(1.0) + .005*(cpu-2.0)
    else: 
        reserved = .06*(1.0) + .01*(1.0) + .005*(2.0) + .0025*(cpu-4)
    
    node_overhead_cpu = reserved
    return node_overhead_cpu

def max_exec(hw_cpu, hw_mem, exec_cpu, exec_mem):
    
    #node_overhead_cpu = reserved_cpu(hw_cpu)
    #node_overhead_mem = reserved_mem(hw_mem)
    
    usable_cpu = hw_cpu - node_overhead_cpu
    #print(usable_cpu)
    usable_mem = hw_mem - node_overhead_mem
    #print(usable_mem)
    
    run_cpu = exec_cpu + exec_overhead_cpu
    #print(run_cpu)
    run_mem = exec_mem + exec_overhead_mem
    #print(run_mem)
    
    execs = 0
    
    while (usable_cpu >= run_cpu and usable_mem >= run_mem): 
        
        execs += 1

        usable_cpu -= run_cpu
        usable_mem -= run_mem
   
    remaining_cpu = usable_cpu
    remaining_mem = usable_mem
    
    o_cpu = node_overhead_cpu + (execs*exec_overhead_cpu)
    o_mem = node_overhead_mem + (execs*exec_overhead_mem)
    
    print('execs: '+str(execs))
    print('remaining_cpu: '+str(remaining_cpu))
    print('remaining_mem: '+str(remaining_mem))
    print('total_cpu_overhead: '+str(o_cpu))
    print('total_mem_overhead: '+str(o_mem))
    
    return execs, remaining_cpu, remaining_mem, o_cpu, o_mem

def overhead(execs, exec_cpu, exec_mem):

    if execs !=0:
        o_cpu = node_overhead_cpu + (execs*exec_overhead_cpu)
        o_mem = node_overhead_mem + (execs*exec_overhead_mem)
        
        print('total_cpu_overhead: '+str(o_cpu))

        tot_cpu = execs * exec_cpu
        print('total execution cores: '+str(tot_cpu))

        tot_mem = execs * exec_mem

        #cpu overhead / total_exec_corese
        ratio_cpu = o_cpu/tot_cpu
        print('overhead ratio, cpu: '+str(ratio_cpu))
        ratio_mem = o_mem/tot_mem
        
    else: #temp set to 100% overhead
        ratio_cpu = 1.
        ratio_mem = 1.
    
    return ratio_cpu, ratio_mem

def utilization(hw_cpu, hw_mem, remaining_cpu, remaining_mem):
    #utilization = (exec_resource_def - idle _resource) / exec_resource_def
    util_cpu = (hw_cpu - remaining_cpu)/hw_cpu
    util_mem = (hw_mem - remaining_mem)/hw_mem
    
    return util_cpu, util_mem

def node_sizing(requested_cpu, requested_mem, hw_tier_data):
    
    df_results = pd.DataFrame(columns=['node_size', 'max_executions', 'overhead_ratio_cpu', 'overhead_ratio_mem', 
                                   'util_ratio_cpu', 'util_ratio_mem', 'efficiency_metric'])
    
    for i in range(len(hw_tier_data)):
        hw_cpu = hw_tier_data.iloc[i,1]
        #print(hw_cpu)
        hw_mem = hw_tier_data.iloc[i,2]
        #print(hw_mem)
        
        #Calculate node overheads for usable resources
        #Note: updated with GKE overhead details from: https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-architecture#node_allocatable
        global node_overhead_cpu
        global node_overhead_mem
        
        node_overhead_cpu = reserved_cpu(hw_cpu)
        node_overhead_mem = reserved_mem(hw_mem)
        
        usable_cpu = hw_cpu - node_overhead_cpu
        usable_mem = hw_mem - node_overhead_mem
        
        print(type(usable_cpu))
        print(type(usable_mem))
        print(type(requested_cpu))
        print(type(requested_mem))
        
        if (usable_cpu > float(requested_cpu) and usable_mem > float(requested_mem)):
                        
            print('core count for eval: '+str(hw_cpu))
            print('memory for eval (GB): '+str(hw_mem))
            
            #note: max_exec also calculates usable, per above.. can clean this up at some point
            execs, remaining_cpu, remaining_mem, o_cpu, o_mem = max_exec(hw_cpu, hw_mem, requested_cpu, requested_mem)
        
            overhead_cpu, overhead_mem = overhead(execs, requested_cpu, requested_mem)
        
            util_cpu, util_mem = utilization(hw_cpu, hw_mem, remaining_cpu, remaining_mem)
        
            eff_cpu = util_cpu/overhead_cpu
            eff_mem = util_mem/overhead_mem
        
            #efficiency_metric = (eff_cpu + 4.*eff_mem)/2.
            #try weighted harmonic mean from: https://en.wikipedia.org/wiki/Harmonic_mean#Harmonic_mean_of_two_numbers
            #with 4:1 weight on memory
            efficiency_metric = 9./((1./eff_cpu) + (8./eff_mem))
        
            df_result = pd.DataFrame({'node_size':hw_tier_data.iloc[i,0],
                                      'max_executions':execs,
                                      'overhead_ratio_cpu': round(overhead_cpu, 2),
                                      'overhead_ratio_mem': round(overhead_mem, 2),
                                      'util_ratio_cpu': round(util_cpu, 2),
                                      'util_ratio_mem': round(util_mem, 2),
                                      'efficiency_metric': round (efficiency_metric,2)}, index = [0])
        
            #print(df_result.shape)
        
            df_results = df_results.append(df_result, ignore_index = True)
            
    #print(df_results.shape)
        
    return df_results


########### Call function ##############

results = node_sizing(req_cpu, req_mem, df)

cols = results.columns.tolist()
cols = cols[:1] + cols[-1:] + cols[1:-1]
results = results[cols] 

results = results.sort_values(['efficiency_metric', 'max_executions'], ascending=[False, False]).reset_index(drop=True)

results.to_csv(os.environ['DOMINO_WORKING_DIR']+'/csv_output/node_recommendations_{}_{}.csv'.format(req_cpu, req_mem))
results.to_html(os.environ['DOMINO_WORKING_DIR']+'/results/node_recommendations_{}_{}.html'.format(req_cpu, req_mem))

