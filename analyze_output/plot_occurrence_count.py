import re
import matplotlib.pyplot as plt
from collections import defaultdict

# 1. Extract session IDs and their occurrence counts and first occurrence line numbers from enumeration file
def extract_enumeration_info(file_path):
    session_counts = defaultdict(int)  # Store occurrence counts of each session ID
    first_occurrences = {}  # Store the first occurrence line number of each session ID
    
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):  # Line numbers start from 1
            match = re.search(r'Popping (.+?) for enumeration', line)
            if match:
                session_id = match.group(1)
                session_counts[session_id] += 1
                
                # Record the first occurrence line number
                if session_id not in first_occurrences:
                    first_occurrences[session_id] = line_num
    
    return session_counts, first_occurrences

# 2. Extract session IDs and their types from proxy file
def extract_proxy_types(file_path):
    session_types = {}  # Store session IDs and their types
    
    with open(file_path, 'r') as file:
        for line in file:
            # Extract type and sessionId
            type_match = re.search(r'current type is (\w+)', line)
            id_match = re.search(r'current sessionId is (.+?),', line)
            
            if type_match and id_match:
                session_type = type_match.group(1)
                session_id = id_match.group(1)
                # If session ID already exists, we keep only the first occurrence type
                if session_id not in session_types:
                    session_types[session_id] = session_type
    
    return session_types

# 3. Plot the scatter graph with first occurrence line numbers on x-axis and occurrence counts on y-axis
def plot_occurrence_count(session_counts, first_occurrences, session_types):
    # Prepare data
    x_values = []  # First occurrence line numbers
    y_values = []  # Occurrence counts
    colors = []    # Colors based on proxy type (green for standalone, blue for webext)
    labels = []    # Session IDs for tooltips (optional)
    
    for session_id, count in session_counts.items():
        if session_id in first_occurrences:
            x_values.append(first_occurrences[session_id])
            y_values.append(count)
            labels.append(session_id)
            
            # Determine color based on proxy type
            if session_id in session_types and session_types[session_id] == 'standalone':
                colors.append('green')
            else:
                colors.append('blue')
    
    # Create figure
    plt.figure(figsize=(14, 10))
    
    # Plot scatter points
    scatter = plt.scatter(x_values, y_values, alpha=0.7, s=60, c=colors)
    
    # Create legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Webext Session', markerfacecolor='blue', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Standalone Session', markerfacecolor='green', markersize=10)
    ]
    plt.legend(handles=legend_elements, loc='best')
    
    # Set plot properties
    plt.title('Session ID Occurrence Count by First Appearance Polling Number')
    plt.xlabel('First Occurrence Polling Number')
    plt.ylabel('Number of Occurrences')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Save plot
    plt.tight_layout()
    plt.savefig('occurrence_count_scatter.png', dpi=300)
    print(f"Scatter plot saved as 'occurrence_count_scatter.png'")
    
    # Statistical information
    total_sessions = len(session_counts)
    standalone_count = sum(1 for session_id in session_counts 
                          if session_id in session_types and session_types[session_id] == 'standalone')
    
    max_occurrences = max(session_counts.values())
    avg_occurrences = sum(session_counts.values()) / total_sessions if total_sessions > 0 else 0
    
    print(f"Total unique session IDs: {total_sessions}")
    print(f"Standalone session IDs: {standalone_count}")
    print(f"Webext session IDs: {total_sessions - standalone_count}")
    print(f"Maximum occurrences of a session ID: {max_occurrences}")
    print(f"Average occurrences per session ID: {avg_occurrences:.2f}")

# Main function
def main():
    enumeration_file = 'enumeration-original.txt'
    proxy_file = 'proxies-original.txt'
    
    try:
        # Extract enumeration information
        session_counts, first_occurrences = extract_enumeration_info(enumeration_file)
        
        if not session_counts:
            print("No session IDs found in the enumeration file.")
            return
        
        # Extract proxy type data
        session_types = extract_proxy_types(proxy_file)
        
        # Plot occurrence count scatter graph
        plot_occurrence_count(session_counts, first_occurrences, session_types)
        
    except Exception as e:
        print(f"Error processing files: {e}")

if __name__ == "__main__":
    main()
