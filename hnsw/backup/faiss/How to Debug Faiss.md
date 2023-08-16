How to Debug Faiss?
# install package
## install BLAS, LAPACK, swig, python3
link: https://installati.one/centos/7/blas-devel/
```
sudo yum makecache
sudo yum -y install blas-devel
sudo yum -y install lapack-devel
sudo yum -y install swig
```
## install python3
```
sudo yum -y install python3
sudo ln -sf /usr/bin/python3 /usr/bin/python
```
## install g++, make and openssl
```
sudo yum -y install gcc-c++
sudo yum -y install make
sudo yum -y install openssl-devel
```

## install CMaker - takes a long time, around half an hour
link: https://orcacore.com/install-use-cmake-centos-7/
```
wget https://github.com/Kitware/CMake/releases/download/v3.22.3/cmake-3.22.3.tar.gz
tar -zxvf cmake-3.22.3.tar.gz
cd cmake-3.22.3
./bootstrap
make
sudo make install
cmake --version
```

# download the source code
```
[tigergraph ~] $ git clone https://github.com/facebookresearch/faiss.git
[tigergraph ~] $ cd faiss/
```

# build from source
link: https://github.com/facebookresearch/faiss/blob/main/INSTALL.md

```

```