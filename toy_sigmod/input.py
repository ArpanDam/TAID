# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 20:46:23 2022

@author: HP
"""

import pickle
import numpy as np
import generate_original_graph_for_input
import RRS
import  dictionary_from_bfs
#import best_r_tags_shortest_path
#import best_tag_finder
#import best_tag_finder_new_defintion
import Evaluation_all_positive_considering_target_users
#import matplotlib.pyplot as plt
import time

#import best_r_tags_shortest_path_new_defintion_copy
import best_r_tags_2nd_code

##############
#set1={('Learn How to Be a Success in Network Marketing', 'Public Speaking as a Means to Market your Business'), ('Public Speaking as a Means to Market your Business',), ('Learn How to Be a Success in Network Marketing', 'Public Speaking as a Means to Market your Business', '"Cloud Computing" How to use it for your business'), ('Learn How to Be a Success in Network Marketing', 'Seminars on First Time Home Buyers', 'Public Speaking as a Means to Market your Business'), ('Learn How to Be a Success in Network Marketing', 'Public Speaking as a Means to Market your Business', 'Making a Difference in the World')}
print("")
file_number=1
############
while file_number<=1:
#file_name_sign="influence_tags_sign_"+str(number_of_files)
    file_name_sign="influence_tags_sign_"+str(file_number)
    print(file_name_sign)
    sign_dictionary=pickle.load(open("../Example of career group tags and its dictionary of positive negative tags_0.8/"+file_name_sign,"rb"))  # portion of the graph
    #group_tags=np.load("../Example of career group tags and its dictionary of positive negative tags_0.8/group_tags_5.npy", mmap_mode=None, allow_pickle=True, fix_imports=True, encoding='ASCII')
    
    
    edge_probability_career=pickle.load(open("edge_probability_career","rb")) # portion of the graph
    
    
        
    
    k =5
    r=5
    
    number_of_target_users=100
    
    Number_of_sample_graphs=500
    
    ##################################
    # found the target users ,  original graph and the set of initial r tags
    graph=generate_original_graph_for_input.generate_final_graph(sign_dictionary,edge_probability_career)
    reverse_graph=generate_original_graph_for_input.generate_reverse_graph(graph)
    dict_for_target_users=generate_original_graph_for_input.give_target_user(reverse_graph,number_of_target_users) # 400 is the number of target user
    print(dict_for_target_users)
    dict_for_influence_tags=generate_original_graph_for_input.give_all_tags(dict_for_target_users,reverse_graph,r+1)
    iteration=1
    while(iteration < 10):
        #print(dict_for_influence_tags)
        old_influence_key=set()
        for key in dict_for_influence_tags:
            old_influence_key.add(key)  
        new_influence_key=set()
        
        print("New iteration")
        print(dict_for_influence_tags)
        #dict_for_influence_tags={'"Cloud Computing" How to use it for your business', 'The Human Energy Field: A Practical Introduction', 'Making Friends to Travel With', 'Public Speaking as a Means to Market your Business', 'Learn How to Be a Success in Network Marketing', 'Building Network Marketing Skills and Strategies', 'How to start a business'}
        filtered_reverse_graph={}
        filtered_reverse_graph=RRS.generate_graph_having_only_r_tags(reverse_graph,dict_for_influence_tags)
        try:
            final_list_of_RRS_set={}
            final_list_of_RRS_set=RRS.genrating_many_sampled_graph(filtered_reverse_graph,Number_of_sample_graphs,dict_for_target_users) 
            # got the list_of_intermediate_graph, use this same intermediate graph for finding best r tags and evaluation
            #dict_for_influence_tags={'Seminars on First Time Home Buyers', '"Cloud Computing" How to use it for your business', 'Learn How to Be a Success in Network Marketing', 'Meetings other couples who share your interest too', 'Making a Difference in the World', 'The Secret (DVD) Making It Work For You', 'Public Speaking as a Means to Market your Business'}
            top_influencial_member=RRS.find_top_influencial_member(final_list_of_RRS_set,k) # 20 is the budget
            #top_influencial_member=[321158, 2794624, 7130244, 7964051, 9779381, 10297783, 11900080, 39398622, 49753142, 97940722]
            #top_influencial_member=[321158, 2775988, 2794624, 2884706, 9078175, 10205905, 10642198, 12140271, 39398622, 127409112]
            print(top_influencial_member)
            
            number_of_influenced_node,list_of_influenced_node=Evaluation_all_positive_considering_target_users.number_of_influenced_member(top_influencial_member,reverse_graph,dict_for_influence_tags,dict_for_target_users,number_of_target_users)
            # Using the seed users find the best set of influence tags
            print(number_of_influenced_node)
            old_number_of_influenced_node=number_of_influenced_node
            list_of_intermediate_graph=[]
            list_of_dictionary_of_shortest_path=[]
            list_of_intermediate_graph,list_of_dictionary_of_shortest_path=dictionary_from_bfs.generating_many_list_of_shortest_path(reverse_graph,Number_of_sample_graphs,dict_for_target_users,top_influencial_member)
            
            
            final_tag_gain={}
            
            set_key=set()
           
            set_key1=best_r_tags_2nd_code.output_dictionary_of_tag_batch_with_gain(top_influencial_member,Number_of_sample_graphs,list_of_intermediate_graph,list_of_dictionary_of_shortest_path,sign_dictionary,r,dict_for_target_users)
            
            
            dict_for_influence_tags=set_key1
            print(dict_for_influence_tags)
            number_of_influenced_node,list_of_influenced_node=Evaluation_all_positive_considering_target_users.number_of_influenced_member(top_influencial_member,reverse_graph,dict_for_influence_tags,dict_for_target_users,number_of_target_users)
            print(number_of_influenced_node)
            
            new_influence_key=set()
            for key in dict_for_influence_tags:
                new_influence_key.add(key)
            if(new_influence_key == old_influence_key):
                print("No change in influence key")
                f = open("demofile.txt", "w+")
                f.write(str(list_of_influenced_node))
                f.close()
                break
            else:    
                
                number_of_influenced_node,list_of_influenced_node=Evaluation_all_positive_considering_target_users.number_of_influenced_member(top_influencial_member,reverse_graph,dict_for_influence_tags,dict_for_target_users,number_of_target_users)
                print(number_of_influenced_node)
                if(number_of_influenced_node >= old_number_of_influenced_node):
                    print("Sucess")
                else:
                    print("Failure")
                print("Checking if any tag is negative")
                flag=0
                for tag_for_checking in dict_for_influence_tags:
                    if(sign_dictionary[tag_for_checking]=='neg'):
                        print("Negative tag is ",tag_for_checking)
                        flag=1
                if(flag==0):
                    print("No negative tags found")
        except:
            pass            
        iteration=iteration+1            
    '''print(dict_for_target_users)                
    graph=generate_original_graph_for_input.generate_final_graph(sign_dictionary,edge_probability_career)
    reverse_graph=generate_original_graph_for_input.generate_reverse_graph(graph)
    dict_for_target_users=generate_original_graph_for_input.give_target_user(reverse_graph,number_of_target_users)'''               
                    
                    
    file_number=file_number+1           
        
   
print("End")
# Normalise the gain
