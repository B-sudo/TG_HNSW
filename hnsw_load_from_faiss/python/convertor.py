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
    print(df.shape)

if __name__ == "__main__":
    # convert siftsmall
    file_dir = "/home/tigergraph/data/hnsw/siftsmall/"
    input_files = ["siftsmall_base.fvecs", "siftsmall_groundtruth.ivecs", "siftsmall_learn.fvecs", "siftsmall_query.fvecs"]
    output_files = ["siftsmall_base.csv", "siftsmall_groundtruth.csv", "siftsmall_learn.csv", "siftsmall_query.csv"]
    for i in range(4):
        file_type = input_files[i].split(".")[1]
        convert_vecs_file(file_dir+input_files[i], file_dir+output_files[i], file_type)

    # convert sift
    file_dir = "/home/tigergraph/data/hnsw/sift/"
    input_files = ["sift_base.fvecs", "sift_groundtruth.ivecs", "sift_learn.fvecs", "sift_query.fvecs"]
    output_files = ["sift_base.csv", "sift_groundtruth.csv", "sift_learn.csv", "sift_query.csv"]
    for i in range(4):
        file_type = input_files[i].split(".")[1]
        convert_vecs_file(file_dir+input_files[i], file_dir+output_files[i], file_type)

