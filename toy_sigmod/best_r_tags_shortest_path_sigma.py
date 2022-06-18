
'''Conversation opened. 1 read message.

Skip to content
Using Gmail with screen readers
baseline2 
Meet
Hangouts

6 of many
Baseline code and result
Inbox

Suryansh Kumar
Attachments
Apr 17, 2022, 11:49 AM (12 days ago)
to me

Best r tags for r=3 and seed=[299259, 2794624, 10297783, 10639978, 11900080, 37955902, 38389592, 92911462, 114358222, 183702935] :

{'Making Friends to Travel With', 'Learn How to Be a Success in Network Marketing', 'How to start a business'}



Attachments area
Thanks a lot.Got it, thanks!Thanks for the mail.'''

#Implementation of Batch-Paths selection algorithm of the paper: Finding seeds and relevant tags jointly for Targeted...
'''
Batch-Paths Selection Algorithm
Require: path set P from source set S to target set T , a positive integer r
Ensure: A subset of paths P1 ⊆ P and its tag set C1 whose size is not
larger than r
1: P1 = ϕ, C1 = ϕ
2: Construct path-batches PB and the lattice with P
3: while |PB| > 0 and C1 < r do
4: Find optimal path-batch P∗ to include next (Equation 17)
5: Add all the paths in P∗ and its descendants into P1
6: Add tags of P∗ to C1
7: Update the lattice to remove tags of P∗ from it (Figure 11)
8: end while
9: return Selected tag set C1
'''


import pickle
import operator
import time as T
from collections import defaultdict
import random
import numpy as np
start=T.time()


'''
PB:  key: tagset TS in the form of a tuple, val: list of shortest paths from seed to target corresponding to the tagset TS

enriched_PB: key:tagset TS in the form of a tuple, val: list of paths corresponding to all subsets TS' of TS

C1:best_r_tags
'''



def sigma(S,T,edge_prob,path_batches): #path-batches= desP U PB_dash
	# Input:  edge_prob: graph object, S:set of seed nodes, T:set of target nodes.
	# 		path_batches: set of paths to be considered while implementing independent cascade
	# Output: average number of nodes influenced by the seed nodes
	edges_of_path_batches=set()
	for path in path_batches:
		for edge in path:
			edges_of_path_batches.add(edge)

	#change the original graph to include only those edges which are included in paths of path_batches
	edge_prob_new={}
	for influencer in edge_prob:
		temp1=defaultdict(list)
		for influenced in edge_prob[influencer]:
			for (t,p) in edge_prob[influencer][influenced]:
				if((influencer,influenced,t) in edges_of_path_batches):
					temp1[influenced].append((t,p))
		if len(temp1):
			edge_prob_new[influencer]=temp1
	mc=500
	# Loop over the Monte-Carlo Simulations
	spread = []
	for i in range(mc):
	# Simulate propagation process      
		new_active=[]
		A=[]
		for seed in S:
			new_active.append(seed)
			A.append(seed)
		while new_active:
			# For each newly active node, find its neighbors that become activated
			new_ones = []
			for node in new_active:    
				# Determine all target neighbors whose edge probability is greater than the random probability
				j=1
				if node not in edge_prob_new:
					continue
				for influenced in edge_prob_new[node]:
					if influenced not in T: #if influenced node is not a target node
						continue
					for (t,p) in edge_prob_new[node][influenced]:
						random.seed(j)
						j+=1
						random_prob=random.uniform(0,1)
						if(random_prob<p):
							new_ones.append(influenced)
							break

			new_active = list(set(new_ones) - set(A))
 			# Add newly activated nodes to the set of activated nodes
			A += new_active   
		spread.append(len(A))
	return(np.mean(spread))	




def optimal_path_batch_to_include_next(S,T,PB,PB_dash,enriched_PB,C1,r,edge_prob):
	#check all path batches P in PB\PB_dash, for each P calculate mgr(marginal gain ratio)---[eq 17]
	#Now, return those Ps for which you get the maximum mgr values.
	print("-->Called optimal_path_batch_to_include_next")
	mx=0
	paths_in_PB_dash=set()
	for key in PB_dash: #key:tuple of tags, #val:list of paths
		for path in PB_dash[key]:
			paths_in_PB_dash.add(path)
	p_mgr={} #key:tuple of tags, #val:mgr of path-batch corresponding to the tags
	print("len(PB)=",len(PB))
	i=0
	for key in PB:
		if key in PB_dash: #since we have to check for all path batches P in PB\PB_dash
			continue
		#P=PB[key]
		s=set(key)
		print("---->i=%d"%(i))
		p_mgr[key]=(sigma(S,T,edge_prob,set(enriched_PB[key]).union(paths_in_PB_dash))- sigma(S,T,edge_prob,paths_in_PB_dash))/len(s.difference(C1))
		mx=max(mx,p_mgr[key])
		i+=1
	ret={} #consists of those path-batches as values which give the maximum marginal gain ratio
	for key in p_mgr:
		if(p_mgr[key]==mx and len(key)<=r):
			#add paths of key in PB_dash and in ret
			PB_dash[key]=PB[key]
			ret[key]=PB[key]
	return ret

def batch_path_selection(S,T,r,PB,enriched_PB,edge_prob): #returns the best r tags
	#PB is the tags_pathbatch without the inclusion of descendants
	C1=set()
	PB_dash={}
	i=1
	while len(PB)>0 and len(C1)<r:
		print("Iteration %d of batch path selection"%(i))
		P_star=optimal_path_batch_to_include_next(S,T,PB,PB_dash,enriched_PB,C1,r,edge_prob) #key:tuple of tags, val:list of paths corresponding to those tags
		tags_p_star=set()
		for key in P_star:
			tags_p_star=tags_p_star.union(set(key))
			C1=C1.union(set(key))
		#remove tags of P_star from lattice
		to_be_removed=[]
		for tags in PB:
			#if tags is a subset of tags_p_star or len(C1.union(tags)>r), remove it
			if set(tags).issubset(tags_p_star) or len(C1.union(set(tags)))>r:
				to_be_removed.append(tags)
		for tags in to_be_removed:
			PB.pop(tags)
		i+=1
	return C1

#Create PB and enriched_PB

### Global variables for computing tags_pathbatch ###

tags_in_path={} #key:tag #value:number of times that tag occurs in the path
path_global=[] #list of edges, each edge is identified by a 3-tuple: (from,to,tag) 
path_tagset={}#key:path #val:tag_set of the path, it is basically the table of slide 19

#########################


def pr(path): #prints the path
	for i in range(len(path)-1):
		print(path[i], end='-->')
	print(path[-1])
	print()



def func(node_list,i,r,edge_prob,S): #traverses all paths between a seed node and a target node
	if( len(tags_in_path)>r) or (node_list[i] in S and len(path_global)):	
		return 
	if i==len(node_list)-1: #if we have reached the target nde
		temp=tuple(path_global)
		path_tagset[temp]=set(tags_in_path.keys())
		pr(path_global) #prints the path
		return 
	for (t,p) in edge_prob[node_list[i]][node_list[i+1]]:
		if t in tags_in_path:
			tags_in_path[t]+=1
		else:
			tags_in_path[t]=1
		path_global.append((node_list[i],node_list[i+1],t))
		func(node_list,i+1,r,edge_prob,S)
		if(tags_in_path[t]==1):
			tags_in_path.pop(t) #revert				
		else:
			tags_in_path[t]-=1
		path_global.pop() #revert	


def compute_tags_pathbatch(r,edge_prob,S,all_shortest_paths):
	#find all shortest paths from target to seed users and fill path_tagset
	for B in all_shortest_paths: #B is a target user
		#print("THIS==",all_shortest_paths[B])
		for A in all_shortest_paths[B]: # A is an influential user
			if A in S: # if A is a seed user
				for path in all_shortest_paths[B][A]:
					temp=[]
					for node in path:
						temp.append(node)
					temp.reverse()
					func(temp,0,r,edge_prob,S)#i=0 is the start level				

	#print(len(path_tagset))

	tags_pathbatch={} #key:tuple of tags(cannot use set instead of tuple beacuse set is unhashable) , #val: path-batch, i.e., list of paths corresponding to those tags
	for path in path_tagset:
		tup=tuple(path_tagset[path])
		if tup in tags_pathbatch:
			tags_pathbatch[tup].append(path)
		else:
			tags_pathbatch[tup]=[path]

	PB=tags_pathbatch
	enriched_PB=PB
	for tags in enriched_PB:
		#check all subsets of tags, if any of the subsets is present as a key in the dictionary, add its val in tags_pathbatch[tags]		
		n=len(tags)
		for i in range((1<<n)-1): #consider every subset except the set containing all elements
			s=set()
			for j in range(n):
				if((1<<j)&i):
					s.add(tags[j])
			tup=tuple(s)
			if tup in enriched_PB:
				for path in enriched_PB[tup]:
					enriched_PB[tags].append(path)
	return PB,enriched_PB



edge_prob=pickle.load(open("edge_probability_career","rb"))
all_shortest_paths=pickle.load(open("dict_for_all_shortest_path_for_all_users","rb"))
S=set([2794624, 8953344, 7092500, 3919257, 13831197, 184864166, 9726633, 11168170, 11900080, 183706546, 10297783, 37955902, 184195777, 75088462, 38389592, 105745502, 10639978, 9420651, 3437293, 13149935, 299259] )#seed
r=7
import generate_original_graph_for_input
reverse_graph=generate_original_graph_for_input.generate_reverse_graph(edge_prob)
number_of_target_users=100
T=set()#target


    
dict_for_target_users=generate_original_graph_for_input.give_target_user(reverse_graph,number_of_target_users)
for key in dict_for_target_users:
	T.add(key)
dict1={}    
for key in T:
   
    dict1[key]= all_shortest_paths[key] 
all_shortest_paths=dict1      
PB,enriched_PB=compute_tags_pathbatch(r,edge_prob,S,all_shortest_paths)
best_r_tags=batch_path_selection(S,T,r,PB,enriched_PB,edge_prob)
print(best_r_tags)
{'Be the Change You Wish to See in the World', 'Exercise and Have Fun at the same time', '"Cloud Computing" How to use it for your business', 'Public Speaking as a Means to Market your Business', 'Meeting other parents', 'Learn How to Be a Success in Network Marketing', 'Seminars on First Time Home Buyers'}
'''baseline.py
Displaying baseline.py.'''