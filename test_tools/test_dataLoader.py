import pytest
import numpy as np
from modules.loadData import SiTDataLoader
 
#pytest test_tools/test_dataLoader.py -v
class TestSiTDataLoader:
 
    def test_loader_initialises(self):
        #Checks if loader creates
        loader = SiTDataLoader()
        assert loader is not None
 
    def test_missing_directory_raises_error(self):
        #Raises error if folder doesn't exist
        loader = SiTDataLoader()
        with pytest.raises(FileNotFoundError):
            loader.load_sit_sequence("nonexistent_folder_12345")
 
    def test_robot_pose_matrix_parsing(self):
        #Checks if we can reshape into 4x4 matrix from 16 values
        values = [
            1, 0, 0, 5.0,
            0, 1, 0, 3.0,
            0, 0, 1, 1.0,
            0, 0, 0, 1
        ]
        matrix = np.array(values).reshape(4, 4)
        #Checks if it pulls x,y,z from last column
        x = matrix[0, 3]
        y = matrix[1, 3]
        z = matrix[2, 3]
        assert x == 5.0
        assert y == 3.0
        assert z == 1.0
 
    def test_pedestrian_line_parsing(self):
        #Checks label_3d line gets split into right fields
        line = "Pedestrian Pedestrian:4 0.5 1.7 0.5 2.34 -1.56 0.0 1.57"
        parts = line.strip().split()
        assert parts[0] == "Pedestrian"
        assert parts[1] == "Pedestrian:4"
        assert float(parts[5]) == 2.34
        assert float(parts[6]) == -1.56
        assert float(parts[7]) == 0.0
 
    def test_person_id_extraction(self):
        #Checks we get num ID from Pedestrian:4 
        agent_id = "Pedestrian:4"
        person_id = int(agent_id.split(':')[-1])
        assert person_id == 4
 
    def test_timestamp_generation(self):
        #Checks timestamps are correct for 200frames at 10FPS
        num_frames = 200
        timestamps = [i * 0.1 for i in range(num_frames)]
        assert len(timestamps) == 200
        assert timestamps[0] == 0.0
        assert timestamps[1] == pytest.approx(0.1)
        assert timestamps[-1] == pytest.approx(19.9)
 