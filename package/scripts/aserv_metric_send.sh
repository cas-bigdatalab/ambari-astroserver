#!/bin/sh
url=http://$1:6188/ws/v1/timeline/metrics
hostname=$2
appid='aserv'
cd 	~/gwac/gwac_dbgen_cluster
while [ 1 ]
do 
./getSumData.sh
arr=(`cat stalog.txt`)
line=${arr[0]}
size=${arr[1]}
latesttime="${arr[2]} ${arr[3]}"

millon_time=$(( $(date +%s%N) / 1000000 ))
json="{
 \"metrics\": [
 {
 \"metricname\": \"line\",
 \"appid\": \"${appid}\",
 \"hostname\": \"${hostname}\",
 \"timestamp\": ${millon_time},
 \"starttime\": ${millon_time},
 \"metrics\": {
 \"${millon_time}\": ${line}
 }
 },
 {
 \"metricname\": \"size\",
 \"appid\": \"${appid}\",
 \"hostname\": \"${hostname}\",
 \"timestamp\": ${millon_time},
 \"starttime\": ${millon_time},
 \"metrics\": {
 \"${millon_time}\": ${size}
 }
 }
 ]
}"
 
# echo $json
#|tee -a /root/my_metric.log
curl -i -X POST -H "Content-Type: application/json" -d "${json}" ${url}
sleep 5
done
