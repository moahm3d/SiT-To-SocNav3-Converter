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
    



