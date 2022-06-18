# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 11:33:34 2022

@author: HP
"""

import pickle
import numpy as np
import generate_original_graph_for_input
import find_seed_from_influence_tags_having_many_graph
import  dictionary_from_bfs
import generate_original_graph_for_input2
#import best_r_tags_shortest_path
#import best_tag_finder
#import best_tag_finder_new_defintion
import Evaluation_number_of_target_nodes_positively_activated_part2
#import matplotlib.pyplot as plt
import time

import best_r_tags_shortest_path_new_defintion_copy

edge_probability_career=pickle.load(open("edge_probability_career","rb")) # portion of the graph
file_number=1
file_name_sign="influence_tags_sign_"+str(file_number)
sign_dictionary=pickle.load(open("../Examples_0.8/"+file_name_sign,"rb"))  # portion of the graph
graph=generate_original_graph_for_input.generate_final_graph(sign_dictionary,edge_probability_career)
new_graph={}

number_of_inf=0
for inf_member in graph:
    number_of_inf=number_of_inf+1
    temp={}
    for follower in graph[inf_member]:
        list1=[]
        for i in graph[inf_member][follower]:
            list1.append((i[0],i[1],i[2]))
        temp[follower]=list1
    new_graph[inf_member]=temp 
    if(number_of_inf==50):
        break
            
number_of_node=set()

for nodes in new_graph:
    number_of_node.add(nodes)
    for follower in new_graph[nodes]:
        number_of_node.add(follower)        
print("number_of_node is",len(number_of_node))

pickle.dump(new_graph,open("toy_graph","wb"))