"""
This python script takes the individual gpx (xml) files and consolidates them into csv.
"""

import pandas as pd
import os
import re
import xml.etree.ElementTree as ET


DATA_EXPORT_DIR = 'Data/Apple Health Data Export'


#--------------- Workout-Routes Data ----------------
WORKOUT_DIR = os.path.join(DATA_EXPORT_DIR,'workout-routes')

WORKOUT_FILE_LIST = os.listdir(WORKOUT_DIR)

def get_gpx_data_as_df(filepath):
    df = pd.DataFrame(columns=['workout_name','datetime','lon','lat','elev','speed','course','hAcc','vAcc'])
    if filepath is not None:
        xml_tree = ET.parse(filepath)
        root = xml_tree.getroot()
        rtag = root.tag
        namespace = re.search(r'\{(.*)\}', rtag).group(1) # between '{' '}'
        namespace = '{' + namespace + '}' # This is the schema of the data file... it is prepended to all tags within and so is needed when searching.
        trk = root.find(f'{namespace}trk')
        workout_name = trk.find(f'{namespace}name').text
        trkseg = trk.find(f'{namespace}trkseg')

        for trkpt in trkseg.findall(f'{namespace}trkpt'):
            df = df.append(
                {'workout_name':workout_name,
                 'datetime':trkpt.find(f'{namespace}time').text,
                 'lon':trkpt.get('lon'),
                 'lat':trkpt.get('lat'),
                 'elev':trkpt.find(f'{namespace}ele').text,
                 'speed':trkpt.find(f'.//{namespace}extensions/{namespace}speed').text,
                 'course':trkpt.find(f'.//{namespace}extensions/{namespace}course').text,
                 'hAcc':trkpt.find(f'.//{namespace}extensions/{namespace}hAcc').text,
                 'vAcc':trkpt.find(f'.//{namespace}extensions/{namespace}vAcc').text
                },ignore_index=True)

        df.datetime = pd.to_datetime(df.datetime)
        for col in df.columns:
            if col not in ('workout_name','datetime'):
                df[col] = pd.to_numeric(df[col])
    
    return df


workout_data = get_gpx_data_as_df(None) # Returns empty dataframe

WORKOUT_FILE_LIST = [x for x in WORKOUT_FILE_LIST if x.split('.')[-1] == 'gpx']	# Exludes the geojson files as they seem to be alternatives for a couple of workouts. The gpx file also exists for these.

for i, workout_file in enumerate(WORKOUT_FILE_LIST):
    rel_path = os.path.join(WORKOUT_DIR, workout_file)
    print(f'{i+1}/{len(WORKOUT_FILE_LIST)}', rel_path)
    
    workout_data = workout_data.append( get_gpx_data_as_df(rel_path), ignore_index=True )

workout_data.to_csv('Data/Transformed Data/workout-routes_data.csv')

