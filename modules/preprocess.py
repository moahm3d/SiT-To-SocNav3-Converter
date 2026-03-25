import numpy as np

class TrajProcess:
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
