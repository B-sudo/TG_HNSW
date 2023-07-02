#include <cassert>
#include <cmath>
#include <cstdio>
#include <iostream>
#include <cstdlib>
#include <cstring>
#include <chrono>

#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <fstream>

const char* input_base_file_path = "/home/liu3529/PASE/dataset/sift/sift_base.fvecs";
const char* input_query_file_path = "/home/liu3529/PASE/dataset/sift/sift_query.fvecs";
const char* output_rootnode = "/home/liu3529/TigerGraph/data/rootnode.csv";
const char* output_vecnode = "/home/liu3529/TigerGraph/data/vecnode.csv";
const char* output_branchnode = "/home/liu3529/TigerGraph/data/branchnode.csv";
size_t limit_size = 1000;
size_t query_limit_size = 10;

float* fvecs_read(const char* fname, size_t* d_out, size_t* n_out) {
    FILE* f = fopen(fname, "r");
    if (!f) {
        fprintf(stderr, "could not open %s\n", fname);
        perror("");
        abort();
    }
    int d;
    fread(&d, 1, sizeof(int), f);
    assert((d > 0 && d < 1000000) || !"unreasonable dimension");
    fseek(f, 0, SEEK_SET);
    struct stat st;
    fstat(fileno(f), &st);
    size_t sz = st.st_size;
    assert(sz % ((d + 1) * 4) == 0 || !"weird file size");
    size_t n = sz / ((d + 1) * 4);

    *d_out = d;
    *n_out = n;
    float* x = new float[n * (d + 1)];
    size_t nr = fread(x, sizeof(float), n * (d + 1), f);
    assert(nr == n * (d + 1) || !"could not read whole file");

    // shift array to remove row headers
    for (size_t i = 0; i < n; i++)
        memmove(x + i * d, x + 1 + i * (d + 1), d * sizeof(*x));

    fclose(f);
    return x;
}

int main() {
    float* x;
    float* xq;
    size_t dim;
    size_t n;
    size_t nq;

    std::ofstream roodnodeFile(output_rootnode);
    std::ofstream vecnodeFile(output_vecnode);
    std::ofstream branchnodeFile(output_branchnode);

    x = fvecs_read(input_base_file_path, &dim, &n);
    xq = fvecs_read(input_query_file_path, &dim, &nq);

    roodnodeFile << "id" << "," << "maxlevel" << "," << "dim"<< ","<< "base" << "," << "embedding" << "\n";
    //vecnodeFile << "id" << "," << "dim" << "," << "value" << "\n";
    //branchnodeFile << "RootNode_id" << "," << "VecNode_id" << ","<< "VecNode_dim" << "\n";

    /*for (size_t i = 0; i < dim; i++) {
        roodnodeFile << "," << "dim_" << i;
    }
    for (size_t i = dim; i < 1000; i++) {
        roodnodeFile << "," << "dim_" << i;
    }
    roodnodeFile << "\n";*/
    
    if (limit_size <= 0)
        limit_size = n;
    for (size_t i = 0; i < limit_size; i++) {
        roodnodeFile << i << "," << "-1" << ","<< dim << "," << "TRUE" << ",";
        for(size_t j = 0; j < dim - 1; j++) {
            //vecnodeFile << i << "," << j << "," << x[i*dim+j] << "\n";
            //branchnodeFile << i << "," << i << "," << j << "\n";
            roodnodeFile  << x[i*dim+j] << "#";
        }
        roodnodeFile  << x[i*dim+dim-1] << "\n";
    }

    if (query_limit_size <= 0)
        query_limit_size = nq;
    for (size_t i = limit_size; i < limit_size + query_limit_size; i++) {
        roodnodeFile << i << "," << "-1" << "," << dim << ","<< "FALSE" << ",";
        for(size_t j = 0; j < dim - 1; j++) {
            //vecnodeFile << i << "," << j << "," << x[i*dim+j] << "\n";
            //branchnodeFile << i << "," << i << "," << j << "\n";
            roodnodeFile  << xq[i*dim+j] << "#";
        }
        roodnodeFile  << xq[i*dim+dim-1] << "\n";
    }
    
    roodnodeFile.close();
    //vecnodeFile.close();
    //branchnodeFile.close();

    float distance = 0;
    auto start_time = std::chrono::high_resolution_clock::now();

    for (size_t j = 0; j < 100000000; j++){
        for (size_t i = 0; i < dim; i++){
            double diff = x[i] - x[3*dim+i];
            distance += diff * diff;
        }
        
    }
    

    auto end_time = std::chrono::high_resolution_clock::now();

    std::cout << "Distance is " << distance << std::endl;
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);

    std::cout << "Elapsed time: " << duration.count() << " milliseconds" << std::endl;
}
