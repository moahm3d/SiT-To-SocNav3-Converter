import numpy as np
from pathlib import Path
import pypcd4 as pypcd 


#Module was tested but traj-based method will be used in production instead
#export.py shows future usage

def read_pcd_file(pcd_file):
    #Reads single PCD file and returns 3d points
    try:
        pc = pypcd.PointCloud.from_path(str(pcd_file))

        #x,y,z coordinates from point cloud
        points = np.column_stack((pc.pc_data['x'], 
                                 pc.pc_data['y'], 
                                 pc.pc_data['z']))
        
        #removes invalid points
        valid_mask = np.isfinite(points).all(axis=1)
        points = points[valid_mask]
        return points
        
    except Exception as e:
        print(f"  Error reading {pcd_file.name}: {e}")
        return np.array([])


def accumulate_pcd_points(pcd_dir, num_frames=10):
    #Loads multiple PCD frames and combines the points
    #Goal is to get as many points as possible
    pcd_files = sorted(pcd_dir.glob("*.pcd"))[:num_frames]
    
    if not pcd_files:
        return np.array([])
    
    print(f"Loading PCD files from {pcd_dir}...")
    
    all_points = []
    for i, pcd_file in enumerate(pcd_files):
        points = read_pcd_file(pcd_file)
        if len(points) > 0:
            all_points.extend(points)
            print(f"  Frame {i}: {len(points)} points")
    
    if not all_points:
        return np.array([])
    
    points_array = np.array(all_points)
    print(f"Total accumulated: {len(points_array)} points")
    
    return points_array


def extract_boundary_walls(points):
    #Makes rect boundary around scanned area using min/max bounds
    if len(points) == 0:
        return []
    
    min_x = float(points[:, 0].min())
    max_x = float(points[:, 0].max())
    min_y = float(points[:, 1].min())
    max_y = float(points[:, 1].max())
    
    print(f"Bounds: X=[{min_x:.2f}, {max_x:.2f}], Y=[{min_y:.2f}, {max_y:.2f}]")
    

    #left,top,right,bottom
    return [
        [min_x, min_y, min_x, max_y],
        [min_x, max_y, max_x, max_y],
        [max_x, max_y, max_x, min_y],
        [max_x, min_y, min_x, min_y]
    ]


def extract_walls_from_pcd(sequence_path, sensor='top'):
    #Looks for top LIDAR sensor folder
    pcd_dir = Path(sequence_path) / 'velo' / sensor / 'data'
    
    if not pcd_dir.exists():
        return []
    
    #Combines points
    points = accumulate_pcd_points(pcd_dir, num_frames=10)
    
    if len(points) == 0:
        return []
    
    #Get bound walls from point cloud
    walls = extract_boundary_walls(points)
    return walls
