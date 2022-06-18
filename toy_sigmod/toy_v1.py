# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 20:46:23 2022

@author: HP
"""

import pickle

import generate_original_graph_for_input
import RRS
import  dictionary_from_bfs
import generate_original_graph_for_input2
import Evaluation_all_positive_considering_target_users


import Evaluation_number_of_target_nodes_positively_activated_part2 # for positive influence evaluation

import best_r_tags_2nd_code

percentile=25
r=5
k=4

Number_of_sample_graphs=1000  # Number of iteration
graph=pickle.load(open("toy_graph","rb"))
reverse_graph=generate_original_graph_for_input.generate_reverse_graph(graph)
value=generate_original_graph_for_input2.give_r_percentile(reverse_graph,percentile)
iteration=1


dict_for_target_users=generate_original_graph_for_input2.give_target_user_based_on_percentile(reverse_graph,value)
#print(dict_for_target_users)
dict_for_influence_tags=generate_original_graph_for_input.give_all_tags(dict_for_target_users,reverse_graph,r+1)
number_of_target_users=len(dict_for_target_users)   
iteration=1
while(True):
    #print(dict_for_influence_tags)
    old_influence_key=set()
    for key in dict_for_influence_tags:
        old_influence_key.add(key)  
    new_influence_key=set()
    
    
   
    filtered_reverse_graph={}
    filtered_reverse_graph=RRS.generate_graph_having_only_r_tags(reverse_graph,dict_for_influence_tags)
    
    final_list_of_RRS_set={}
    final_list_of_RRS_set=RRS.genrating_many_sampled_graph(filtered_reverse_graph,Number_of_sample_graphs,dict_for_target_users) 
   
    top_influencial_member=RRS.find_top_influencial_member(final_list_of_RRS_set,k) # 20 is the budget
    
    
    
   
    number_of_influenced_node,list_of_influenced_node=Evaluation_all_positive_considering_target_users.number_of_influenced_member(top_influencial_member,reverse_graph,dict_for_influence_tags,dict_for_target_users,number_of_target_users)
    
    
    number_of_influenced_node="{:.2f}".format(number_of_influenced_node)
    old_number_of_influenced_node=number_of_influenced_node
    
    list_of_intermediate_graph=[]
    list_of_dictionary_of_shortest_path=[]
    list_of_intermediate_graph,list_of_dictionary_of_shortest_path=dictionary_from_bfs.generating_many_list_of_shortest_path(reverse_graph,Number_of_sample_graphs,dict_for_target_users,top_influencial_member)
    
    
   
    set_key1=best_r_tags_2nd_code.output_dictionary_of_tag_batch_with_gain(top_influencial_member,Number_of_sample_graphs,list_of_intermediate_graph,list_of_dictionary_of_shortest_path,r,dict_for_target_users)
   
    #print("Set key 1",set_key1)
    dict_for_influence_tags=set_key1
    
    number_of_influenced_node,list_of_influenced_node=Evaluation_all_positive_considering_target_users.number_of_influenced_member(top_influencial_member,reverse_graph,dict_for_influence_tags,dict_for_target_users,number_of_target_users)
       
    number_of_influenced_node="{:.2f}".format(number_of_influenced_node)
    new_number_of_influenced_node=number_of_influenced_node    
                
    if((float(new_number_of_influenced_node) - float(old_number_of_influenced_node)) ==0): #     CONVERGENCE CONDITION
        #print("Converge in influence spread")
        break        
            
                
                
    
    iteration=iteration+1
            
           
                
                    
new_number_of_influnced_node=Evaluation_number_of_target_nodes_positively_activated_part2.number_of_influenced_member(top_influencial_member,reverse_graph,dict_for_influence_tags,dict_for_target_users,number_of_target_users)                    
print("Positive influence spread is ",new_number_of_influnced_node) 
print("best influuecnial nodes are",top_influencial_member)   
print("best influence Tags  nodes are",dict_for_influence_tags)


