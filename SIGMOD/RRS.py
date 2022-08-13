# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 17:06:50 2022

@author: HP
"""

import pickle
import random
from random import uniform, seed
import numpy as np
#from igraph import *
import pickle
#import matplotlib.pyplot as plt
#from scipy import stats
from numpy import save
from numpy import load
from numpy import dot
from numpy.linalg import norm
#from igraph import *
#import matplotlib.pyplot as plt
from queue import Queue
import pandas as pd
import generate_original_graph_for_input

'''edge_probability_career = pickle.load(open("edge_probability_career","rb"))
sign_dictionary=pickle.load(open("../Example of career group tags and its dictionary of positive negative tags_0.8/influence_tags_sign_5","rb"))        
group_tags=np.load("../Example of career group tags and its dictionary of positive negative tags_0.8/group_tags_5.npy", mmap_mode=None, allow_pickle=True, fix_imports=True, encoding='ASCII')
# 15 group tags 
graph=generate_original_graph_for_input.generate_final_graph(sign_dictionary)
reverse_graph=generate_original_graph_for_input.generate_reverse_graph(graph)
dict_for_target_users=generate_original_graph_for_input.give_target_user(reverse_graph,400) # 400 is the number of target user
dict_for_influence_tags=generate_original_graph_for_input.give_best_postive_tags(dict_for_target_users,reverse_graph,6)
dict_for_influence_tags={'Learn How to Be a Success in Network Marketing', 'Seminars on First Time Home Buyers', '"Cloud Computing" How to use it for your business', 'How to start a business', 'Public Speaking as a Means to Market your Business'}
#dict_for_influence_tags=generate_original_graph_for_input.give_all_tags(dict_for_target_users,reverse_graph)
#{'Learn How to Be a Success in Network Marketing': 727, 'Public Speaking as a Means to Market your Business': 436, '"Cloud Computing" How to use it for your business': 311, 'Seminars on First Time Home Buyers': 150, 'Making Friends to Travel With': 142, 'How to make money in network marketing': 130}
print(dict_for_influence_tags)'''
#dict_for_influence_tags={'Learn How to Be a Success in Network Marketing', 'Public Speaking as a Means to Market your Business', '"Cloud Computing" How to use it for your business', 'Seminars on First Time Home Buyers', 'How to start a business'}
#dict_for_influence_tags={'Learn How to Be a Success in Network Marketing': 730, 'Public Speaking as a Means to Market your Business': 446, '"Cloud Computing" How to use it for your business': 310, 'How to start a business': 143, 'How to make money in network marketing': 131, 'How To Use Social Media To Promote Your Business': 118, 'Market Your Small Business Locally On The Internet': 58, 'How To Build Business Credit': 37}
#dict_for_influence_tags={'Public Speaking as a Means to Market your Business': 440, 'Exercise and Have Fun at the same time': 280, 'Seminars on First Time Home Buyers': 155, 'How to start a business': 138, 'Learn How to Be a Success in Network Marketing': 596}
#dict_for_influence_tags={'Learn How to Be a Success in Network Marketing': 727,'Public Speaking as a Means to Market your Business': 436,'Exercise and Have Fun at the same time': 207, 'The Secret (DVD) Making It Work For You': 95, 'Making a Difference in the World': 93, 'Dining Out, BBQs, Food Fairs, Happy Hour and More': 67}
def generate_graph_having_only_r_tags(reverse_graph,dict_for_influence_tags):
    influence_tags=set()
    dict1={}
    for tags in dict_for_influence_tags:
        influence_tags.add(tags)
    for follower in reverse_graph:
        temp={}
        for influencer in reverse_graph[follower]:
            
            list1=[]
            for i in reverse_graph[follower][influencer]:
                if (i[0] in influence_tags):
                    list1.append((i[0],i[1],i[2]))
            if (len(list1)>0):        
                temp[influencer]=list1
        if ( bool(temp)): # false if empty        
            dict1[follower]=temp
    return dict1         
                
#filtered_reverse_graph=generate_graph_having_only_r_tags(reverse_graph,dict_for_influence_tags)    # filtered_reverse_graph contains the reverse of the graph and the tags are only the r tags
# remove all the edges having different tags
def positive_node_and_path_finder(adj_list, start_node, target_node,graph):  # input - the target node(start_node) and the 
                                                                      # list of nodes reachable from the target nodes.
                                                                      # list of nodes reachable from the target nodes is the output
                                                                      # of BFS algorithm
                                                                      # Output - path and the set of nodes which postively influnce the target node
    target_node1=target_node                            
    # Set of visited nodes to prevent loops
    visited = set()
    queue = Queue()

    # Add the start_node to the queue and visited list
    queue.put(start_node)
    visited.add(start_node)
    
    # start_node has not parents
    parent = dict()
    parent[start_node] = None

    # Perform step 3
    path_found = False
    while not queue.empty():
        current_node = queue.get()
        if current_node == target_node:
            path_found = True
            break
        if(current_node in adj_list):
            for next_node in adj_list[current_node]:
                if next_node not in visited:
                    queue.put(next_node)
                    parent[next_node] = current_node
                    visited.add(next_node)
                         
                
    # Path reconstruction
    path = []
    if path_found:
        path.append(target_node)
        while parent[target_node] is not None:
            path.append(parent[target_node]) 
            target_node = parent[target_node]
        path.reverse()
    #print("")
    # Here path is the list of nodes example   [80674, 299259, 9321243, 101694462]
    # now need to find if the last node of the path is posstively being influenced if yes the return the path
    # consisting of events id
    #number_of_positively_activated=0
    #number_of_negatively_activated=0
    if(len(path)>3):
        pass
    positively_activated_node=[]
    negatively_activated_node=[]
    for i in range(len(path)-1):
        
        previous_node=path[i]
        next_node=path[i+1]
        sum_positive=0
        sum_negative=0
        for j in graph[previous_node][next_node]:
            if(j[2]=='pos'):
                sum_positive=j[1]+sum_positive
            if(j[2]=='neg'):
                sum_negative=j[1]+sum_negative
        if(sum_positive>sum_negative):
            positively_activated_node.append(previous_node)
        else:
            negatively_activated_node.append(previous_node)
    '''if(len(negatively_activated_node)>0):
        print("")'''        
    if(len(positively_activated_node) > len(negatively_activated_node)):
        target_node=[]
        target_node.append(target_node1)
        return (target_node,path) # we only need the positive node
    else:
        target_node1=[]
        return(target_node1,path)    # Return no node since number of negatively activated node > number of positively activated node

   

def bfs(visited, graph, node): #function for BFS , output the set of nodes reachable from the input node
  visited = [] # List for visited nodes.
  queue = []     #Initialize a queue
  visited.append(node)
  queue.append(node)
  list1=[]   
  while queue:          # Creating loop to visit each node
    m = queue.pop(0) 
    #print (m, end = " ")
    list1.append(m)
    
    if m in graph:
        for neighbour in graph[m]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
    else:
        pass             
                
  return list1

def RRS_set_genetaor(graph,dict_for_target_users):
    target_users=set()
    for member in dict_for_target_users:
        target_users.add(member)
    list_of_RRS_set=[]
          
        
    for target_user in target_users:
        visited=[]               
        list1=bfs(visited, graph, target_user)
        list1.remove(target_user)
        list_of_RRS_set.append(list1)
        '''set_positive_nodes=set()
        for member in list1:
            positive_node,path = positive_node_and_path_finder(graph, target_user, member,graph)
            if(len(positive_node)>0):
                for i in positive_node:
                    set_positive_nodes.add(i)
        if(len(set_positive_nodes)>0):
            list_of_RRS_set.append(list(set_positive_nodes))'''
    return(list_of_RRS_set)            
    
from collections import Counter   

#RRS_set=RRS_set_genetaor(filtered_reverse_graph,dict_for_target_users)

# Find the influencial members having most number of occusrence in RRS_set
def find_top_influencial_member(RRS_set,k): # k is the budget of the influencial member
    SEED=[]
    for _ in range(k):
        
        # Find node that occurs most often in R and add to seed set
        flat_list = [item for sublist in RRS_set for item in sublist]
        seed = Counter(flat_list).most_common()[0][0]
        SEED.append(seed)
        
        # Remove RRSs containing last chosen seed 
        RRS_set = [rrs for rrs in RRS_set if seed not in rrs]
        
        # Record Time
        #timelapse.append(time.time() - start_time)
    return(sorted(SEED))        
def genrating_many_sampled_graph(G,number_of_graphs,dict_for_target_users):
    final_list_of_RRS_set=[]
    #list_of_intermediate_graph=[]
    #number_of_graphs=500
    for no in range(number_of_graphs):
        
        intermediate_graph={}
        for follower in G:
            temp={}
            for influencer in G[follower]:
                list1=[]
                for i in G[follower][influencer]:
                    # i correspond to each edge
                    if(random.uniform(0, 1)<i[1]): # add the edge else continue
                        list1.append((i[0],i[1],i[2]))
                if(len(list1)>0):        
                    temp[influencer]=list1
            if ( bool(temp)):        
                intermediate_graph[follower]=temp 
        #list_of_intermediate_graph.append(intermediate_graph)        
        RRS_set=RRS_set_genetaor(intermediate_graph,dict_for_target_users) # get multiple RRS set for each intermediate graoh       
        for individual_RRS_set in RRS_set:
            final_list_of_RRS_set.append(individual_RRS_set)
            
        #print("")
    return  final_list_of_RRS_set      
    '''source=[]
    target=[]
    
    for key in G:
        for i in G[key]:
            neighbour=i
            weight=G[key][i]
            for j in range(weight):
                source.append(key)
                target.append(neighbour)'''
                

    
#final_list_of_RRS_set=genrating_many_sampled_graph(filtered_reverse_graph,0.1,500) 
#top_influencial_member=find_top_influencial_member(final_list_of_RRS_set,20) # 20 is the budget 
#print(top_influencial_member)
