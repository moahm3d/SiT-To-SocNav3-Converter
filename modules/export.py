import json
import numpy as np
from pathlib import Path

class Exporter:
    def __init__(self):
        print("SocNav3 Exporter initialised")
    def get_people_at_time(self, human_trajs, timestamp):
        people = []

        for traj in human_trajs:
            times = traj['timestamps']
            positions = traj['positions']
            orientations = traj['orientations']

            if len(times) == 0:
                continue

            if timestamp < times[0] or timestamp > times[-1]:
                continue

            closest_idx = 0
            min_dif = abs(times[0] - timestamp)

            for i, t in enumerate(times):
                diff = abs(t - timestamp)
                if diff < min_diff:
                    min_diff = diff
                    closest_idx = i
            if closest_idx >= len(positions) or closest_idx >= len(orientations):
                continue

            agent_id = traj['agent_id']
            try:
                person_id = int(agent_id.split(':')[-1])
            except:
                person_id = hash(agent_id) & 10000
            
            try:
                person = {
                    "id": person_id,
                    "x": float(positions[closest_idx][0]),
                    "y": float(positions[closest_idx][1]),
                    "angle": float(orientations[closest_idx])
                }
                people.append(person)
            except (IndexError, TypeError) as e:
                print(f"Warning: Skipping person {agent_id} at time {timestamp}: {e}")
                continue

        return people
    
    def build_grid(self, trajectories):
        all_positions = []
        for traj in trajectories:
            all_positions.extend(traj['positions'])
        
        if not all_positions:
            return {
                "width": 200,
                "height": 200,
                "cell_size": 0.1,
                "x_orig": -10.0,
                "y_orig": -10.0,
                "angle_orig": 0.0,
                "data": [[0]]
            }
        
        positions = np.array(all_positions)
        min_x = positions[:, 0].min()
        max_x = positions[:, 0].max()
        min_y = positions[:, 1].min()
        max_y = positions[:, 1].max()
        padding = 2.0
        min_x -= padding
        max_x += padding
        min_y -= padding
        max_y += padding
        
        width = max_x - min_x
        height = max_y - min_y
        cell_size = 0.1
        grid_width = int(np.ceil(width / cell_size))
        grid_height = int(np.ceil(height / cell_size))

        grid_data = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

        return {
            "width": grid_width,
            "height": grid_height,
            "cell_size": cell_size,
            "x_orig": float(min_x),
            "y_orig": float(min_y),
            "angle_orig": 0.0,
            "data": grid_data
        }