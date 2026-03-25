import numpy as np

class TrajProcess:
    def __init__(self, position_threshold=0.01):
        self.threshold = position_threshold
        print(f"Preprocessor initalised (threshold: {position_threshold}m)")
    def compute_velocity(self, positions, times):
        velocities = []

        for i in range(len(positions) - 1):
            dx = positions[i+1][0] - positions[i][0]
            dy = positions[i+1][1] - positions[i][1]
            dz = positions[i+1][2] - positions[i][2]

            dt = times[i+1] - times[i]
            if dt == 0:
                dt = 0.000001
            
            vx = dx / dt
            vy = dy / dt
            vz = dz / dt

            velocities.append([vx, vy, vz])

        if velocities:
            velocities.insert(0, velocities[0])
        else:
            velocities = [[0,0,0,]]

        return velocities
    
    def compute_orientation(self, positions):

        orientations = []

        for i in range(len(positions) - 1):
            dx = positions[i+1][0] - positions[i][0]
            dy = positions[i+1][1] - positions[i][1]
            angle = np.arctan2(dy,dx)
            orientations.append(angle)
        
        if orientations:
            orientations.insert(0, orientations[0])
        else:
            orientations = [0.0]
        
        return orientations
    
    def clean_duplicates(self, positions, times):
        if len(positions) == 0:
            return positions, times
        keep = [True]
        for i in range(1, len(positions)):
            prev = positions[i-1]
            curr = positions[i]

            dx = curr[0] - prev[0]
            dy = curr[1] - prev[1]
            dz = curr[2] - prev[2]
            distance = np.sqrt(dx**2 + dy**2 + dz**2)

            if distance > self.threshold:
                keep.append(True)
            else:
                keep.append(False)
            

        clean_pos = [positions[i] for i in range(len(positions)) if keep[i]]
        clean_times = [times[i] for i in range (len(times)) if keep[i]]

        return clean_pos, clean_times