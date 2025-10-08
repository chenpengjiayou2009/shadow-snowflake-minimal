import re
import csv
import os
from collections import defaultdict, Counter

# Define file paths
proxies_filename = 'proxies.txt'
popping_filename = 'popping.txt'
output_filename = 'combined_proxy_stats.csv'

# Data storage for extracted information
session_data = {}
# Statistics by type
type_stats = defaultdict(lambda: {'count': 0, 'total_clients': 0, 'total_interval': 0})

# 定义正则表达式模式
type_pattern = re.compile(r'current type is ([^,]+),')
session_id_pattern = re.compile(r'current sessionId is ([^,]+),')
interval_pattern = re.compile(r'current interval is %!f\(time\.Duration=([0-9]+)\)')
clients_pattern = re.compile(r'current clients served is (\d+)')

# Count ID occurrences in popping.txt
def count_popping_ids(filename):
    # Initialize counter
    id_counter = Counter()
    
    try:
        # Read file and extract IDs
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                for line in f.readlines():
                    # Directly search for fixed-format ID parts
                    start_idx = line.find('%!d(string=')
                    if start_idx != -1:
                        # Skip prefix
                        start_idx += len('%!d(string=')
                        # Find end position
                        end_idx = line.find(')', start_idx)
                        if end_idx != -1:
                            # Extract ID
                            id_value = line[start_idx:end_idx]
                            id_counter[id_value] += 1
            print(f'Successfully extracted {len(id_counter)} unique IDs from {filename}')
        else:
            print(f'Warning: File {filename} does not exist, will use empty ID count')
        
        return id_counter
        
    except Exception as e:
        print(f'Error processing file {filename}: {e}')
        return Counter()

# Process proxies.txt file
def process_proxies_file(filename):
    total_lines = 0
    parsed_lines = 0
    
    print(f'Processing file: {filename}')
    
    try:
        with open(filename, 'r') as f:
            for line_num, line in enumerate(f, 1):
                total_lines += 1
                line = line.strip()
                if not line:
                    continue
                
                # Extract information
                type_match = type_pattern.search(line)
                session_id_match = session_id_pattern.search(line)
                interval_match = interval_pattern.search(line)
                clients_match = clients_pattern.search(line)
                
                if type_match and session_id_match and interval_match and clients_match:
                    parsed_lines += 1
                    
                    # Extract data
                    session_type = type_match.group(1)
                    session_id = session_id_match.group(1)
                    interval_ns = int(interval_match.group(1))
                    interval_seconds = interval_ns / 1_000_000_000  # Convert to seconds
                    clients = int(clients_match.group(1))
                    
                    # Store session data
                    session_data[session_id] = {
                        'type': session_type,
                        'interval_seconds': interval_seconds,
                        'interval_ns': interval_ns,
                        'clients': clients,
                        'pop_count': 0  # Initialize to 0
                    }
                    
                    # Update type statistics
                    type_stats[session_type]['count'] += 1
                    type_stats[session_type]['total_clients'] += clients
                    type_stats[session_type]['total_interval'] += interval_seconds
        
        print(f'Processing complete: {total_lines} lines, successfully parsed {parsed_lines} lines, extracted {len(session_data)} sessions')
        
    except FileNotFoundError:
        print(f'Error: Cannot find file {filename}')
        return False
    except Exception as e:
        print(f'Error occurred while processing file: {e}')
        return False
    
    return True

# Export results to CSV file
def export_to_csv(filename, session_data, popping_counts):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['session_id', 'type', 'interval_seconds', 'interval_ns', 'clients', 'pop_count', 'has_popping']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for session_id, data in session_data.items():
                # Get popping count, 0 if ID not in popping_counts
                pop_count = popping_counts.get(session_id, 0)
                has_popping = 1 if pop_count > 0 else 0
                
                writer.writerow({
                    'session_id': session_id,
                    'type': data['type'],
                    'interval_seconds': data['interval_seconds'],
                    'interval_ns': data['interval_ns'],
                    'clients': data['clients'],
                    'pop_count': pop_count,
                    'has_popping': has_popping
                })
            print(f'\nCombined statistical data has been saved to: {filename}')
            return True
    except Exception as e:
        print(f'Error saving data to CSV: {e}')
        return False

# Print type statistics
def print_type_stats(type_stats):
    print(f'\n==== Session Type Statistics ====')
    print('-' * 90)
    print(f"| {'Type':<15} | {'Count':<10} | {'Avg Clients':<15} | {'Avg Interval(s)':<15} | {'Sessions with Pop':<15} |")
    print('-' * 90)
    
    for session_type, stats in type_stats.items():
        avg_clients = stats['total_clients'] / stats['count'] if stats['count'] > 0 else 0
        avg_interval = stats['total_interval'] / stats['count'] if stats['count'] > 0 else 0
        # Calculate number of sessions with popping
        pop_count = sum(1 for data in session_data.values() if data['type'] == session_type and data['pop_count'] > 0)
        print(f'| {session_type:<15} | {stats["count"]:<10} | {avg_clients:<15.2f} | {avg_interval:<15.2f} | {pop_count:<15} |')
    
    print('-' * 90)

# Print information about sessions with popping
def print_popping_sessions(session_data):
    popping_sessions = {k: v for k, v in session_data.items() if v['pop_count'] > 0}
    if popping_sessions:
        print(f'\n==== Sessions with Popping Records ({len(popping_sessions)}) ====')
        print('-' * 100)
        print(f"| {'Session ID':<30} | {'Type':<15} | {'Clients':<10} | {'Interval(s)':<10} | {'Pop Count':<10} |")
        print('-' * 100)
        
        # Sort by popping count
        sorted_sessions = sorted(popping_sessions.items(), key=lambda x: x[1]['pop_count'], reverse=True)
        for session_id, data in sorted_sessions:
            # Limit session ID display length
            display_id = session_id[:27] + '...' if len(session_id) > 30 else session_id
            print(f'| {display_id:<30} | {data["type"]:<15} | {data["clients"]:<10} | {data["interval_seconds"]:<10.1f} | {data["pop_count"]:<10} |')
        
        print('-' * 100)
    else:
        print('\nNo sessions with popping records found')

# Main function
def main():
    # Process proxies.txt file
    if not process_proxies_file(proxies_filename):
        return
    
    # Count ID occurrences in popping.txt
    popping_counts = count_popping_ids(popping_filename)
    
    # Update popping counts in session_data
    for session_id, pop_count in popping_counts.items():
        if session_id in session_data:
            session_data[session_id]['pop_count'] = pop_count
    
    # Print type statistics
    print_type_stats(type_stats)
    
    # Print information about sessions with popping
    print_popping_sessions(session_data)
    
    # Export combined data to CSV file
    if not export_to_csv(output_filename, session_data, popping_counts):
        return
    
    print('\nAll operations completed')

if __name__ == '__main__':
    main()
