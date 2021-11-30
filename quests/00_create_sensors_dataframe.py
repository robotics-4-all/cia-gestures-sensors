# Imports
import os
import json
import pandas as pd
from tqdm import tqdm

# Parameters
json_files_path = 'D:\_Projects_\Thesis_ContinuousImplicitAuthentication\Datasets\BrainRun\sensors_data'
gestures_database_name = 'BrainRun_GestureDevicesUsersGames'

screens = ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']
sensors = ['accelerometer', 'gyroscope']
sample_rate = 100  # ms

save_path = os.path.join(os.path.dirname(__file__), '00_sensors_data.csv')

# Thread
sensors_data = pd.DataFrame()

json_files = [pos_json for pos_json in os.listdir(json_files_path) if pos_json.endswith('.json')]
for json_file in tqdm(json_files):

    user = json_file.replace('.json', '').split('_')[0]
    timestamp = int(json_file.replace('.json', '').split('_')[1])

    with open(os.path.join(json_files_path, json_file)) as js:
        json_text = json.load(js)

        for sensor in sensors:
            for idx, sample in enumerate(json_text[sensor]):
                for screen in screens:
                    if screen in sample['screen']:

                        df_row = {
                            'user': user,
                            'screen': sample['screen'],
                            'sensor': sensor[0:3],
                            'timestamp': timestamp,
                            'realtime': timestamp + idx * sample_rate,
                            'x': sample['x'],
                            'y': sample['y'],
                            'z': sample['z']
                        }

                        sensors_data = sensors_data.append(df_row, ignore_index=True)
                        break

sensors_data.to_csv(save_path, index=False)
