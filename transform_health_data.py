"""
This python script takes the export.xml data file and converts the data to csv.
"""

import pandas as pd
import os
import re
import xml.etree.ElementTree as ET


DATA_EXPORT_DIR = 'Data/Apple Health Data Export'

data_file_path = os.path.join(DATA_EXPORT_DIR, 'export.xml')

# Get the XML Tree and Root (Health Data section).
xml_tree = ET.parse(data_file_path)
health_data = xml_tree.getroot()

records = health_data.findall('Record')

# Intiate dataframe
data = pd.DataFrame(columns=['record_type','source_name','unit','creation_date','start_date','end_date','value','meta.key','meta.value'])

for i, record in enumerate(records):
	print(f'{i}/{len(records)}')

	data = data.append(
		{
			'record_type': record.get('type'),
			'source_name': record.get('sourceName'),
			'unit': record.get('unit'),
			'creation_date': record.get('creationDate'),
			'start_date': record.get('startDate'),
			'end_date': record.get('endDate'),
			'value': record.get('value'),
			'meta.key': record.find('MetadataEntry').get('key') if len(record.findall('MetadataEntry')) else None,
			'meta.value': record.find('MetadataEntry').get('value') if len(record.findall('MetadataEntry')) else None
		}, ignore_index=True
	)

data.to_csv('Data/Transformed Data/health_data.csv')

	
