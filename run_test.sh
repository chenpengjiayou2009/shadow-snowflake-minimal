rm -rf shadow.data
shadow --model-unblocked-syscall-latency=true snowflake.yaml  > shadow.log
cat shadow.data/hosts/broker/* | grep "Popping" > analyze_output/popping.txt
cat shadow.data/hosts/*proxy*/* | grep "current" > analyze_output/proxies.txt
cd analyze_output
python3 combine_proxy_stats.py
