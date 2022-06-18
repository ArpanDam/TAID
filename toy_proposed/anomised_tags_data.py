# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 18:50:23 2022

@author: HP
"""


import pickle



graph=pickle.load(open("toy_graph_anomised","rb"))
tags=set()

for inf in graph:
    
    for follower in graph[inf]:
        for i in graph[inf][follower]:
            tags.add((i[0]))
        

dict1={}
index=1
for ind_node in tags:
    
    if ind_node not in dict1:
        dict1[ind_node]=index
        index=index+1

changed_graph={}

for inf_member in graph:
    temp={}
    for follower in graph[inf_member]:
        list1=[]
        
        for i in graph[inf_member][follower]:
            list1.append((dict1[i[0]],i[1],i[2]))
        temp[follower]=list1
    changed_graph[inf_member]=temp    
            
pickle.dump(changed_graph,open("toy_graph_fully_anomised","wb"))    