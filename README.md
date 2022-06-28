# TAID
There are 2 folders (a) One folder contains our proposed algorithm TAID (b) Another folder contains Sigmod paper algoroithm

A toy graph is being provided which is fully anonymized, The toy graph is in the form of dictionary and store in pickle file. Members and influence tags are labelled as 
digits in the toy graph.

1. Run `python TAID.py number_of_influencial_users number_of_influence_tags percentile' to run TAID  and get the output as expected influence spread, top-k influencial nodes and top-r influence tags. 

  Example : Run 'python TAID.py 4 5 50' 
  If no parameter is provided then  k, r and percentile is being provided as 4,5 and 50. 

  Only Run 'python TAID.py' to run the code with k(number of influencial user), r(number of influence tags) and percentile as 4,5 and 50

2. Run `python SIGMOD.py number_of_influencial_users number_of_influence_tags percentile' to run SYGMOD algorithm and get the output as and get the output as expected    influence spread, top-k influencial nodes and top-r influence tags.
 
   Example : Run 'python SIGMOD.py 4 5 50'
   If no parameter is provided then  k, r and percentile is being provided as 4,5 and 50. 
 
   Only Run 'python SIGMOD.py' to run the code with k(number of influencial user), r(number of influence tags) and percentile as 4,5 and 10 
