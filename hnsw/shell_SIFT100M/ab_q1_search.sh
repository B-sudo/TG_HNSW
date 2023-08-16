concurrency=200
num=1
k=10
ef_search=32

if [ $# -ge 2 ]
then
    k=$1
    ef_search=$2
elif [ $# -ge 1 ]
then
    k=$1
    ef_search=$1
fi
total_num=$((concurrency*num))
echo "concurrency: $concurrency; total_num: $total_num; k: $k; ef_search: $ef_search"
echo 
time ab -n $total_num -c $concurrency -H "GSQL-TIMEOUT: 3600000" "http://127.0.0.1:14240/restpp/query/HNSW/q1_search?input=3,9,17,78,83,15,10,8,101,109,21,8,3,2,9,64,39,31,18,80,55,10,2,12,7,7,26,58,32,6,4,3,14,2,13,28,37,19,47,59,109,22,2,6,18,15,20,109,30,8,11,44,109,54,19,32,17,21,15,22,12,28,101,35,66,11,9,30,68,35,30,75,106,103,26,50,76,20,8,13,51,41,63,109,40,2,3,15,36,49,21,13,12,9,36,37,52,37,24,34,19,3,13,23,21,8,3,20,68,56,79,60,99,36,7,28,78,41,7,21,74,26,3,15,34,15,12,27&k=$k&max_level=7&ef_search=$ef_search"


