import pytest
import numpy as np
from modules.loadData import SiTDataLoader
 
 
class TestSiTDataLoader:
 
    def test_loader_initialises(self):
        loader = SiTDataLoader()
        assert loader is not None
 
    def test_missing_directory_raises_error(self):
        loader = SiTDataLoader()
        with pytest.raises(FileNotFoundError):
            loader.load_sit_sequence("nonexistent_folder_12345")
 
    def test_robot_pose_matrix_parsing(self):
        values = [
            1, 0, 0, 5.0,
            0, 1, 0, 3.0,
            0, 0, 1, 1.0,
            0, 0, 0, 1
        ]
        matrix = np.array(values).reshape(4, 4)
        x = matrix[0, 3]
        y = matrix[1, 3]
        z = matrix[2, 3]
        assert x == 5.0
        assert y == 3.0
        assert z == 1.0
 
    def test_pedestrian_line_parsing(self):
        line = "Pedestrian Pedestrian:4 0.5 1.7 0.5 2.34 -1.56 0.0 1.57"
        parts = line.strip().split()
        assert parts[0] == "Pedestrian"
        assert parts[1] == "Pedestrian:4"
        assert float(parts[5]) == 2.34
        assert float(parts[6]) == -1.56
        assert float(parts[7]) == 0.0
 
    def test_person_id_extraction(self):
        agent_id = "Pedestrian:4"
        person_id = int(agent_id.split(':')[-1])
        assert person_id == 4
 
    def test_timestamp_generation(self):
        num_frames = 200
        timestamps = [i * 0.1 for i in range(num_frames)]
        assert len(timestamps) == 200
        assert timestamps[0] == 0.0
        assert timestamps[1] == pytest.approx(0.1)
        assert timestamps[-1] == pytest.approx(19.9)
 