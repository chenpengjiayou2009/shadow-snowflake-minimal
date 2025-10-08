#!/usr/bin/env python3

import matplotlib.pyplot as plt
import re
from collections import defaultdict

# Function to process popping.txt and proxies.txt and generate the plot
def plot_proxy_polling(filename:str):
    # Set up data structures to track unique proxies
    webext_proxies = set()
    standalone_proxies = set()
    total_proxies = set()  # Track all unique proxies regardless of type
    
    # Track counts over lines
    line_numbers = []
    webext_counts = []
    standalone_counts = []
    total_counts = []  # Track total unique proxies count over lines
    
    current_line = 0
    current_unique_web_count = set()
    current_unique_standalone_count = set()
    current_unique_total_count = set()

    print("Processing proxies.txt...")
    try:
        with open('proxies-FIFO.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Extract proxy type and session ID
                # Format: "current type is webext, current sessionId is +tFR7QcWkjuD7jAuTEN4Cg, ..."
                type_match = re.search(r'type is (\w+)', line)
                session_match = re.search(r'sessionId is ([^,]+)', line)
        
                if type_match and session_match:
                    proxy_type = type_match.group(1)
                    session_id = session_match.group(1)
                    print(proxy_type)
                    print("session id", session_id)
                    
                    # Add to the appropriate set
                    if proxy_type == 'webext':
                        webext_proxies.add(session_id)
                    elif proxy_type == 'standalone':
                        standalone_proxies.add(session_id)

            
    except FileNotFoundError:
        print("Warning: proxies.txt not found")
    print('standalone session ids', standalone_proxies)
    # Process popping.txt
    print("Processing enumeration.txt...")
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Extract session ID from popping.txt lines
                # Format: "2000/01/01 00:02:05 Popping restricted %!d(string=1bFbK6IhuFgwyRUNfxma4Q) out of heap"
                match = re.search(r'Popping\s+([^,]+)\s+for\s+enumeration', line)
                if match:
                    session_id = match.group(1)
                
                
                current_line += 1
                line_numbers.append(current_line)
                if session_id in webext_proxies and session_id not in current_unique_web_count:
                    print("find a web-ext session", session_id)
                    current_unique_web_count.add(session_id)
                
                if session_id in standalone_proxies and session_id not in current_unique_standalone_count:
                    print("find a standalone session", session_id)
                    current_unique_standalone_count.add(session_id)

                current_unique_total_count.add(session_id)

                standalone_counts.append(len(current_unique_standalone_count))
                webext_counts.append(len(current_unique_web_count))
                total_counts.append(len(current_unique_total_count))

    except FileNotFoundError:
        print("Warning: popping.txt not found")
    
    for id in webext_proxies:
        if id not in current_unique_web_count:
            print(id)
            print(";;;")
    
    # Create the plot
    print("Generating plot...")
    plt.figure(figsize=(12, 6))
    
    # Plot the data
    if line_numbers:
        print("web counts", len(webext_counts))
        plt.plot(line_numbers, webext_counts, 'b-', label='Unique WebExt Proxies')
        print("standalone counts", len(standalone_counts))
        plt.plot(line_numbers, standalone_counts, 'g-', label='Unique Standalone Proxies')
        print("total counts", len(total_counts))
        plt.plot(line_numbers, total_counts, 'r-', label='Total Unique Proxies')
        
        # Add labels and title
        plt.xlabel('Polling Time')
        plt.ylabel('Unique Proxies Count')
        plt.title('Unique WebExt, Standalone, and Total Proxies Polled Over Lines')
        plt.legend()
        plt.grid(True)
        
        # Save the plot
        output_file = 'proxy_polling_trends_FIFO.png'
        plt.savefig(output_file)
        print(f"Plot saved to {output_file}")
        
        # Show the plot
        plt.show()
    else:
        print("No data to plot")

if __name__ == "__main__":
    filename="enumeration-FIFO.txt"
    plot_proxy_polling(filename)
