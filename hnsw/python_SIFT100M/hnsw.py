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
    file_dir = "/home/liu3529/TigerGraph/data/data/sift100M/"
    input_files = ["bigann_base.bvecs", "bigann_query.bvecs"]
    head_line_number = 100000000
    xq = read_bvecs(file_dir+input_files[1])
    #xq = xq[0].reshape(1, xq.shape[1])
    print(xq.shape)
    print(xq)
    wb = read_bvecs_head(file_dir+input_files[0], head_line_number)
    print(wb.shape)

    # HNSW parameters
    d = 128
    k = 10
    M = 16
    ef_search = 32
    ef_construction = 64

    index = faiss.IndexHNSWFlat(d, M)
    index.hnsw.efSearch = ef_search
    index.hnsw.efConstruction = ef_construction

    # HNSW construction
    start_time = time.time()
    index.add(wb)
    end_time = time.time()
    duration_ms = round((end_time - start_time) * 1000, 3)
    print("construction time:", duration_ms, "ms.")

    # HNSW search
    start_time = time.time()
    D, I = index.search(xq, k)
    end_time = time.time()
    print(D)
    print(I)
    duration_ms = round((end_time - start_time) * 1000, 3)
    print("search time:", duration_ms, "ms.")

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
