import requests
from threading import Thread
import time
import os
import re

def request_get(url, input):
    r = requests.get(url + input)
    data = r.json()
    return data['results']

def process_id_range(id_range, url, input_list, store=None):
    if store is None:
        store = {}
    for i in range(len(id_range)):
        id = id_range[i]
        store[id] = request_get(url, input_list[i])
    return store

def threaded_process(n_thread, id_range, url, input_list):
    store = {}
    threads = []
    for i in range(n_thread):
        ids = id_range[i::n_thread]
        inputs = input_list[i::n_thread]
        t = Thread(target=process_id_range, args=(ids, url, inputs, store))
        threads.append(t)
    [ t.start() for t in threads ]
    [ t.join() for t in threads ]
    return store

ef_list = []
batch_search_time = []
single_search_time = []
recall_list = []

def main(k=10, ef_search=32):
    url = "http://127.0.0.1:14240/restpp/query/HNSW/q2_search_mod?k=" + str(k) + "&ef_search=" + str(ef_search) + "&input="
    query_file = "/home/liu3529/Tigergraph/data/data/sift/sift_query.csv"
    groundtruth_file = "/home/liu3529/Tigergraph/data/data/sift/sift_groundtruth.csv"
    n_thread = 32

    ef_list.append(ef_search)

    # 1. query file parsing
    start_time = time.time()
    id_list = []
    input_list = []
    with open(query_file) as f:
        lines = f.read().splitlines()
    # lines = lines[:4]
    for line in lines:
        splited_line = line.split(",", 1)
        id_list.append(int(splited_line[0]))
        input_list.append(splited_line[1])
    end_time = time.time()
    duration_ms = round((end_time - start_time) * 1000, 3)
    print("query file parsing time:", duration_ms, "ms.")

    # 2. call the resful API in parallel
    start_time = time.time()
    results = threaded_process(n_thread, id_list, url, input_list)
    end_time = time.time()
    duration_ms = round((end_time - start_time) * 1000, 3)
    print("restful API calling time:", duration_ms, "ms.")

    # 3. groundtruth file parsing
    start_time = time.time()
    with open(groundtruth_file) as f:
        lines = f.read().splitlines()
    # lines = lines[:4]
    groundtruth = {}
    end_col = k + 1
    for line in lines:
        splited_line = line.split(",", end_col)
        groundtruth[int(splited_line[0])] = splited_line[1: end_col]
    end_time = time.time()
    duration_ms = round((end_time - start_time) * 1000, 3)
    print("groundtruth file parsing time:", duration_ms, "ms.")

    # 4. calculate the recall 
    start_time = time.time()
    true_positive = 0
    hop_num = 0
    visited_nodes_num = 0
    hop_num_greedy = 0
    visited_nodes_num_greedy = 0
    hop_num_0 = 0
    visited_nodes_num_0 = 0
    for id in id_list:
        min_heap = results[id][0]["@@min_heap"]
        hop_num += results[id][1]["@@hop_num"]
        visited_nodes_num += results[id][2]["@@visited_nodes_num"]
        hop_num_greedy += results[id][3]["@@hop_num_greedy"]
        hop_num_0 += results[id][4]["@@hop_num_0"]
        visited_nodes_num_greedy += results[id][5]["@@visited_nodes_num_greedy"]
        visited_nodes_num_0 += results[id][6]["@@visited_nodes_num_0"]
        for item in min_heap:
            if item["element"] in groundtruth[id]:
                true_positive += 1
    recall = true_positive / len(id_list) / k
    avg_hop_num = hop_num / len(id_list)
    avg_visited_nodes_num = visited_nodes_num/ len(id_list)
    avg_hop_num_greedy = hop_num_greedy / len(id_list)
    avg_visited_nodes_num_greedy = visited_nodes_num_greedy/ len(id_list)
    avg_hop_num_0 = hop_num_0 / len(id_list)
    avg_visited_nodes_num_0 = visited_nodes_num_0/ len(id_list)
    end_time = time.time()
    duration_ms = round((end_time - start_time) * 1000, 3)
    recall_list.append(round(recall*100, 3))
    print("recall calculation time:", duration_ms, "ms.")
    print(f"recall = {recall*100:.3f}%")
    print(f"hop_num = {avg_hop_num:.3f}")
    print(f"visited_nodes_num = {avg_visited_nodes_num:.3f}")
    print(f"hop_num_greedy = {avg_hop_num_greedy:.3f}")
    print(f"visited_nodes_num_greedy= {avg_visited_nodes_num_greedy:.3f}")
    print(f"hop_num_0 = {avg_hop_num_0:.3f}")
    print(f"visited_nodes_num_0 = {avg_visited_nodes_num_0:.3f}")

    command = 'curl -H "GSQL-TIMEOUT: 3600000" "http://127.0.0.1:14240/restpp/query/HNSW/q2_search_batch?input_file="/home/tigergraph/mydata/data/sift/sift_query_parse.csv"&output_file="/home/tigergraph/mydata/hnsw/hnsw/sift/result.csv"' + '&ef_search=' + str(ef_search) + '"'

    # Run the command and capture the output using os.popen()
    time_output = os.popen(f"/usr/bin/time -p {command} 2>&1").read()
    print(time_output)

    # Extract the real time value using regular expression
    real_time_match = re.search(r'real\s+(\d+\.\d+)', time_output)
    if real_time_match:
        real_time = float(real_time_match.group(1))
        batch_search_time.append(real_time)
    else:
        print("Failed to extract real time value.")

    print("Batch Real times:", real_time )

    command = 'curl -H "GSQL-TIMEOUT: 3600000" "http://127.0.0.1:14240/restpp/query/HNSW/q2_search_mod?input=1.0,3.0,11.0,110.0,62.0,22.0,4.0,0.0,43.0,21.0,22.0,18.0,6.0,28.0,64.0,9.0,11.0,1.0,0.0,0.0,1.0,40.0,101.0,21.0,20.0,2.0,4.0,2.0,2.0,9.0,18.0,35.0,1.0,1.0,7.0,25.0,108.0,116.0,63.0,2.0,0.0,0.0,11.0,74.0,40.0,101.0,116.0,3.0,33.0,1.0,1.0,11.0,14.0,18.0,116.0,116.0,68.0,12.0,5.0,4.0,2.0,2.0,9.0,102.0,17.0,3.0,10.0,18.0,8.0,15.0,67.0,63.0,15.0,0.0,14.0,116.0,80.0,0.0,2.0,22.0,96.0,37.0,28.0,88.0,43.0,1.0,4.0,18.0,116.0,51.0,5.0,11.0,32.0,14.0,8.0,23.0,44.0,17.0,12.0,9.0,0.0,0.0,19.0,37.0,85.0,18.0,16.0,104.0,22.0,6.0,2.0,26.0,12.0,58.0,67.0,82.0,25.0,12.0,2.0,2.0,25.0,18.0,8.0,2.0,19.0,42.0,48.0,11.0&k=10'  + '&ef_search=' + str(ef_search) + '"'
    # Run the command and capture the output using os.popen()
    time_output = os.popen(f"/usr/bin/time -p {command} 2>&1").read()
    print(time_output)

    # Extract the real time value using regular expression
    real_time_match = re.search(r'real\s+(\d+\.\d+)', time_output)
    if real_time_match:
        real_time = float(real_time_match.group(1))
        single_search_time.append(real_time)
    else:
        print("Failed to extract real time value.")

    print("Single Real times:", real_time )

if __name__ == "__main__":
    '''
    k_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    ef_search_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for k in k_list:
        for ef_search in ef_search_list:
            if ef_search >= k:
                print(k, ef_search)'''
    for ef in range(10,250,10):            
        main(10, ef)
        
    print("ef list is ")
    print(ef_list)
    print("batch search time is ")
    print(batch_search_time)
    print("single search time")
    print(single_search_time)
    print("recall list is ")
    print(recall_list)








