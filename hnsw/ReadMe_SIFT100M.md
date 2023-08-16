# 1. Dowload dataset
## 1.1 Dowload dataset from http://corpus-texmex.irisa.fr/
```
[tigergraph ~] $ mkdir -p /home/tigergraph/data/hnsw
[tigergraph ~] $ cd /home/tigergraph/data/hnsw
[tigergraph hnsw] $ mkdir sift100M
[tigergraph hnsw] $ cd sift100M/
[tigergraph sift100M] $ wget ftp://ftp.irisa.fr/local/texmex/corpus/bigann_query.bvecs.gz
--2022-08-04 06:35:21--  ftp://ftp.irisa.fr/local/texmex/corpus/bigann_query.bvecs.gz
           => ‘bigann_query.bvecs.gz’
Resolving ftp.irisa.fr (ftp.irisa.fr)... 131.254.254.45, 2001:660:7303:254::45
Connecting to ftp.irisa.fr (ftp.irisa.fr)|131.254.254.45|:21... connected.
Logging in as anonymous ... Logged in!
==> SYST ... done.    ==> PWD ... done.
==> TYPE I ... done.  ==> CWD (1) /local/texmex/corpus ... done.
==> SIZE bigann_query.bvecs.gz ... 986411
==> PASV ... done.    ==> RETR bigann_query.bvecs.gz ... done.
Length: 986411 (963K) (unauthoritative)

100%[======================================================================================================>] 986,411     1.32MB/s   in 0.7s

2022-08-04 06:35:24 (1.32 MB/s) - ‘bigann_query.bvecs.gz’ saved [986411]

[tigergraph sift100M] $ wget ftp://ftp.irisa.fr/local/texmex/corpus/bigann_gnd.tar.gz
--2022-08-04 06:35:32--  ftp://ftp.irisa.fr/local/texmex/corpus/bigann_gnd.tar.gz
           => ‘bigann_gnd.tar.gz’
Resolving ftp.irisa.fr (ftp.irisa.fr)... 131.254.254.45, 2001:660:7303:254::45
Connecting to ftp.irisa.fr (ftp.irisa.fr)|131.254.254.45|:21... connected.
Logging in as anonymous ... Logged in!
==> SYST ... done.    ==> PWD ... done.
==> TYPE I ... done.  ==> CWD (1) /local/texmex/corpus ... done.
==> SIZE bigann_gnd.tar.gz ... 536740006
==> PASV ... done.    ==> RETR bigann_gnd.tar.gz ... done.
Length: 536740006 (512M) (unauthoritative)

100%[======================================================================================================>] 536,740,006 26.1MB/s   in 21s

2022-08-04 06:35:54 (24.7 MB/s) - ‘bigann_gnd.tar.gz’ saved [536740006]

[tigergraph sift100M] $ wget ftp://ftp.irisa.fr/local/texmex/corpus/bigann_learn.bvecs.gz
--2022-08-04 06:35:59--  ftp://ftp.irisa.fr/local/texmex/corpus/bigann_learn.bvecs.gz
           => ‘bigann_learn.bvecs.gz’
Resolving ftp.irisa.fr (ftp.irisa.fr)... 131.254.254.45, 2001:660:7303:254::45
Connecting to ftp.irisa.fr (ftp.irisa.fr)|131.254.254.45|:21... connected.
Logging in as anonymous ... Logged in!
==> SYST ... done.    ==> PWD ... done.
==> TYPE I ... done.  ==> CWD (1) /local/texmex/corpus ... done.
==> SIZE bigann_learn.bvecs.gz ... 9746888942
==> PASV ... done.    ==> RETR bigann_learn.bvecs.gz ... done.
Length: 9746888942 (9.1G) (unauthoritative)

100%[====================================================================================================>] 9,746,888,942 25.8MB/s   in 6m 7s

2022-08-04 06:42:07 (25.3 MB/s) - ‘bigann_learn.bvecs.gz’ saved [9746888942]

[tigergraph sift100M] $ wget ftp://ftp.irisa.fr/local/texmex/corpus/bigann_base.bvecs.gz
--2022-08-04 06:42:32--  ftp://ftp.irisa.fr/local/texmex/corpus/bigann_base.bvecs.gz
           => ‘bigann_base.bvecs.gz’
Resolving ftp.irisa.fr (ftp.irisa.fr)... 131.254.254.45, 2001:660:7303:254::45
Connecting to ftp.irisa.fr (ftp.irisa.fr)|131.254.254.45|:21... connected.
Logging in as anonymous ... Logged in!
==> SYST ... done.    ==> PWD ... done.
==> TYPE I ... done.  ==> CWD (1) /local/texmex/corpus ... done.
==> SIZE bigann_base.bvecs.gz ... 97941899519
==> PASV ... done.    ==> RETR bigann_base.bvecs.gz ... done.
Length: 97941899519 (91G) (unauthoritative)

100%[===================================================================================================>] 97,941,899,519 15.1MB/s   in 64m 47sd

2022-08-04 08:02:22 (24.0 MB/s) - ‘bigann_base.bvecs.gz’ saved [97941899519]

```
## 1.2 extract the compressed files
```
[tigergraph sift100M] $ gunzip bigann_query.bvecs.gz
[tigergraph sift100M] $ time tar zxvf bigann_gnd.tar.gz
gnd/
gnd/dis_100M.fvecs
gnd/dis_10M.fvecs
gnd/dis_1M.fvecs
gnd/dis_200M.fvecs
gnd/dis_20M.fvecs
gnd/dis_2M.fvecs
gnd/dis_500M.fvecs
gnd/dis_50M.fvecs
gnd/dis_5M.fvecs
gnd/idx_1000M.ivecs
gnd/idx_100M.ivecs
gnd/idx_10M.ivecs
gnd/idx_1M.ivecs
gnd/idx_200M.ivecs
gnd/idx_20M.ivecs
gnd/idx_2M.ivecs
gnd/idx_500M.ivecs
gnd/idx_50M.ivecs
gnd/idx_5M.ivecs
gnd/README
gnd/dis_1000M.fvecs

real    0m7.417s
user    0m7.065s
sys     0m1.298s
[tigergraph sift100M] $ rm bigann_gnd.tar.gz
[tigergraph sift100M] $ time gunzip bigann_learn.bvecs.gz

real    2m13.634s
user    2m7.568s
sys     0m6.065s
[tigergraph sift100M] $ time gunzip bigann_base.bvecs.gz

real    21m52.580s
user    20m52.562s
sys     1m0.011s
```
# 2. Convert the raw data to csv file
## 2.1 install Anaconda
Download 64-Bit (x86) Installer from https://www.anaconda.com/products/individual#Downloads, and install it.
```
[tigergraph sift100M] cd
[tigergraph ~] $ wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
--2022-08-04 09:28:05--  https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
Resolving repo.anaconda.com (repo.anaconda.com)... 104.16.130.3, 104.16.131.3, 2606:4700::6810:8203, ...
Connecting to repo.anaconda.com (repo.anaconda.com)|104.16.130.3|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 690850711 (659M) [application/x-sh]
Saving to: ‘Anaconda3-2022.05-Linux-x86_64.sh’

100%[=============================================================================>] 690,850,711  204MB/s   in 3.3s

2022-08-04 09:28:08 (201 MB/s) - ‘Anaconda3-2022.05-Linux-x86_64.sh’ saved [690850711/690850711]

[tigergraph ~] chmod +x Anaconda3-2022.05-Linux-x86_64.sh
[tigergraph ~] ./Anaconda3-2022.05-Linux-x86_64.sh
...
Do you wish the installer to initialize Anaconda3
...
Do you accept the license terms? [yes|no]
[no] >>> yes
...
[/home/tigergraph/anaconda3] >>>
PREFIX=/home/tigergraph/anaconda3
...
by running conda init? [yes|no]
[no] >>> yes
...
```
## 2.2 Create an new environment
Exit and SSH again, and then create the new environment.
```
(base) [tigergraph ~] $ conda create --name hnsw python=3.9
...
Proceed ([y]/n)? y
...
(base) [tigergraph ~] $ conda activate hnsw
(hnsw) [tigergraph ~] $ conda install matplotlib pandas seaborn scipy numpy
...
Proceed ([y]/n)?y
...
(hnsw) [tigergraph ~] $ conda install -c conda-forge faiss-cpu
...
Proceed ([y]/n)?y
...
(hnsw) [tigergraph ~] $ pip install requests
...
```
## 2.3 convert the raw data to csv file
Change directory to the hnsw folder and run the following command to run the python command
```
(hnsw) [tigergraph hnsw] $ cd python_SIFT100M
(hnsw) [tigergraph python_SIFT100M] $ time python convertor.py
/home/tigergraph/data/hnsw/sift100M/bigann_base.bvecs (100000000, 128)
/home/tigergraph/data/hnsw/sift100M/gnd/idx_100M.ivecs (10000, 1000)
/home/tigergraph/data/hnsw/sift100M/bigann_query.bvecs (10000, 128)

real    30m49.410s
user    30m34.191s
sys     0m30.052s

```
# 3. use Faiss to run HNSW
```
(hnsw) [tigergraph python_SIFT100M] $ time python hnsw.py
(1, 128)
[[  3.   9.  17.  78.  83.  15.  10.   8. 101. 109.  21.   8.   3.   2.
    9.  64.  39.  31.  18.  80.  55.  10.   2.  12.   7.   7.  26.  58.
   32.   6.   4.   3.  14.   2.  13.  28.  37.  19.  47.  59. 109.  22.
    2.   6.  18.  15.  20. 109.  30.   8.  11.  44. 109.  54.  19.  32.
   17.  21.  15.  22.  12.  28. 101.  35.  66.  11.   9.  30.  68.  35.
   30.  75. 106. 103.  26.  50.  76.  20.   8.  13.  51.  41.  63. 109.
   40.   2.   3.  15.  36.  49.  21.  13.  12.   9.  36.  37.  52.  37.
   24.  34.  19.   3.  13.  23.  21.   8.   3.  20.  68.  56.  79.  60.
   99.  36.   7.  28.  78.  41.   7.  21.  74.  26.   3.  15.  34.  15.
   12.  27.]]
(100000000, 128)
construction time: 1518850.582 ms.
[[64124. 64727. 67335. 67541. 67666. 69641. 70382. 70415. 70878. 71618.]]
[[28539420 64429592 40642738 80468484 18530806 14925721 61457390 82774411
  22351844 28798102]]
search time: 1180.817 ms.
file writing time: 5605862.196 ms.

real    119m15.684s
user    3009m0.987s
sys     170m5.143s

```

# 4. create schema, install queries and load data
## 4.1 create schema
```
(hnsw) [tigergraph python_SIFT100M] $ cd ../
(hnsw) [tigergraph hnsw] $ gsql 1_create_schema.gsql
Stopping GPE GSE RESTPP
Successfully stopped GPE GSE RESTPP in 43.598 seconds
Starting GPE GSE RESTPP
Successfully started GPE GSE RESTPP in 0.092 seconds
The graph HNSW is created.
Successfully created schema change jobs: [change_schema_of_HNSW].

Current graph version 0
Trying to add vertex Element.
Trying to add vertex EntryPoint.
Trying to add edge link_to.
Trying to add edge entrypoint_element.
Kick off job change_schema_of_HNSW

Graph HNSW update to new version 1
The job change_schema_of_HNSW completes in 10.721 seconds!
Successfully dropped jobs on the graph 'HNSW': [change_schema_of_HNSW].
```
## 4.2 install queries
### 4.2.1 add UDF
```
vi /home/tigergraph/tigergraph/app/3.2.4/dev/gdk/gsql/src/QueryUdf/ExprFunctions.hpp
```
Add the following UDF to the file:
```
  inline ListAccum <double> split (string s, string delimiter) {
    size_t pos_start = 0, pos_end, delim_len = delimiter.length();
    string token;
    ListAccum <double> outBag;

    while ((pos_end = s.find (delimiter, pos_start)) != string::npos) {
        token = s.substr (pos_start, pos_end - pos_start);
        if(token != ""){
            outBag += atof(token.c_str());
        }
        pos_start = pos_end + delim_len;
    }
    
    token = s.substr (pos_start);
    if(token != ""){
        outBag += atof(token.c_str());
    }
    return outBag;
  }
```
Then run the command below:
```
(hnsw) [tigergraph hnsw] $ gsql 'PUT ExprFunctions FROM "/home/tigergraph/tigergraph/app/3.2.4/dev/gdk/gsql/src/QueryUdf/ExprFunctions.hpp"'
PUT ExprFunctions successfully.
```
### 4.2.2 install queries
```
(hnsw) [tigergraph hnsw] $ gsql 3_install_queries.gsql
Using graph 'HNSW'
Successfully created queries: [q1_search_vis].
Successfully created queries: [q1_search].
Successfully created queries: [q2_explore].
Successfully created queries: [q3_stats].
Start installing queries, about 1 minute ...
q3_stats query: curl -X GET 'http://127.0.0.1:9000/query/HNSW/q3_stats'. Add -H "Authorization: Bearer TOKEN" if authentication is enabled.
q2_explore query: curl -X GET 'http://127.0.0.1:9000/query/HNSW/q2_explore?[min_level=VALUE]'. Add -H "Authorization: Bearer TOKEN" if authentication is enabled.
q1_search query: curl -X GET 'http://127.0.0.1:9000/query/HNSW/q1_search?[input=VALUE]&[k=VALUE]&[ef_search=VALUE]&[max_level=VALUE]&[dim=VALUE]'. Add -H "Authorization: Bearer TOKEN" if authentication is enabled.
q1_search_vis query: curl -X GET 'http://127.0.0.1:9000/query/HNSW/q1_search_vis?[input=VALUE]&[k=VALUE]&[ef_search=VALUE]&[hop=VALUE]&[max_level=VALUE]&[dim=VALUE]'. Add -H "Authorization: Bearer TOKEN" if authentication is enabled.
Select 'm1' as compile server, now connecting ...
Node 'm1' is prepared as compile server.

[========================================================================================================] 100% (4/4)
Query installation finished.
```
## 4.3 load data
## 4.3.1 load the base file
```
(hnsw) [tigergraph hnsw] $ gstatusgraph
=== graph ===
[GRAPH  ] Graph was loaded (/home/tigergraph/tigergraph/data/gstore/0/part/):
[m1     ] Partition size: 3.7KiB, IDS size: 454KiB, Vertex count: 0, Edge count: 0, NumOfDeletedVertices: 0 NumOfSkippedVertices: 0
[WARN   ] Above vertex and edge counts are for internal use which show approximate topology size of the local graph partition. Use DML to get the correct graph topology information
(hnsw) [tigergraph hnsw] $ gsql 2.3_load_sift100M.gsql
Using graph 'HNSW'
Successfully created loading jobs: [loading_job].
[Tip: Use "CTRL + C" to stop displaying the loading status update, then use "SHOW LOADING STATUS jobid" to track the loading progress again]
[Tip: Manage loading jobs with "ABORT/RESUME LOADING JOB jobid"]
Starting the following job, i.e.
  JobName: loading_job, jobid: HNSW.loading_job.file.m1.1659614190475
  Loading log: '/home/tigergraph/tigergraph/log/restpp/restpp_loader_logs/HNSW/HNSW.loading_job.file.m1.1659614190475.log'

Job "HNSW.loading_job.file.m1.1659614190475" loading status
[FINISHED] m1 ( Finished: 1 / Total: 1 )
  [LOADED]
  +-----------------------------------------------------------------------------------------------+
  |                                           FILENAME |   LOADED LINES |   AVG SPEED |   DURATION|
  |/home/tigergraph/data/hnsw/sift100M/bigann_base.csv |      100000000 |    359 kl/s |   278.43 s|
  +-----------------------------------------------------------------------------------------------+
Successfully dropped jobs on the graph 'HNSW': [loading_job].
(hnsw) [tigergraph hnsw] $ gstatusgraph
=== graph ===
[GRAPH  ] Graph was loaded (/home/tigergraph/tigergraph/data/gstore/0/part/):
[m1     ] Partition size: 97GiB, IDS size: 934MiB, Vertex count: 100000000, Edge count: 0, NumOfDeletedVertices: 0 NumOfSkippedVertices: 0
[WARN   ] Above vertex and edge counts are for internal use which show approximate topology size of the local graph partition. Use DML to get the correct graph topology information
```
## 4.3.2 load the HNSW graph
```
(hnsw) [tigergraph hnsw] $ gsql 2.4_load_hnsw_graph.gsql
Using graph 'HNSW'
Successfully created loading jobs: [loading_job].
[Tip: Use "CTRL + C" to stop displaying the loading status update, then use "SHOW LOADING STATUS jobid" to track the loading progress again]
[Tip: Manage loading jobs with "ABORT/RESUME LOADING JOB jobid"]
Starting the following job, i.e.
  JobName: loading_job, jobid: HNSW.loading_job.file.m1.1659624934612
  Loading log: '/home/tigergraph/tigergraph/log/restpp/restpp_loader_logs/HNSW/HNSW.loading_job.file.m1.1659624934612.log'

Job "HNSW.loading_job.file.m1.1659624934612" loading status
[FINISHED] m1 ( Finished: 2 / Total: 2 )
  [LOADED]
  +-------------------------------------------------------------------------------------------+
  |                                       FILENAME |   LOADED LINES |   AVG SPEED |   DURATION|
  |      /home/tigergraph/data/hnsw/hnsw/edges.csv |     2181291638 |   2417 kl/s |   902.37 s|
  |/home/tigergraph/data/hnsw/hnsw/entry_point.csv |              1 |      10 l/s |     0.10 s|
  +-------------------------------------------------------------------------------------------+
Successfully dropped jobs on the graph 'HNSW': [loading_job].
(hnsw) [tigergraph hnsw] $ gstatusgraph
=== graph ===
[GRAPH  ] Graph was loaded (/home/tigergraph/tigergraph/data/gstore/0/part/):
[m1     ] Partition size: 111GiB, IDS size: 935MiB, Vertex count: 100000001, Edge count: 2155702626, NumOfDeletedVertices: 0 NumOfSkippedVertices: 0
[WARN   ] Above vertex and edge counts are for internal use which show approximate topology size of the local graph partition. Use DML to get the correct graph topology information
```
# 5 run the query
## 5.1 link_to edge level distribution
```
(hnsw) [tigergraph hnsw] $ ./shell_SIFT100M/q3_stats.sh
{"version":{"edition":"enterprise","api":"v2","schema":1},"error":false,"message":"","results":[{"@@map":{"7":20,"6":695,"1":2091122567,"2":84555507,"3":5276740,"4":318194,"5":17915}}]}
real    0m58.338s
user    0m0.007s
sys     0m0.000s
```
## 5.2 ANN search
```
(hnsw) [tigergraph hnsw] $ ./shell_SIFT100M/q1_search.sh
{"version":{"edition":"enterprise","api":"v2","schema":1},"error":false,"message":"","results":[{"@@min_heap":[{"element":"87356234","dist":61249},{"element":"28539420","dist":64124},{"element":"64429592","dist":64727},{"element":"40642738","dist":67335},{"element":"80468484","dist":67541},{"element":"18530806","dist":67666},{"element":"82631435","dist":69496},{"element":"14925721","dist":69641},{"element":"13934280","dist":70287},{"element":"61457390","dist":70382}]}]}
real    0m0.072s
user    0m0.002s
sys     0m0.003s
```
## 5.3 concurrency test
```
(hnsw) [tigergraph hnsw] $ ./shell_SIFT100M/ab_q1_search.sh
concurrency: 200; total_num: 200; k: 10; ef_search: 32

This is ApacheBench, Version 2.3 <$Revision: 1430300 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 100 requests
Completed 200 requests
Finished 200 requests


Server Software:        nginx
Server Hostname:        127.0.0.1
Server Port:            14240

Document Path:          /restpp/query/HNSW/q1_search?input=3,9,17,78,83,15,10,8,101,109,21,8,3,2,9,64,39,31,18,80,55,10,2,12,7,7,26,58,32,6,4,3,14,2,13,28,37,19,47,59,109,22,2,6,18,15,20,109,30,8,11,44,109,54,19,32,17,21,15,22,12,28,101,35,66,11,9,30,68,35,30,75,106,103,26,50,76,20,8,13,51,41,63,109,40,2,3,15,36,49,21,13,12,9,36,37,52,37,24,34,19,3,13,23,21,8,3,20,68,56,79,60,99,36,7,28,78,41,7,21,74,26,3,15,34,15,12,27&k=10&max_level=7&ef_search=32
Document Length:        474 bytes

Concurrency Level:      200
Time taken for tests:   0.659 seconds
Complete requests:      200
Failed requests:        0
Write errors:           0
Total transferred:      147399 bytes
HTML transferred:       94800 bytes
Requests per second:    303.71 [#/sec] (mean)
Time per request:       658.525 [ms] (mean)
Time per request:       3.293 [ms] (mean, across all concurrent requests)
Transfer rate:          218.59 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    7   2.7      7      12
Processing:    67  423  97.1    365     590
Waiting:       55  423  97.5    365     590
Total:         67  430  95.1    372     596

Percentage of the requests served within a certain time (ms)
  50%    372
  66%    526
  75%    542
  80%    552
  90%    560
  95%    571
  98%    589
  99%    590
 100%    596 (longest request)

real    0m0.664s
user    0m0.003s
sys     0m0.027s
```