import numpy as np
from pathlib import Path


class SiTDataLoader:
    def __init__(self):
        print("Starting SiT Data Loader")
    def load_sit_sequence(self, sequence_path):
        sequence_path = Path(sequence_path)
        if not sequence_path.exists():
            raise FileNotFoundError(f"Folder not found: {sequence_path}")
        label_dir = sequence_path / "label_3d"
        robot_dir = sequence_path / "ego_trajectory"
        if not label_dir.exists():
            raise FileNotFoundError(f"label_3d folder not found")
        if not robot_dir.exists():
            raise FileNotFoundError(f"ego_trajectory folder not found")
        print(f"Loading sequence: {sequence_path.name}")

        frames = self.load_all_frames(label_dir, robot_dir)
        trajectories = self.build_trajectories(frames)
        num_frames = len(frames)
        timestamps = [i * 0.1 for i in range(num_frames)]

        metadata = {
            'sequence_name': sequence_path.name,
            'num_frames': num_frames,
            'num_agents': len(trajectories) - 1,
            'fps': 10.0,
            'duration_seconds': num_frames * 0.1
        }
    
    def parse_pedestrians(self, filepath):
        pedestrians = []

        try:
            with open(filepath, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 9:
                        pedestrians.append({
                            'type': parts[0],
                            'id': parts[1],
                            'x': float(parts[5]),
                            'y': float(parts[6]),
                            'z': float(parts[7]),
                            'rotation': float(parts[8])
                        })
        except Exception as e:
            print(f"Warning: ERror parsing {filepath}: {e}")
        
        return pedestrians
    
    def parse_robot_pose(self, filepath):
        try:
            with open(filepath, 'r') as f:
                values = [float(x) for x in f.read().strip().split(',')]

                if len(values) == 16:
                    matrix = np.array(values.reshape(4, 4))
                    x = matrix[0,3]
                    y = matrix[1,3]
                    z = matrix[2,3]

                    return [x, y, z]
        except Exception as e:
            print(f"Warning: Error parsing {filepath}: {e}")
        
        return None
    
    def build_trajectories(self, frames):
        agent_tracks = {}

        for frame in frames:
            frame_time = frame['frame_id'] * 0.1
            for ped in frame['pedestrians']:
                agent_id = ped['id']

                if agent_id not in agent_tracks:
                    agent_tracks[agent_id] = {
                        'agent_id': agent_id,
                        'type': 'human',
                        'positions': [],
                        'timestamps': []
                    }

                agent_tracks[agent_id]['positions'].append([ped['x'], ped['y'], ped['z']])
                agent_tracks[agent_id]['timestamps'].append(frame_time)

        if frame['robot_pose'] is not None:
            if 'robot_0' not in agent_tracks:
                agent_tracks['robot_0'] = {
                    'agent_id': 'robot_0',
                    'type': 'robot',
                    'position': [],
                    'timestamps': []
                }

            agent_tracks['robot_0']['positions'].append(frame['robot_pose'])
            agent_tracks['robot_0']['timestamps'].append(frame_time)

        return list(agent_tracks.values())
    
    def load_all_frames(self, label_dir, robot_dir):
        label_files = sorted(label_dir.glob("*.txt"), key=lambda x: int(x.stem))

        frames = []
        for label_file in label_files:
            frame_num = int(label_file.stem)
            pedestrians = self.parse_pedestrians(label_file)
            robot_file = robot_dir / f"{frame_num}.txt"
            if robot_file.exists():
                robot_pose = self.parse_robot_Pose(robot_file)
            
            frames.append({
                'frame_id': frame_num,
                'pedestrians': pedestrians,
                'robot_pose': robot_pose
            })

        print(f"Loaded {len(frames)} frames")
        return frames
    
    
