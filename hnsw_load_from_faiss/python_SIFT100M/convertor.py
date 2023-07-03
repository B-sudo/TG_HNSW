import numpy as np
import pandas as pd

def convert_vecs_file(input_file, output_file, file_type="fvecs"):
    if file_type == "fvecs":
        fv = np.fromfile(input_file, dtype=np.float32)
    elif file_type == "ivecs":
        fv = np.fromfile(input_file, dtype=np.int32)
    else:
        return
    if fv.size == 0:
        return np.zeros((0, 0))
    dim = fv.view(np.int32)[0]
    assert dim > 0
    fv = fv.reshape(-1, 1 + dim)
    if not all(fv.view(np.int32)[:, 0] == dim):
        raise IOError("Non-uniform vector sizes in " + filename)
    fv = fv[:, 1:]
    # np.savetxt(output_file+".tmp", fv, delimiter=",")
    df = pd.DataFrame(fv)
    df.to_csv(output_file, index=True, header=False)
    print(input_file, df.shape)

def mmap_bvecs(fname, output_file):
    x = np.memmap(fname, dtype='uint8', mode='r')
    d = x[:4].view('int32')[0]
    fv = x.reshape(-1, d + 4)[:, 4:]
    df = pd.DataFrame(fv)
    df.to_csv(output_file, index=True, header=False)
    print(fname, df.shape)

def mmap_bvecs_head(fname, output_file, head_line_number):
    x = np.memmap(fname, dtype='uint8', mode='r')
    d = x[:4].view('int32')[0]
    fv = x.reshape(-1, d + 4)[:head_line_number, 4:]
    df = pd.DataFrame(fv)
    df.to_csv(output_file, index=True, header=False)
    print(fname, df.shape)

if __name__ == "__main__":
    # convert sift100M
    file_dir = "/home/tigergraph/data/hnsw/sift100M/"
    input_files = ["bigann_base.bvecs", "gnd/idx_100M.ivecs", "bigann_learn.bvecs", "bigann_query.bvecs"]
    output_files = ["bigann_base.csv", "bigann_groundtruth.csv", "bigann_learn.csv", "bigann_query.csv"]
    head_line_number = 100000000
    for i in range(4):
        if i == 2:
            continue
        file_type = input_files[i].split(".")[1]
        input_file = file_dir+input_files[i]
        output_file = file_dir+output_files[i]
        if file_type == "fvecs" or file_type == "ivecs":
            convert_vecs_file(input_file, output_file, file_type)
        elif file_type == "bvecs":
            if i == 0:
                mmap_bvecs_head(input_file, output_file, head_line_number)
            else:
                mmap_bvecs(input_file, output_file)
