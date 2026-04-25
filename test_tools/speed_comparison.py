import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def load_json(filepath):
    #Loads JSON file
    with open(filepath, 'r') as f:
        return json.load(f)


def get_average_speeds(data):
    #Calc avg speed(total dist/ total time) by going through all frames and tracking each person pos over time
    sequence = data['sequence']
    
    #Collects pos and timestamp for each person
    person_positions = {}
    person_timestamps = {}
    
    for frame in sequence:
        timestamp = frame['timestamp']
        
        for person in frame.get('people', []):
            pid = person['id']
            
            if pid not in person_positions:
                person_positions[pid] = []
                person_timestamps[pid] = []
            
            person_positions[pid].append([person['x'], person['y']])
            person_timestamps[pid].append(timestamp)
    
    #Calc avg speed for each person
    avg_speeds = []
    
    for pid in person_positions:
        positions = person_positions[pid]
        times = person_timestamps[pid]
        
        #Needs 2 pos to calculate speed
        if len(positions) < 2:
            continue
        
        total_distance = 0.0
        for i in range(len(positions) - 1):
            dx = positions[i+1][0] - positions[i][0]
            dy = positions[i+1][1] - positions[i][1]
            total_distance += np.sqrt(dx**2 + dy**2)
        
        total_time = times[-1] - times[0]
        
        if total_time > 0:
            avg_speed = total_distance / total_time
            avg_speeds.append(avg_speed)
    
    return avg_speeds


def load_all_speeds(folder_path):
    #Loads JSON files from folder and gets speed from each
    folder = Path(folder_path)
    all_speeds = []
    
    json_files = list(folder.glob("*.json"))
    print(f"Found {len(json_files)} files in {folder}")
    
    for json_file in json_files:
        try:
            data = load_json(json_file)
            speeds = get_average_speeds(data)
            all_speeds.extend(speeds)
            print(f"  {json_file.name}: {len(speeds)} trajectories")
        except Exception as e:
            print(f"  Skipping {json_file.name}: {e}")
    
    return all_speeds


def plot_comparison(original_speeds, converted_speeds):
    #Plots both speed onto 1D plot 
    fig, ax = plt.subplots(figsize=(10, 3))
    
    #Green = SocNAV3, Blue = SiT converted into SocNav3 format
    if original_speeds:
        ax.scatter(original_speeds, [1.0] * len(original_speeds),
                   color='green', alpha=0.5, s=30, label='Original (SocNav3)')
    
    if converted_speeds:
        ax.scatter(converted_speeds, [0.5] * len(converted_speeds),
                   color='blue', alpha=0.5, s=30, label='Converted (SiT)')
    
    ax.set_xlabel('Average Speed (m/s)')
    ax.set_yticks([0.5, 1.0])
    ax.set_yticklabels(['Converted (SiT)', 'Original (SocNav3)'])
    ax.set_title('Average Trajectory Speed Comparison')
    ax.legend(loc='upper right')
    ax.grid(True, axis='x', alpha=0.3)
    
    #Set x axis range
    all_speeds = original_speeds + converted_speeds
    if all_speeds:
        ax.set_xlim(-0.1, min(max(all_speeds) * 1.2, 10))
    
    plt.tight_layout()
    plt.savefig("speed_comparison.png", dpi=150)
    print("Saved plot to speed_comparison.png")
    plt.show()


#Paths to folders
original_path = "socnav3_traj"
converted_path = "test_output"

#Prints the statistics
print("Loading original SocNav3 data...")
original_speeds = load_all_speeds(original_path)

print("\nLoading converted data...")
converted_speeds = load_all_speeds(converted_path)

print(f"\nOriginal: {len(original_speeds)} trajectories")
if original_speeds:
    arr = np.array(original_speeds)
    print(f"  Mean: {arr.mean():.3f} m/s")
    print(f"  Min: {arr.min():.3f}, Max: {arr.max():.3f}")

print(f"\nConverted: {len(converted_speeds)} trajectories")
if converted_speeds:
    arr = np.array(converted_speeds)
    print(f"  Mean: {arr.mean():.3f} m/s")
    print(f"  Min: {arr.min():.3f}, Max: {arr.max():.3f}")

#Makes plot
plot_comparison(original_speeds, converted_speeds)