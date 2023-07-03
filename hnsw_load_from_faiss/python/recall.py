import requests
from threading import Thread
import time

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

def main(k=10, ef_search=32):
    url = "http://127.0.0.1:14240/restpp/query/HNSW/q1_search?k=" + str(k) + "&ef_search=" + str(ef_search) + "&input="
    query_file = "/home/tigergraph/data/hnsw/sift/sift_query.csv"
    groundtruth_file = "/home/tigergraph/data/hnsw/sift/sift_groundtruth.csv"
    n_thread = 32

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
    for id in id_list:
        min_heap = results[id][0]["@@min_heap"]
        for item in min_heap:
            if item["element"] in groundtruth[id]:
                true_positive += 1
    recall = true_positive / len(id_list) / k
    end_time = time.time()
    duration_ms = round((end_time - start_time) * 1000, 3)
    print("recall calculation time:", duration_ms, "ms.")
    print(f"recall = {recall*100:.3f}%")

if __name__ == "__main__":
    k_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    ef_search_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for k in k_list:
        for ef_search in ef_search_list:
            if ef_search >= k:
                print(k, ef_search)
                main(k, ef_search)

