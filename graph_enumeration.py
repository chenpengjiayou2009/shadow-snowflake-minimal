import re
import matplotlib.pyplot as plt
import os
from datetime import datetime

def parse_log_file_and_plot(filename):
    """Read log data from file and create the graph"""
    
    # Check if file exists
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found!")
        return None, None
    
    # Read the log file
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            log_text = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None
    
    # Split into lines and filter out empty lines
    lines = [line.strip() for line in log_text.split('\n') if line.strip()]
    
    # Extract session IDs using regex
    session_ids = []
    for line in lines:
        match = re.search(r'string=([^)]+)', line)
        if match:
            session_ids.append(match.group(1))
    
    if not session_ids:
        print("No session IDs found in the log file!")
        return None, None
    
    # Track unique session IDs as we go through each line
    unique_sessions = set()
    unique_counts = []
    
    for i, session_id in enumerate(session_ids):
        unique_sessions.add(session_id)
        unique_counts.append(len(unique_sessions))
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(range(1, len(unique_counts) + 1), unique_counts, 'b-o', linewidth=2, markersize=4)
    plt.xlabel('Line Number')
    plt.ylabel('Number of Unique Session IDs')
    plt.title('Unique Session IDs Over Time')
    plt.grid(True, alpha=0.3)
    
    # Add some styling
    plt.tight_layout()
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"unique_session_ids_{timestamp}.png"
    
    # Save the plot to current directory
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Graph saved as: {output_filename}")
    
    # Optionally show the plot (comment out if you don't want to display)
    # plt.show()
    
    # Print summary
    print(f"Total lines processed: {len(session_ids)}")
    print(f"Total unique session IDs: {len(unique_sessions)}")
    print(f"Session IDs: {list(unique_sessions)}")
    
    return unique_counts, list(unique_sessions)

# Usage example:
if __name__ == "__main__":
    # Replace 'logfile.txt' with your actual log file path
    filename = "Popping-FIFO.txt"
    unique_counts, session_ids = parse_log_file_and_plot(filename)
