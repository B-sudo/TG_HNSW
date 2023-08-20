import numpy as np
import faiss
import time
import os

def read_fvecs(input_file):
    fv = np.fromfile(input_file, dtype='int32')
    d = fv[0]
    return fv.reshape(-1, d + 1)[:, 1:].copy().view('float32')

if __name__ == "__main__":
    # read siftsmall
    '''
    file_dir = "/home/tigergraph/data/nsg/siftsmall/"
    input_files = ["siftsmall_base.fvecs", "siftsmall_groundtruth.ivecs", "siftsmall_learn.fvecs", "siftsmall_query.fvecs"]
    output_files = ["siftsmall_base.csv", "siftsmall_groundtruth.csv", "siftsmall_learn.csv", "siftsmall_query.csv"]
    '''

    # read sift
    file_dir = "/home/liu3529/Tigergraph/data/data/sift/"
    input_files = ["sift_base.fvecs", "sift_groundtruth.ivecs", "sift_learn.fvecs", "sift_query.fvecs"]
    output_files = ["sift_base.csv", "sift_groundtruth.csv", "sift_learn.csv", "sift_query.csv"]
    wb = read_fvecs(file_dir+input_files[0])
    xq = read_fvecs(file_dir+input_files[3])
    #xq = xq[0].reshape(1, xq.shape[1])
    print(xq.shape)
    print(wb.shape)
    print(xq)

    # nsg parameters
    d = 128
    k = 10
    M = 16

    index = faiss.IndexNSGFlat(d, M)
    index.nsg.search_L = 70

    # nsg construction
    start_time = time.time()
    index.add(wb)
    end_time = time.time()
    duration_ms = round((end_time - start_time) * 1000, 3)
    print("construction time:", duration_ms, "ms.")

    # nsg search
    start_time = time.time()
    D, I = index.search(xq, k)
    end_time = time.time()
    print(D)
    print(I)
    duration_ms = round((end_time - start_time) * 1000, 3)
    print("search time:", duration_ms, "ms.")

    xq = xq[0].reshape(1, xq.shape[1])
    print(xq.shape)

    print(faiss.omp_get_max_threads())
    faiss.omp_set_num_threads(1)
    print(faiss.omp_get_max_threads())
    start_time = time.time()
    D0, I0 = index.search(xq, k)
    end_time = time.time()
    print(D0)
    print(I0)
    duration_ms = round((end_time - start_time) * 1000, 3)
    print("single search time:", duration_ms, "ms.")
    faiss.omp_set_num_threads(112)
    print(faiss.omp_get_max_threads())
'''
    # write results to file
    dir="/home/liu3529/TigerGraph/data/nsg_load_from_faiss/nsg/"
    if not os.path.exists(dir):
        os.makedirs(dir)
    entry_point_file = open(dir + "entry_point.csv", "w")
    entry_point_file.write(str(index.nsg.entry_point) + "\n")
    entry_point_file.close()
    edges_file = open(dir + "edges.csv", "w")
    start_time = time.time()
    cum_nneighbor_per_level = faiss.vector_to_array(index.nsg.cum_nneighbor_per_level)
    levels = faiss.vector_to_array(index.nsg.levels)
    offsets = faiss.vector_to_array(index.nsg.offsets)
    neighbors = faiss.vector_to_array(index.nsg.neighbors)
    for level in range(1, index.nsg.max_level+2):
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

    
    print("len(cum_nneighbor_per_level)", len(cum_nneighbor_per_level))
    # print("levels", levels)
    print("len(levels)", len(levels))
    print("levels.dtype", levels.dtype)
    # print("offsets", offsets)
    print("len(offsets)", len(offsets))
    # print("neighbors", neighbors)
    print("len(neighbors)", len(neighbors))
    print("entry_point", index.nsg.entry_point)
    print("max_level", index.nsg.max_level)
    print("check_relative_distance", index.nsg.check_relative_distance)
    print("upper_beam", index.nsg.upper_beam)
    print("search_bounded_queue", index.nsg.search_bounded_queue)
    '''
