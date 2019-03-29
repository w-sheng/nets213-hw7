############################################################
# NETS 213: Homework 7
############################################################

import pandas as pd
import csv

# Part 1 - Majority vote

def majority_vote(mturk_res):
	## Retrieving relevant columns
	cols = ['Input.attr_id']
	input_cols = []
	ans_cols = []

	adj_string = 'Input.adj_'
	ans_string = 'Answer.adj_'

	for i in range(1,11):
	    cols.append(adj_string + str(i))
	    input_cols.append(adj_string + str(i))
	for i in range(1,11):
	    cols.append(ans_string + str(i))
	    ans_cols.append(ans_string + str(i))

	mturk_res = mturk_res[cols]

	## Creating majority label
	max_val = int(len(mturk_res.index) / 3)
	labels = {}

	# Loop through all attributes
	for i in range(1,max_val+1):
	    temp_df = mturk_res.iloc[(3*(i-1)):(3*i):, :]
	    attr = temp_df.iloc[0]['Input.attr_id']

	    # Loop through all 10 adjectives
	    for j in range(10):
	        adj = temp_df.iloc[0][input_cols[j]]
	        label = ''

	        # Loop through all 3 HITs
	        HIT_ans = []
	        for k in range(3):
	            HIT_ans.append(temp_df.iloc[k][ans_cols[j]])

	        if (HIT_ans.count('Yes') > 1):
	            label = 'Yes'
	        else:
	            label = 'No'

	        labels[(attr,adj)] = label

	## Create output 
	output_list = []
	for k in labels:
	    output_list.append((k[0], k[1], labels.get(k)))

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

	majority_labels = majority_vote(mturk_res)
	with open('output1.csv', 'w') as output1:
	    writer = csv.writer(output1)
	    writer.writerow(('attr_id', 'adj', 'label'))
	    writer.writerows(majority_labels)

	output1.close()
	# Call functions and output required CSV files
	pass

if __name__ == '__main__':
    main()
