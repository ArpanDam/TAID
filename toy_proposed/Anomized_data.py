# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 18:50:23 2022

@author: HP
"""


import pickle



graph=pickle.load(open("toy_graph","rb"))
nodes=set()

for inf in graph:
    nodes.add(inf)
    for follower in graph[inf]:
        nodes.add(follower)

dict1={}
index=1
for ind_node in nodes:
    
    if ind_node not in dict1:
        dict1[ind_node]=index
        index=index+1

changed_graph={}

for inf_member in graph:
    temp={}
    for follower in graph[inf_member]:
        list1=[]
        
        for i in graph[inf_member][follower]:
            list1.append((i[0],i[1],i[2]))
        temp[dict1[follower]]=list1
    changed_graph[dict1[inf_member]]=temp    
            
pickle.dump(changed_graph,open("toy_graph_anomised","wb"))    