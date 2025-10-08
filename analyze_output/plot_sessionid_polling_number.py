import re
import matplotlib.pyplot as plt
import argparse

# Extract session IDs and line numbers from enumeration file
def extract_enumeration_data(file_path):
    session_data = []  # Store all session IDs and their line numbers
    first_occurrences = {}  # Store the first occurrence line number of each session ID
    
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):  # Line numbers start from 1
            match = re.search(r'Popping (.+?) for enumeration', line)
            if match:
                session_id = match.group(1)
                # Record the first occurrence line number
                if session_id not in first_occurrences:
                    first_occurrences[session_id] = line_num
                
                # Store session ID and line number
                session_data.append((session_id, line_num))
    
    return session_data, first_occurrences

# Extract session IDs and their types from proxy file
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

# Plot scatter graph
def plot_scatter_with_types(session_data, first_occurrences, session_types):
    # Assign a unique index to each unique session ID
    unique_sessions = {session_id: i for i, (session_id, _) in enumerate(set(session_data))}
    
    # Prepare data
    x = [unique_sessions[session_id] for session_id, _ in session_data]
    y = [line_num for _, line_num in session_data]
    session_ids = [session_id for session_id, _ in session_data]
    
    # Create figure
    plt.figure(figsize=(14, 10))
    
    # Prepare colors for different types of session IDs
    colors = []
    for session_id in session_ids:
        # Default to blue, standalone type is green
        if session_id in session_types and session_types[session_id] == 'standalone':
            colors.append('green')
        else:
            colors.append('blue')
    
    # Plot all points
    scatter = plt.scatter(x, y, alpha=0.6, s=50, c=colors)
    
    # Mark first occurrence points
    first_x = []
    first_y = []
    first_labels = []
    first_colors = []
    
    for session_id, line_num in first_occurrences.items():
        first_x.append(unique_sessions[session_id])
        first_y.append(line_num)
        first_labels.append(session_id)
        if session_id in session_types and session_types[session_id] == 'standalone':
            first_colors.append('green')
        else:
            first_colors.append('red')
    
    # Plot first occurrence points
    plt.scatter(first_x, first_y, alpha=1.0, s=80, c=first_colors, marker='*', label='First occurrence')
    
    # Create legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Webext Session', markerfacecolor='blue', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Standalone Session', markerfacecolor='green', markersize=10),
        Line2D([0], [0], marker='*', color='w', label='First Occurrence (Webext)', markerfacecolor='red', markersize=10),
        Line2D([0], [0], marker='*', color='w', label='First Occurrence (Standalone)', markerfacecolor='green', markersize=10)
    ]
    plt.legend(handles=legend_elements, loc='best')
    
    # Set plot properties
    plt.title('Session ID Enumeration Scatter Plot with Types')
    plt.xlabel('Session ID (Indexed)')
    plt.ylabel('Polling Number')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Save plot
    plt.tight_layout()
    plt.savefig('enumeration_with_types_scatter_FIFO.png', dpi=300)
    print(f"Scatter plot saved as 'enumeration_with_types_scatter.png'")
    
    # Statistical information
    total_sessions = len(unique_sessions)
    standalone_count = sum(1 for session_id in unique_sessions if session_id in session_types and session_types[session_id] == 'standalone')
    
    print(f"Total unique session IDs: {total_sessions}")
    print(f"Standalone session IDs: {standalone_count}")
    print(f"Webext session IDs: {total_sessions - standalone_count}")
    print(f"First occurrences marked with stars on the plot.")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Script with two positional arguments")
    parser.add_argument("--enumeration-file", default="enumeration.txt" , help="Path to the enumeration file")
    parser.add_argument("--proxy-file", default="proxies.txt" , help="Path to the proxies file")
    args = parser.parse_args()
    
    try:
        # Extract enumeration data
        session_data, first_occurrences = extract_enumeration_data(args.enumeration_file)
        
        if not session_data:
            print("No session IDs found in the enumeration file.")
            return
        
        # Extract proxy type data
        session_types = extract_proxy_types(args.proxy_file)
        
        # Plot scatter graph
        plot_scatter_with_types(session_data, first_occurrences, session_types)
        
    except Exception as e:
        print(f"Error processing files: {e}")

if __name__ == "__main__":
    main()
