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
    head_line_number = 1000000
    xq = read_bvecs(file_dir+input_files[1])
    #xq = xq[0].reshape(1, xq.shape[1])
    print(xq.shape)
    print(xq)
    wb = read_bvecs_head(file_dir+input_files[0], head_line_number)
    print(wb.shape)

    # nsg parameters
    d = 128
    k = 10
    M = 16

    index = faiss.IndexNSGFlat(d, M)
    index.nsg.search_L = 32

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

    # write results to file
    dir="/home/liu3529/TigerGraph/data/nsg/nsg/sift100m/"
    if not os.path.exists(dir):
        os.makedirs(dir)
    entry_point_file = open(dir + "entry_point.csv", "w")
    entry_point_file.write(str(index.nsg.enterpoint) + "\n")
    entry_point_file.close()
    edges_file = open(dir + "edges.csv", "w")
    start_time = time.time()
    
    N = index.nsg.final_graph.N
    K = index.nsg.final_graph.K

    for i in range(N):
        for j in range(K):
            if index.nsg.final_graph.at(i, j) != -1:
                edges_file.write(str(i) + "," + str(index.nsg.final_graph.at(i, j)) + "\n")
    end_time = time.time()
    duration_ms = round((end_time - start_time) * 1000, 3)
    edges_file.close()
    print("file writing time:", duration_ms, "ms.")
