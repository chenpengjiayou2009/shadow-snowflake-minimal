rm -rf shadow.data
shadow --model-unblocked-syscall-latency=true snowflake.yaml  > shadow.log
cat shadow.data/hosts/broker/* | grep "enumeration" > analyze_output/enumeration.txt
cat shadow.data/hosts/*proxy*/* | grep "current" > analyze_output/proxies.txt
cd analyze_output
python3 plot_occurrence_count.py
python3 plot_proxy_polling.py
python3 plot_sessionid_polling_number.py