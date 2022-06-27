import pickle

import generate_original_graph_for_input
import find_seed_from_influence_tags_having_many_graph
import  dictionary_from_bfs
import generate_original_graph_for_input2

import Evaluation_number_of_target_nodes_positively_activated_part2

import linear_threshold
import  best_r_tags_shortest_path_new_defintion_copy_checking_last_gain

import sys

'''print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))
print("length is",len(sys.argv))'''
if(len(sys.argv) == 4):
    percentile=int(sys.argv[3])
    r=int(sys.argv[2]) # Number of influence tags
    k=int(sys.argv[1]) # Number of Influencial users

if(len(sys.argv) != 4):
    percentile=10
    r=4 # Number of influence tags
    k=5# Number of Influencial users    


Number_of_sample_graphs=1000  # Number of iteration
graph=pickle.load(open("toy_graph","rb"))

reverse_graph=generate_original_graph_for_input.generate_reverse_graph(graph)
value=generate_original_graph_for_input2.give_r_percentile(reverse_graph,percentile)
dict_for_target_users=generate_original_graph_for_input2.give_target_user_based_on_percentile(reverse_graph,value)

number_of_target_users=len(dict_for_target_users)

dict_for_influence_tags=generate_original_graph_for_input.give_best_postive_tags(dict_for_target_users,reverse_graph,r+1)
iteration=1

print("For k = ",k,"r=",r,"and percentile =",percentile)
dict_for_influence_tags=generate_original_graph_for_input.give_best_postive_tags(dict_for_target_users,reverse_graph,r+1)
iteration_number=0

while(True):
    
    old_influence_key=set()
    for key in dict_for_influence_tags:
        old_influence_key.add(key)  
    new_influence_key=set()
    
    print("New iteration")
    print("Potential r influence tags are")
    print(dict_for_influence_tags)
    
    
    filtered_reverse_graph={}
    filtered_reverse_graph=find_seed_from_influence_tags_having_many_graph.generate_graph_having_only_r_tags(reverse_graph,dict_for_influence_tags)
    
    final_list_of_RRS_set={}
    final_list_of_RRS_set=find_seed_from_influence_tags_having_many_graph.genrating_many_sampled_graph(filtered_reverse_graph,Number_of_sample_graphs,dict_for_target_users) 
    
    top_influencial_member=find_seed_from_influence_tags_having_many_graph.find_top_influencial_member(final_list_of_RRS_set,k) 
    
    
    number_of_influenced_node=Evaluation_number_of_target_nodes_positively_activated_part2.number_of_influenced_member(top_influencial_member,reverse_graph,dict_for_influence_tags,dict_for_target_users,number_of_target_users)
    # Using the seed users find the best set of influence tags
    iteration_number=iteration_number+0.5
    number_of_influenced_node="{:.2f}".format(number_of_influenced_node)
    print("positive influence spread in ",iteration_number," iteration is",number_of_influenced_node)
    print("Updating influence tags ..")
    old_number_of_influenced_node=number_of_influenced_node
    list_of_intermediate_graph=[]
    list_of_dictionary_of_shortest_path=[]
    list_of_intermediate_graph,list_of_dictionary_of_shortest_path=dictionary_from_bfs.generating_many_list_of_shortest_path(reverse_graph,Number_of_sample_graphs,dict_for_target_users,top_influencial_member)
    
    
    set_key1=best_r_tags_shortest_path_new_defintion_copy_checking_last_gain.output_dictionary_of_tag_batch_with_gain(top_influencial_member,Number_of_sample_graphs,list_of_intermediate_graph,list_of_dictionary_of_shortest_path,r,dict_for_target_users)
    #set_key1=best_r_tags_shortest_path_new_defintion_copy.output_dictionary_of_tag_batch_with_gain(top_influencial_member,Number_of_sample_graphs,list_of_intermediate_graph,list_of_dictionary_of_shortest_path,r,dict_for_target_users)
    
    
    dict_for_influence_tags=set_key1
    print(dict_for_influence_tags)
       
    new_number_of_influnced_node=Evaluation_number_of_target_nodes_positively_activated_part2.number_of_influenced_member(top_influencial_member,reverse_graph,dict_for_influence_tags,dict_for_target_users,number_of_target_users)
    iteration_number=iteration_number+0.5 
    new_number_of_influnced_node="{:.2f}".format(new_number_of_influnced_node)
    print("positive influence spread in ",iteration_number,"iteration is",new_number_of_influnced_node)
     
    #new_number_of_influnced_node = "{:.2f}".format(new_number_of_influnced_node)
    #old_number_of_influenced_node = "{:.2f}".format(old_number_of_influenced_node)
    if((float(new_number_of_influnced_node) - float(old_number_of_influenced_node)) ==0): #     CONVERGENCE CONDITION
        print("Converge in influence spread")
        break
print("\n")       
#print("Positive influence spread is ",new_number_of_influnced_node*100) 
print("Best influential nodes are",top_influencial_member)   
print("Best influence Tags are",dict_for_influence_tags)


# Using Lienar threshold for evaluation 
print("using linear threshold influence spread is")
print("Positive influence spread is",linear_threshold.main(graph,top_influencial_member,dict_for_influence_tags,dict_for_target_users)*100)
print("End")