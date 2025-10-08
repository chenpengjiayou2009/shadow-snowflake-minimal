#!/usr/bin/env python3

import requests
import time
import random
import threading
import json
import base64
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Configuration parameters
RUNS = 1000
MIN_SLEEP = 1    # minimum seconds between requests
MAX_SLEEP = 5    # maximum seconds between requests
THREAD_COUNT = 3 # Number of concurrent requests per batch (set to RUNS for all requests at once)
URL = 'http://broker:8080/client'
HEADERS = {'Content-Type': 'text/plain'}
# The data needs to be exactly the same as in the shell script
sdp_offer = {
    "type": "offer",
    "sdp": "fake-sdp"}
# Convert the SDP offer to a JSON string
offer_json = json.dumps(sdp_offer, separators=(',', ':'))

# Base64 encode the JSON string
base64_offer = base64.b64encode(offer_json.encode('utf-8')).decode('utf-8')
# The data needs to be exactly the same as in the shell script
DATA = f"1.0\n{{\"offer\":\"fake-sdp\",\"nat\":\"unrestricted\",\"fingerprint\":\"2B280B23E1107BB62ABFC40DDCC8824814F80A72\"}}"

def get_timestamp():
    """Return current timestamp in the format YYYY-MM-DD HH:MM:SS"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def send_request(request_id, total_requests):
    """Send a single POST request and log the result"""
    print(f"[{get_timestamp()}] Request {request_id}/{total_requests}")
    
    try:
        # Send POST request
        response = requests.post(URL, headers=HEADERS, data=DATA)
        # Get status code (equivalent to exit code in shell)
        status_code = response.status_code
        print(f"[{get_timestamp()}] Request {request_id}: Status code: {status_code} Response: {response.text}")
        
    except requests.exceptions.RequestException as e:
        # Handle any request errors
        print(f"[{get_timestamp()}] Request {request_id}: Error: {str(e)}")
        status_code = -1  # Custom error code


def main():
    print(f"Starting {RUNS} requests with random intervals between {MIN_SLEEP}-{MAX_SLEEP} seconds")
    print(f"Sending {THREAD_COUNT} requests concurrently per batch")
    
    request_count = 0
    
    while request_count < RUNS:
        # Calculate how many requests to send in this batch
        remaining = RUNS - request_count
        current_batch_size = min(THREAD_COUNT, remaining)
        
        print(f"\n[{get_timestamp()}] Starting batch of {current_batch_size} requests")
        
        # Use ThreadPoolExecutor to manage concurrent requests
        with ThreadPoolExecutor(max_workers=current_batch_size) as executor:
            futures = []
            for i in range(current_batch_size):
                request_id = request_count + i + 1
                futures.append(executor.submit(send_request, request_id, RUNS))
            
            # Wait for all requests in this batch to complete
            for future in futures:
                future.result()
        
        # Update request count
        request_count += current_batch_size
        
        # Sleep after each batch, except when all requests are done
        if request_count < RUNS:
            # Generate random sleep time
            range_seconds = MAX_SLEEP - MIN_SLEEP + 1
            if range_seconds > 0:
                delay = random.randint(MIN_SLEEP, MAX_SLEEP)
            else:
                delay = MIN_SLEEP
            print(f"Sleeping {delay}s...")
            time.sleep(delay)
    
    print(f"Completed all {RUNS} requests")


if __name__ == "__main__":
    main()
