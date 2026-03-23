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
