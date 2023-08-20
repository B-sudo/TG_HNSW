import numpy as np
import faiss
import time
import os

def read_fvecs(input_file):
    fv = np.fromfile(input_file, dtype='int32')
    d = fv[0]
    return fv.reshape(-1, d + 1)[:, 1:].copy().view('float32')

def read_bvecs(input_file):
    fv = np.memmap(input_file, dtype='uint8', mode='r')
    d = fv[:4].view('int32')[0]
    return fv.reshape(-1, d + 4)[:, 4:].copy().view('uint8').astype(np.float32)

def read_bvecs_head(input_file, head_line_number):
    fv = np.memmap(input_file, dtype='uint8', mode='r')
    d = fv[:4].view('int32')[0]
    return fv.reshape(-1, d + 4)[:head_line_number, 4:].copy().view('uint8').astype(np.float32)

if __name__ == "__main__":
    # read sift100M
    file_dir = "/home/liu3529/Tigergraph/data/data/sift100M/"
    input_files = ["bigann_base.bvecs", "bigann_query.bvecs"]
    head_line_number = 100000000
    xq = read_bvecs(file_dir+input_files[1])
    xq0 = xq[0].reshape(1, xq.shape[1])
    print(xq.shape)
    print(xq)
    wb = read_bvecs_head(file_dir+input_files[0], head_line_number)
    print(wb.shape)

    # HNSW parameters
    d = 128
    k = 10
    M = 16
    ef_search = 180
    ef_construction = 64

    index = faiss.IndexHNSWFlat(d, M)
    index.hnsw.efSearch = ef_search
    index.hnsw.efConstruction = ef_construction

    groundtruth_file = "/home/liu3529/Tigergraph/data/data/sift100M/bigann_groundtruth.csv"
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

    # HNSW construction
    start_time = time.time()
    index.add(wb)
    end_time = time.time()
    duration_ms = round((end_time - start_time) * 1000, 3)
    print("construction time:", duration_ms, "ms.")

    ef_list = []
    batch_search_time = []
    single_search_time = []
    recall_list = []


    for ef in range(10,480,20):
        index.hnsw.efSearch = ef
        ef_list.append(ef)
        # HNSW search
        start_time = time.time()
        D, I = index.search(xq, k)
        end_time = time.time()
        print(D)
        print(I)
        duration_ms = round((end_time - start_time) * 1000, 3)
        batch_search_time.append(duration_ms)
        print("search time:", duration_ms, "ms.")

        print(xq0.shape)

        print(faiss.omp_get_max_threads())
        faiss.omp_set_num_threads(1)
        print(faiss.omp_get_max_threads())
        start_time = time.time()
        D0, I0 = index.search(xq0, k)
        end_time = time.time()
        print(D0)
        print(I0)
        duration_ms = round((end_time - start_time) * 1000, 3)
        single_search_time.append(duration_ms)
        print("single search time:", duration_ms, "ms.")
        faiss.omp_set_num_threads(112)
        print(faiss.omp_get_max_threads())
        # HNSW recall

        true_positive = 0

        for i in range(0,10000):
            for result in I[i]:
                if str(result) in groundtruth[i]:
                    true_positive += 1
        recall = true_positive / 10000 / k
        recall_list.append(round(recall*100, 3))
        print(f"recall = {recall*100:.3f}%")

    print("ef list is ")
    print(ef_list)
    print("batch search time is ")
    print(batch_search_time)
    print("single search time")
    print(single_search_time)
    print("recall list is ")
    print(recall_list)

'''
    # write results to file
    dir="/home/liu3529/TigerGraph/data/hnsw/hnsw/sift100m/"
    if not os.path.exists(dir):
        os.makedirs(dir)
    entry_point_file = open(dir + "entry_point.csv", "w")
    entry_point_file.write(str(index.hnsw.entry_point) + "\n")
    entry_point_file.close()
    edges_file = open(dir + "edges.csv", "w")
    start_time = time.time()
    cum_nneighbor_per_level = faiss.vector_to_array(index.hnsw.cum_nneighbor_per_level)
    levels = faiss.vector_to_array(index.hnsw.levels)
    offsets = faiss.vector_to_array(index.hnsw.offsets)
    neighbors = faiss.vector_to_array(index.hnsw.neighbors)
    for level in range(1, index.hnsw.max_level+2):
        start = cum_nneighbor_per_level[level-1]
        end = cum_nneighbor_per_level[level]
        for node in range(len(levels)):
            node_level = levels[node]
            if level <= node_level:
                offset = np.int64(offsets[node])
                target_arr = neighbors[offset + start: offset + end]
                target_arr = target_arr[target_arr >= 0]
                for target in target_arr:
                    edges_file.write(str(node) + "," + str(target) + "," + str(level) + "\n")
    end_time = time.time()
    duration_ms = round((end_time - start_time) * 1000, 3)
    edges_file.close()
    print("file writing time:", duration_ms, "ms.")
'''