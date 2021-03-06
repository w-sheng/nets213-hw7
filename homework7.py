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
    qualities = {};
    num_count_workers = {};
    num_correct_workers = {};
    adj_string = 'Input.adj_'
    ans_string = 'Answer.adj_'
    cols = ['Input.attr_id', 'WorkerId']
    input_cols = []
    ans_cols = []

    for i in range(1,11):
    	cols.append(adj_string + str(i))
    	input_cols.append(adj_string + str(i))
    for i in range(1,11):
    	cols.append(ans_string + str(i))
    	ans_cols.append(ans_string + str(i))

    mturk_res = mturk_res[cols]
    max_val = int(len(mturk_res.index) / 3)

	# Loop through all attributes
    for i in range(1,max_val+1):
	    temp_df = mturk_res.iloc[i]
	    attr = temp_df['Input.attr_id']

	    ans_df = mturk_res.iloc[(3*(i-1)):(3*i):, :]

	    # Loop through all 10 adjectives
	    for j in range(10):
	        adj = temp_df[input_cols[j]]


	        label = ''
	        # Loop through all 3 HITs
	        HIT_ans = []
	        for k in range(3):
	            HIT_ans.append(ans_df.iloc[k][ans_cols[j]])

	        if (HIT_ans.count('Yes') > 1):
	            label = 'Yes'
	        else:
	            label = 'No' 


	        worker_id = temp_df['WorkerId'];
	        if (worker_id in num_count_workers):
	        	num_count_workers[worker_id] = num_count_workers[worker_id] +1;
	        else:
	        	num_count_workers[worker_id] = 1;
	        
	        if label == temp_df[ans_cols[j]]:
	        	if worker_id in num_correct_workers:
	        		num_correct_workers[worker_id] = num_correct_workers[worker_id] +1;

	        	
	        	else:
	        		num_correct_workers[worker_id] = 1;

    for (key, val) in num_correct_workers.items():
    	qualities[key] = round(val/num_count_workers[key], 3);

    output_list = []

    for key, value in qualities.items():
    	output_list.append((key, value))

    return sorted(output_list, key=lambda tup: (tup[0],tup[1]))


# Part 1 - Weighted majority vote

def weighted_majority_vote_workers(mturk_res):
    qualities = {};
    num_count_workers = {};
    num_correct_workers = {};
    adj_string = 'Input.pos_qual_ctrl_'
    ans_string = 'Answer.pos_qual_ctrl_'
    cols = ['Input.attr_id', 'WorkerId']
    input_cols = []
    ans_cols = []


    for i in range(1,6):
    	cols.append(adj_string + str(i))
    	input_cols.append(adj_string + str(i))
    for i in range(1,6):
    	cols.append(ans_string + str(i))
    	ans_cols.append(ans_string + str(i))

    mturk_res = mturk_res[cols]
    max_val = int(len(mturk_res.index) / 3)

	# Loop through all attributes
    for i in range(1,max_val+1):
	    temp_df = mturk_res.iloc[i]
	    attr = temp_df['Input.attr_id']
	    ans_df = mturk_res.iloc[(3*(i-1)):(3*i):, :]

	    # Loop through all 5 gold standard pairs
	    for j in range(5):
	        
	    	label = 'Yes'
	    	worker_id = temp_df['WorkerId'];

	    	#keep track of number of hits each worker keep
	    	if (worker_id in num_count_workers):
	    		num_count_workers[worker_id] = num_count_workers[worker_id] +1;
	    	else:
	    		num_count_workers[worker_id] = 1;
	    	
	    	#keep track of the number of correct answer each worker has
	    	if label == temp_df[ans_cols[j]]:
	        	if worker_id in num_correct_workers:
	        		num_correct_workers[worker_id] = num_correct_workers[worker_id] +1;
	        	else:
	        		num_correct_workers[worker_id] = 1;

	    	else:
	       		if worker_id not in num_correct_workers:
	        		num_correct_workers[worker_id] = 0

	        

    for (key, val) in num_correct_workers.items():
    	qualities[key] = round(val/num_count_workers[key], 3);

    output_list = []

    for key, value in qualities.items():
    	output_list.append((key, value))

    return sorted(output_list, key=lambda tup: (tup[0],tup[1]))

def weighted_majority_vote(mturk_res, workers):
    dict_workers_quality = dict(workers);
    adj_string = 'Input.adj_'
    ans_string = 'Answer.adj_'
    cols = ['Input.attr_id', 'WorkerId']
    input_cols = []
    ans_cols = []
    votes = {}; #key is (adj, atr, yes/no), value = points
    attr_adj_dict = {};

    for i in range(1,11):
    	cols.append(adj_string + str(i))
    	input_cols.append(adj_string + str(i))
    for i in range(1,11):
    	cols.append(ans_string + str(i))
    	ans_cols.append(ans_string + str(i))

    mturk_res = mturk_res[cols]
    max_val = int(len(mturk_res.index) / 3)

	# Loop through all attributes
    for i in range(1,max_val+1):
	    temp_df = mturk_res.iloc[i];
	    attr = temp_df['Input.attr_id'];
	    worker_id = temp_df['WorkerId'];
	    worker_qual= dict_workers_quality[worker_id];

	    # Loop through all 10 adjectives
	    for j in range(10):
	    	adj = temp_df[input_cols[j]]
	    	worker_ans = temp_df[ans_cols[j]];
	    	tup = (attr, adj, worker_ans)

	    	if tup in votes:
	    		votes[tup] = votes[tup] + worker_qual
	    	else:
	    		votes[tup] = worker_qual;

	    	if (attr, adj) not in attr_adj_dict:
	        	attr_adj_dict[(attr, adj)] = 'No'


    
    for (key, val) in attr_adj_dict.items():
    	yes_vote = 0
    	if (key[0], key[1], 'Yes') in votes:
    		yes_vote = votes[key[0], key[1], 'Yes'];

    	no_vote = 0;
    	if ((key[0], key[1], 'No') in votes):
    		no_vote = votes[key[0], key[1], 'No'];

    	if yes_vote > no_vote:
    		attr_adj_dict[key] = 'Yes';
    	else:
    		attr_adj_dict[key] = 'No';

    output_list = []

    for key, value in attr_adj_dict.items():
    	output_list.append((key[0], key[1], value))

    return sorted(output_list, key=lambda tup: (tup[0],tup[1]))


# Part 2 - EM algorithm

def em_worker_quality(rows, labels):
	k = len(rows)
	n = len(rows[0])
	worker_qual = []

	for i in range(k):
		correct = 0
		for j in range(n):
			if rows[i][j] == labels[j]:
				correct += 1

		worker_qual.append(correct/n)

	return worker_qual

def em_votes(rows, worker_qual):
	k = len(rows)
	n = len(rows[0])
	labels = []

	for i in range(n):
		porn = 0
		notporn = 0

		for j in range(k):
			quality = worker_qual[j]

			if rows[j][i] == 'porn':
				porn += quality
			else:
				notporn += quality

		if porn > notporn:
			labels.append('porn')
		else:
			labels.append('notporn')

	return labels

def em_iteration(rows, worker_qual):
	labels = em_votes(rows, worker_qual)
	worker_qual = em_worker_quality(rows, labels)
	return labels, worker_qual

def em_vote(rows, iter_num):
	# get URLs and make labels matrix
	urlrow = rows[0]
	label_matrix = rows[1:]
	for r in label_matrix:
		r.pop(0)

	k = len(label_matrix)
	n = len(label_matrix[0])
	labels = []
	worker_qual = [1] * k

	# Majority vote
	for i in range(n):
		label = ''
		worker_ans = []
		for j in range(k):
		    worker_ans.append(label_matrix[j][i]) 
		if (worker_ans.count('porn') > (len(worker_ans)/2)):
			label = 'porn'
		else:
			label = 'notporn'
		labels.append(label)

	# Iterate EM
	for i in range(iter_num):
		(labels, worker_qual) = em_iteration(label_matrix, worker_qual)

	# Get tuple output
	output = []
	for i in range(len(labels)):
		output.append((urlrow[i],labels[i]))

	return sorted(output, key=lambda tup: (tup[0],tup[1]))


# Part 3 - Qualified workers

def select_qualified_worker(mturk_res):
    num_count_workers = {};
    adj_string = 'Input.pos_qual_ctrl_'
    ans_string = 'Answer.pos_qual_ctrl_'
    cols = ['Input.attr_id', 'WorkerId', 'Answer.neg_qual_ctrl']
    input_cols = []
    ans_cols = []


    for i in range(1,6):
    	cols.append(adj_string + str(i))
    	input_cols.append(adj_string + str(i))
    for i in range(1,6):
    	cols.append(ans_string + str(i))
    	ans_cols.append(ans_string + str(i))

    mturk_res = mturk_res[cols]
    max_val = int(len(mturk_res .index) / 3)

	# Loop through all attributes
    for i in range(1,max_val+1):
	    temp_df = mturk_res.iloc[i]
	    attr = temp_df['Input.attr_id']

	    worker_id = temp_df['WorkerId'];

	    if (worker_id in num_count_workers):
	       	num_count_workers[worker_id] = num_count_workers[worker_id] +1;
	    else:
	       	num_count_workers[worker_id] = 1;

    workers_5hits = [];
	#getting workers with 5+ hits
    for (key, value) in num_count_workers.items():
    	if value >= 5:
    		workers_5hits.append(key);


 
    num_criteria_met_workers = {};
 
	# Loop through all attributes
    for i in range(1,max_val+1):
	    temp_df = mturk_res.iloc[i]
	    attr = temp_df['Input.attr_id']
	    worker_id = temp_df['WorkerId'];

	    if (worker_id in workers_5hits):
		    
		    num_correct_pos = 0;
		    for j in range(5):		  	
		    	label = 'Yes'
		    	if label == temp_df[ans_cols[j]]:
		        	num_correct_pos+=1;

		    if ('No' == temp_df['Answer.neg_qual_ctrl']) or ('Naa' == temp_df['Answer.neg_qual_ctrl']):
		    	if num_correct_pos >= 4:
		    		if worker_id in num_criteria_met_workers:
		    			num_criteria_met_workers[worker_id] = num_criteria_met_workers[worker_id] + 1;
		    		else:
		    			num_criteria_met_workers[worker_id] = 1


		    if worker_id not in num_criteria_met_workers:
		    	num_criteria_met_workers[worker_id] = 0;



    worker_percent_dict = {};
    for worker in workers_5hits:
    	percent = round(num_criteria_met_workers[worker]/num_count_workers[worker], 3);
    	if percent >= .750:
    		worker_percent_dict[worker] = percent
    return worker_percent_dict;




	        
# Your main function

def main():
	# Read in CVS result file with pandas
	# PLEASE DO NOT CHANGE
	mturk_res = pd.read_csv('hw7_data.csv')

	## PART 1: Aggregation Methods
	majority_labels = majority_vote(mturk_res)
	with open('output1.csv', 'w') as output1:
	    writer = csv.writer(output1)
	    writer.writerow(('attr_id', 'adj', 'label'))
	    writer.writerows(majority_labels)

	output1.close()

	majority_vote_workers_res = majority_vote_workers(mturk_res, majority_labels);
	with open('output2.csv', 'w') as output2:
	    writer = csv.writer(output2)
	    writer.writerow(('worker_id', 'quality'))
	    writer.writerows(majority_vote_workers_res)

	output2.close()


	weighted_majority_vote_workers_res = weighted_majority_vote_workers(mturk_res);
	with open('output3.csv', 'w') as output3:
	    writer = csv.writer(output3)
	    writer.writerow(('worker_id', 'quality'))
	    writer.writerows(weighted_majority_vote_workers_res)

	output3.close()

	weighted_majority_vote_res = weighted_majority_vote(mturk_res,weighted_majority_vote_workers_res);
	with open('output4.csv', 'w') as output4:
	    writer = csv.writer(output4)
	    writer.writerow(('attr_id', 'adj', 'label'))
	    writer.writerows(weighted_majority_vote_res)

	output4.close()

	## PART 2: EM Algorithm
	# Import EM toy data
	lines = []
	with open('em_toy_data.txt', 'r') as input:
	    for line in input:
	        lines.append(line)
	
	# Create rows 2d array
	# First row is list of URLs
	# Row k = labels given by worker k
	# Column n = label assigned to url n
	rows = [[0]*5]*6
	for i in range(5):
		worker_labels = []
	    for l in lines[(i*5):(i+1)*5]:
	        label = l.split()[2]
	        worker_labels.append(label)
	    rows[i+1] = worker_labels
	urls = []
	for l in lines[:5]:
		urls.append(l.split()[1])
	rows[0] = urls
	
	# Call EM algorithm for 3 iterations
	em = em_vote(rows, 3)
	
	# Write output
	with open('output5.csv', 'w') as output5:
	    writer = csv.writer(output5)
	    writer.writerow(('url', 'label'))
	    writer.writerows(em)

	output5.close()

	## PART 3: Qualified Workers
	select_qualified_worker_res = select_qualified_worker(mturk_res);
	with open('output6.csv', 'w') as output6:
	    writer = csv.writer(output6)
	    writer.writerow(('worker_id', 'percentage'))
	    writer.writerows(select_qualified_worker_res)

	output6.close()


	# Call functions and output required CSV files
	pass

if __name__ == '__main__':
    main()
