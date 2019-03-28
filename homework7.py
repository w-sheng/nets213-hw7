############################################################
# NETS 213: Homework 7
############################################################

import pandas as pd

# Part 1 - Majority vote

def majority_vote(mturk_res):
	## Retrieving relevant columns
	cols = ['Input.attr_id']

	adjstring = 'Input.adj_'
	ansstring = 'Answer.adj_'

	for i in range(1,11):
	    cols.append(adjstring + str(i))
	for i in range(1,11):
	    cols.append(ansstring + str(i))

	mturk_res = mturk_res[cols]
	
	## Creating majority label
	max_val = int(9 / 3)
	labels = {}

	# Loop through all attributes
	for i in range(1,max_val):
	    temp_df = mturk_res.iloc[(3*(i-1)):(3*i):, :]
	    attr = temp_df.iloc[0]['Input.attr_id']
	    
	    # Loop through all 10 adjectives
	    for j in range(1,11):
	        adj = temp_df.iloc[0][input_cols[j]]
	        label = ''
	        
	        # Loop through all 3 HITs
	        HIT_ans = []
	        for k in range(3):
	            HIT_ans.append(temp_df.iloc[k][input_cols[i]])
	        
	        if (HIT_ans.count('Yes') > 1):
	            label = 'Yes'
	        else:
	            label = 'No'
	            
	        pair = 
	        labels[(attr,adj)] = label

	## Create output 
	output_list = []
	for (k,v) in labels:
		output_list.append(k[0], k[1], v)

	return sorted(output_list, key=lambda tup: (tup[0],tup[1],tup[2]))
	# return a list of three-element tuples in the format (attr_id, adj, label) sorted alphabetically given the same column order.

def majority_vote_workers(mturk_res, votes):
    pass


# Part 1 - Weighted majority vote

def weighted_majority_vote_workers(mturk_res):
    pass

def weighted_majority_vote(mturk_res, workers):
    pass


# Part 2 - EM algorithm

def em_worker_quality(rows, labels):
    pass

def em_votes(rows, worker_qual):
    pass

def em_iteration(rows, worker_qual):
    labels = em_votes(rows, worker_qual)
    worker_qual = em_worker_quality(rows, labels)
    return labels, worker_qual

def em_vote(rows, iter_num):
    pass


# Part 3 - Qualified workers

def select_qualified_worker(mturk_res):
    pass


# Your main function

def main():
    # Read in CVS result file with pandas
    # PLEASE DO NOT CHANGE
    mturk_res = pd.read_csv('hw7_data.csv')

    # Call functions and output required CSV files
    pass

if __name__ == '__main__':
    main()
