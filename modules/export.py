import json
import numpy as np
from pathlib import Path

class Exporter:
    def __init__(self):
        print("SocNav3 Exporter initialised")
        self.robot_shape = {
            "type": "circle",
            "width": 0.6,
            "length": 0.6
        }

    def export_to_socnav3(self, data, output_path, sequence_path=None, metadata=""):
        print(f"Exporting to: {output_path}")
        
        socnav3_data = self.build_socnav3_structure(data, sequence_path, metadata)
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(socnav3_data, f, indent=2)
        
        print(f"Saved to {output_path}")
        return str(output_path)
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
                dif = abs(t - timestamp)
                if dif < min_dif:
                    min_dif = dif
                    closest_idx = i
            if closest_idx >= len(positions) or closest_idx >= len(orientations):
                continue

            agent_id = traj['agent_id']
            try:
                person_id = int(agent_id.split(':')[-1])
            except:
                person_id = hash(agent_id) % 10000
            
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
    
    def build_sequence(self, robot_traj, human_trajs):
        sequence = []

        robot_positions = robot_traj['positions']
        robot_times = robot_traj['timestamps']
        robot_velocities = robot_traj['velocities']
        robot_orientations = robot_traj['orientations']

        goal_x = robot_positions[-1][0]
        goal_y = robot_positions[-1][1]
        goal_angle = robot_orientations[-1]

        for i, timestamp in enumerate(robot_times):
            robot_state = {
                "shape": self.robot_shape,
                "x": float(robot_positions[i][0]),
                "y": float(robot_positions[i][1]),
                "angle": float(robot_orientations[i]),
                "speed_x": float(robot_velocities[i][0]),
                "speed_y": float(robot_velocities[i][1]),
                "speed_a": 0.0
            }

            goal = {
                "type": "go-to",
                "human": None,
                "x": float(goal_x),
                "y": float(goal_y),
                "angle": float(goal_angle),
                "pos_threshold": 0.5,
                "angle_threshold": 0.1
            }

            people = self.get_people_at_time(human_trajs, timestamp)

            frame = {
                "timestamp": float(timestamp),
                "robot": robot_state,
                "goal": goal,
                "people": people,
                "objects": []
            }

            sequence.append(frame)
        return sequence
    
    def build_socnav3_structure(self, data, sequence_path, metadata):
        trajectories = data['trajectories']
        robot_traj = None
        human_trajs = []
        for traj in trajectories:
            if traj['type'] == 'robot':
                robot_traj = traj
            else:
                human_trajs.append(traj)
        
        if robot_traj is None:
            raise ValueError("No robot trajectory found")
        
        sequence = self.build_sequence(robot_traj, human_trajs)
        grid = self.build_grid(trajectories)
        return {
            "metadata": metadata or f"Converted frmo SiT: {data['metadata']['sequence_name']}",
            "sequence": sequence,
            "grid": grid,
        }
    
def export_to_socnav3(data, output_path, sequence_path=None, metadata=""):
    exporter = Exporter()
    return exporter.export_to_socnav3(data, output_path, sequence_path, metadata)