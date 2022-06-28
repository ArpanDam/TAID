# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 17:49:12 2022

@author: HP
"""

import pickle
import random
import numpy as np



def find_neighbours(target,graph):
    neighs = []
    for node in graph:
        #if node == target:
        for follower in graph[node]:
            if follower == target:
                neighs.append(node)
    return(neighs) 

def first_diffusion(node,graph,list_outer):
    
    influenceable = [] #List of nodes can be influenced by node
    no_of_influenceable = 0 #Number of nodes can be influenced by node
    
    for item in list_outer:
        if (item[0]==node and item[3]>item[2]):
            influenceable.append(item[1])
                        
    return(influenceable)

def network_diffusion(nodess,list_outer,graph):
    
    temp_diff = []
    for node in nodess: #node is in active_nodes
              
        for item in list_outer:
            influence_val = 0
            node_adjacent = 0
            
            if (item[0] == node and item[1] not in nodess): #neighbour is not in active_nodes
                node_adjacent = item[1]
                influence_val = influence_val + item[3]
                neighs = find_neighbours(node_adjacent,graph)
                for n in neighs:
                    for item in list_outer:
                        if item[0]==n and n in nodess and item[1] == node_adjacent:
                                influence_val = influence_val + item[3]
        
            if influence_val>=item[2] and node_adjacent != 0:
                temp_diff.append(node_adjacent)
                    
    return(temp_diff)
def main(graph,seed,dict_for_influence_tags,dict_for_target_users):
    new_graph={}
    number_of_active_list=[]
    for inf in graph:
        temp={}
        for follower in graph[inf]:
            list1=[]
            for i in graph[inf][follower]:
                if i[0] in dict_for_influence_tags:
                    list1.append((i[0],i[1],i[2]))
            temp[follower]=list1
        new_graph[inf]=temp    
    graph=new_graph        
    graph_nodes = []
    for node in graph:
        graph_nodes.append(node)
        
    for node in graph:
        for follower in graph[node]:
            graph_nodes.append(follower)    
    number_of_graph_nodes=len(set(graph_nodes))
    graph_nodes = list(set(graph_nodes))
    #print(len(graph_nodes)) 
    #print(graph_nodes)
    
    
    #no_of_seeds = 5
    no_of_iterations = 1000
    
    #seed_nodes = random.sample(graph_nodes, no_of_seeds)
    #seed_nodes = [10297783, 10639978, 37008262]
    #print("Seed nodes: ", seed_nodes)
    seed_nodes=seed
    avg_active_nodes = []
    
    for j in range(no_of_iterations):
        
        #print('------------------------------------------------')
        #print("Iteration number: ", j)
            
        list_outer = []
    
        for node in graph:
            for follower in graph[node]:
                for follower_info in graph[node][follower]:
                    list_inner = []
                    list_inner.append(node)
                    list_inner.append(follower)
                    
                    threshold = round(random.uniform(0,1),2) #threshold of the neighbour
                    list_inner.append(threshold)
                
                    list_inner.append(follower_info[1])
                    list_outer.append(list_inner)
        
        active_nodes = []
        no_of_seeds=len(seed_nodes)
        for i, node in zip(range(no_of_seeds), seed_nodes):
    
            if i==0:
                active = first_diffusion(node,graph,list_outer)
                active_nodes.append(node)  
                active_nodes.extend(active)
                active_nodes = list(set(active_nodes))
                    
            else:
                nodess = []
                nodess.extend(active_nodes)
                nodess.append(node)
                nodes = network_diffusion(nodess,list_outer,graph)
                active_nodes.append(node)
                active_nodes.extend(nodes)
                active_nodes = list(set(active_nodes))
               
        #print("Active nodes: ", active_nodes)
        #print("Number of active nodes: ", len(active_nodes))
        
        avg_active_nodes.append(len(active_nodes))
        number_of_active=0    
        for node in active_nodes:
            if node in dict_for_target_users:
                number_of_active=number_of_active+1
        number_of_active_list.append(number_of_active) 
    #print(number_of_active_list)    
    return (sum(number_of_active_list)/len(number_of_active_list)/len(dict_for_target_users)) 
    #((np.mean(avg_active_nodes)/number_of_graph_nodes) *100)        
    

