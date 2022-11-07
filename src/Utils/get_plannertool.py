# Download Plannertool 

import requests
import pandas as pd
import os

USER = os.getlogin()
# Appending &download=1 to the link forces it to download
#url = 'https://healthybrainstudy-my.sharepoint.com/:x:/g/personal/verkroost_hbs365_nl/EUNn8BpHGYJJkqdG6MaTUgoBxDQ2Kpb2wzv5EsqpZ6843Q?rtime=g3w2n-9J2kg&download=1' # old
url = 'https://healthybrainstudy-my.sharepoint.com/:x:/g/personal/zonneveld_hbs365_nl/EXzvxQloqQ1Dgz0z-TswCQUB76PqjuZFqGul8T-5eZs81Q'
url = f'{url}?rtime=q3w2n-9J2kg&download=1'  # download=1 for downloading, and the rtime parameter seems to just work i dont know why
local_name = 'temp_plannertool.xlsx'
local_path = f'C:\\Users\\{USER}\\AppData\\Local\\Temp\\{local_name}'

def download_plannertool():
	""" Download the Plannertool file and store to disk """
	response = requests.get(url)
	with open(local_path, 'wb') as f:
		f.write(response.content)
		print(f'Plannertool downloaded: {f.name}')
	return
	

def read_plannertool():
	""" Loads the planner tool form disk and returns the 'Planning' sheet """
	df = pd.read_excel(local_path, sheet_name="Planning", header=12)
	df = df.dropna(subset = ['Participant'])
	return df
	




if __name__ == "__main__":	
	#download_plannertool()
	pt = read_plannertool(local_path)
	print('Done')