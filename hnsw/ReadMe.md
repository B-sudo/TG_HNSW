This is a solution of Real-time Graph-based ANNS(Approximate Nearest Neighbor Search). This file tells you how to test it on the dataset SIFT1M which has 1 million base data, while ReadMe_SIFT100M.md tells you how to test it on the dataset SIFT100M. For more information, please visit https://docs.google.com/presentation/d/1ckyQbTTlSfWzbAsNDU_RZ7AIQIL-vY2RMGwIfa33DwE/edit#slide=id.g109915c673b_0_0.

# 1. Dowload dataset
## 1.1 Dowload dataset ANN_SIFT10K from http://corpus-texmex.irisa.fr/
```
[tigergraph ~] $ mkdir -p /home/tigergraph/data/hnsw
[tigergraph ~] $ cd /home/tigergraph/data/hnsw
[tigergraph hnsw] $ wget ftp://ftp.irisa.fr/local/texmex/corpus/siftsmall.tar.gz
--2022-07-29 02:45:01--  ftp://ftp.irisa.fr/local/texmex/corpus/siftsmall.tar.gz
           => ‘siftsmall.tar.gz’
Resolving ftp.irisa.fr (ftp.irisa.fr)... 131.254.254.45, 2001:660:7303:254::45
Connecting to ftp.irisa.fr (ftp.irisa.fr)|131.254.254.45|:21... connected.
Logging in as anonymous ... Logged in!
==> SYST ... done.    ==> PWD ... done.
==> TYPE I ... done.  ==> CWD (1) /local/texmex/corpus ... done.
==> SIZE siftsmall.tar.gz ... 5305734
==> PASV ... done.    ==> RETR siftsmall.tar.gz ... done.
Length: 5305734 (5.1M) (unauthoritative)

100%[=============================================================================>] 5,305,734   5.26MB/s   in 1.0s

2022-07-29 02:45:04 (5.26 MB/s) - ‘siftsmall.tar.gz’ saved [5305734]

[tigergraph hnsw] $ tar zxvf siftsmall.tar.gz
siftsmall/
siftsmall/siftsmall_base.fvecs
siftsmall/siftsmall_groundtruth.ivecs
siftsmall/siftsmall_learn.fvecs
siftsmall/siftsmall_query.fvecs
[tigergraph hnsw] $ rm siftsmall.tar.gz
```
## 1.2 Dowload dataset ANN_SIFT1M from http://corpus-texmex.irisa.fr/
```
[tigergraph hnsw] $ wget ftp://ftp.irisa.fr/local/texmex/corpus/sift.tar.gz
--2022-07-29 02:45:34--  ftp://ftp.irisa.fr/local/texmex/corpus/sift.tar.gz
           => ‘sift.tar.gz’
Resolving ftp.irisa.fr (ftp.irisa.fr)... 131.254.254.45, 2001:660:7303:254::45
Connecting to ftp.irisa.fr (ftp.irisa.fr)|131.254.254.45|:21... connected.
Logging in as anonymous ... Logged in!
==> SYST ... done.    ==> PWD ... done.
==> TYPE I ... done.  ==> CWD (1) /local/texmex/corpus ... done.
==> SIZE sift.tar.gz ... 168280445
==> PASV ... done.    ==> RETR sift.tar.gz ... done.
Length: 168280445 (160M) (unauthoritative)

100%[=============================================================================>] 168,280,445 25.5MB/s   in 7.1s

2022-07-29 02:45:43 (22.7 MB/s) - ‘sift.tar.gz’ saved [168280445]

[tigergraph hnsw] $ tar zxvf sift.tar.gz
sift/
sift/sift_base.fvecs
sift/sift_groundtruth.ivecs
sift/sift_learn.fvecs
sift/sift_query.fvecs
[tigergraph hnsw] $ rm sift.tar.gz
```
# 2. Convert the raw data to csv file
## 2.1 install Anaconda
Download 64-Bit (x86) Installer from https://www.anaconda.com/products/individual#Downloads, and install it.
```
[tigergraph hnsw] cd
[tigergraph ~] wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
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
```
## 2.2 Create an new environment
```
[tigergraph ~] $ conda create --name hnsw python=3.9
...
Proceed ([y]/n)? y
...
[tigergraph ~] $ conda activate hnsw
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
(hnsw) [tigergraph hnsw] $ cd python
(hnsw) [tigergraph python] $ time python convertor.py
(10000, 128)
(100, 100)
(25000, 128)
(100, 128)
(1000000, 128)
(10000, 100)
(100000, 128)
(10000, 128)

real    1m13.745s
user    1m10.495s
sys     0m3.248s

```
# 3. use Faiss to run HNSW
```
(hnsw) [tigergraph python] $ time python hnsw.py
(1, 128)
(1000000, 128)
construction time: 28159.517 ms.
[[54229. 55091. 59531. 65260. 65697. 67010. 69844. 71441. 71861. 73344.
  73537. 73581. 73793. 75124. 75554. 75634. 76583. 76664. 77660. 78092.]]
[[932085 934876 561813 708177 706771 695756 701258 455537 872728  36538
  562594 908244 600499 562167 746931 565419  36267 454263 886630 779712]]
search time: 1.935 ms.
file writing time: 47137.553 ms.

real    1m18.928s
user    13m0.739s
sys     1m12.222s

```

# 4. create schema, install queries and load data
## 4.1 create schema
```
(hnsw) [tigergraph python] $ cd ../
(hnsw) [tigergraph hnsw] $ gsql 1_create_schema.gsql
Stopping GPE GSE RESTPP
Successfully stopped GPE GSE RESTPP in 30.562 seconds
Starting GPE GSE RESTPP
Successfully started GPE GSE RESTPP in 0.074 seconds
The graph HNSW is created.
Successfully created schema change jobs: [change_schema_of_HNSW].

Current graph version 0
Trying to add vertex Element.
Trying to add vertex EntryPoint.
Trying to add edge link_to.
Trying to add edge entrypoint_element.
Kick off job change_schema_of_HNSW

Graph HNSW update to new version 1
The job change_schema_of_HNSW completes in 9.823 seconds!
Successfully dropped jobs on the graph 'HNSW': [change_schema_of_HNSW].
```
## 4.2 install queries
### 4.2.1 add UDF
```
vi /home/tigergraph/tigergraph/app/3.2.3/dev/gdk/gsql/src/QueryUdf/ExprFunctions.hpp
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
(hnsw) [tigergraph hnsw] $ gsql 'PUT ExprFunctions FROM "/home/tigergraph/tigergraph/app/3.2.3/dev/gdk/gsql/src/QueryUdf/ExprFunctions.hpp"'
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
q1_search query: curl -X GET 'http://127.0.0.1:9000/query/HNSW/q1_search?input=VALUE&[k=VALUE]&[ef_search=VALUE]&[max_level=VALUE]&[dim=VALUE]'. Add -H "Authorization: Bearer TOKEN" if authentication is enabled.
q1_search_vis query: curl -X GET 'http://127.0.0.1:9000/query/HNSW/q1_search_vis?input=VALUE&[k=VALUE]&[ef_search=VALUE]&[max_level=VALUE]&[dim=VALUE]'. Add -H "Authorization: Bearer TOKEN" if authentication is enabled.
Select 'm1' as compile server, now connecting ...
Node 'm1' is prepared as compile server.

[========================================================================================================] 100% (4/4)
Query installation finished.
```
## 4.3 load data
```
(hnsw) [tigergraph hnsw] $ gstatusgraph
=== graph ===
[GRAPH  ] Graph was loaded (/home/tigergraph/tigergraph/data/gstore/0/part/):
[m1     ] Partition size: 3.6KiB, IDS size: 453KiB, Vertex count: 0, Edge count: 0, NumOfDeletedVertices: 0 NumOfSkippedVertices: 0
[WARN   ] Above vertex and edge counts are for internal use which show approximate topology size of the local graph partition. Use DML to get the correct graph topology information
(hnsw) [tigergraph hnsw] $ gsql 2.2_load_sift.gsql
Using graph 'HNSW'
Successfully created loading jobs: [loading_job].
[Tip: Use "CTRL + C" to stop displaying the loading status update, then use "SHOW LOADING STATUS jobid" to track the loading progress again]
[Tip: Manage loading jobs with "ABORT/RESUME LOADING JOB jobid"]
Starting the following job, i.e.
  JobName: loading_job, jobid: HNSW.loading_job.file.m1.1659320604364
  Loading log: '/home/tigergraph/tigergraph/log/restpp/restpp_loader_logs/HNSW/HNSW.loading_job.file.m1.1659320604364.log'

Job "HNSW.loading_job.file.m1.1659320604364" loading status
[FINISHED] m1 ( Finished: 1 / Total: 1 )
  [LOADED]
  +-----------------------------------------------------------------------------------------+
  |                                     FILENAME |   LOADED LINES |   AVG SPEED |   DURATION|
  |/home/tigergraph/data/hnsw/sift/sift_base.csv |        1000000 |    242 kl/s |     4.13 s|
  +-----------------------------------------------------------------------------------------+
Successfully dropped jobs on the graph 'HNSW': [loading_job].
(hnsw) [tigergraph hnsw] $ gstatusgraph
=== graph ===
[GRAPH  ] Graph was loaded (/home/tigergraph/tigergraph/data/gstore/0/part/):
[m1     ] Partition size: 989MiB, IDS size: 24MiB, Vertex count: 1000000, Edge count: 0, NumOfDeletedVertices: 0 NumOfSkippedVertices: 0
[WARN   ] Above vertex and edge counts are for internal use which show approximate topology size of the local graph partition. Use DML to get the correct graph topology information
(hnsw) [tigergraph hnsw] $ gsql 2.4_load_hnsw_graph.gsql
Using graph 'HNSW'
Successfully created loading jobs: [loading_job].
[Tip: Use "CTRL + C" to stop displaying the loading status update, then use "SHOW LOADING STATUS jobid" to track the loading progress again]
[Tip: Manage loading jobs with "ABORT/RESUME LOADING JOB jobid"]
Starting the following job, i.e.
  JobName: loading_job, jobid: HNSW.loading_job.file.m1.1659320647553
  Loading log: '/home/tigergraph/tigergraph/log/restpp/restpp_loader_logs/HNSW/HNSW.loading_job.file.m1.1659320647553.log'

Job "HNSW.loading_job.file.m1.1659320647553" loading status
[FINISHED] m1 ( Finished: 2 / Total: 2 )
  [LOADED]
  +-------------------------------------------------------------------------------------------+
  |                                       FILENAME |   LOADED LINES |   AVG SPEED |   DURATION|
  |      /home/tigergraph/data/hnsw/hnsw/edges.csv |       18397960 |   1475 kl/s |    12.47 s|
  |/home/tigergraph/data/hnsw/hnsw/entry_point.csv |              1 |      10 l/s |     0.10 s|
  +-------------------------------------------------------------------------------------------+
Successfully dropped jobs on the graph 'HNSW': [loading_job].
(hnsw) [tigergraph hnsw] $ gstatusgraph
=== graph ===
[GRAPH  ] Graph was loaded (/home/tigergraph/tigergraph/data/gstore/0/part/):
[m1     ] Partition size: 1.1GiB, IDS size: 24MiB, Vertex count: 1000001, Edge count: 13901800, NumOfDeletedVertices: 0 NumOfSkippedVertices: 0
[WARN   ] Above vertex and edge counts are for internal use which show approximate topology size of the local graph partition. Use DML to get the correct graph topology information
```
# 5 run the query
## 5.1 link_to edge level distribution
```
(hnsw) [tigergraph hnsw] $ ./shell/q3_stats.sh
{"version":{"edition":"enterprise","api":"v2","schema":1},"error":false,"message":"","results":[{"@@map":{"1":17587446,"2":764679,"3":43711,"4":1884,"5":240}}]}
real    0m1.163s
user    0m0.002s
sys     0m0.004s
```
## 5.2 ANN search
```
(hnsw) [tigergraph hnsw] $ ./shell/q1_search.sh
{"version":{"edition":"enterprise","api":"v2","schema":1},"error":false,"message":"","results":[{"@@min_heap":[{"element":"932085","dist":54229},{"element":"934876","dist":55091},{"element":"561813","dist":59531},{"element":"708177","dist":65260},{"element":"706771","dist":65697},{"element":"695756","dist":67010},{"element":"435345","dist":68247},{"element":"701258","dist":69844},{"element":"455537","dist":71441},{"element":"872728","dist":71861}]}]}
real    0m0.035s
user    0m0.002s
sys     0m0.005s
```
## 5.3 concurrency test
```
(hnsw) [tigergraph hnsw] $ ./shell/ab_q1_search.sh
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

Document Path:          /restpp/query/HNSW/q1_search?input=1.0,3.0,11.0,110.0,62.0,22.0,4.0,0.0,43.0,21.0,22.0,18.0,6.0,28.0,64.0,9.0,11.0,1.0,0.0,0.0,1.0,40.0,101.0,21.0,20.0,2.0,4.0,2.0,2.0,9.0,18.0,35.0,1.0,1.0,7.0,25.0,108.0,116.0,63.0,2.0,0.0,0.0,11.0,74.0,40.0,101.0,116.0,3.0,33.0,1.0,1.0,11.0,14.0,18.0,116.0,116.0,68.0,12.0,5.0,4.0,2.0,2.0,9.0,102.0,17.0,3.0,10.0,18.0,8.0,15.0,67.0,63.0,15.0,0.0,14.0,116.0,80.0,0.0,2.0,22.0,96.0,37.0,28.0,88.0,43.0,1.0,4.0,18.0,116.0,51.0,5.0,11.0,32.0,14.0,8.0,23.0,44.0,17.0,12.0,9.0,0.0,0.0,19.0,37.0,85.0,18.0,16.0,104.0,22.0,6.0,2.0,26.0,12.0,58.0,67.0,82.0,25.0,12.0,2.0,2.0,25.0,18.0,8.0,2.0,19.0,42.0,48.0,11.0&k=10
Document Length:        454 bytes

Concurrency Level:      200
Time taken for tests:   0.406 seconds
Complete requests:      200
Failed requests:        0
Write errors:           0
Total transferred:      142711 bytes
HTML transferred:       90800 bytes
Requests per second:    492.16 [#/sec] (mean)
Time per request:       406.375 [ms] (mean)
Time per request:       2.032 [ms] (mean, across all concurrent requests)
Transfer rate:          342.95 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    9   3.2      9      15
Processing:    52  208  92.4    217     351
Waiting:       37  208  92.6    217     351
Total:         52  218  89.6    224     356

Percentage of the requests served within a certain time (ms)
  50%    224
  66%    271
  75%    299
  80%    307
  90%    348
  95%    351
  98%    354
  99%    355
 100%    356 (longest request)
```