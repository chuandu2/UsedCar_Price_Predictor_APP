"""
Created on 5/25/19
@author: SophieDu
"""
import sys
import os
import json
import warnings
warnings.filterwarnings('ignore')
#appending dates to filenames
import datetime
import re
import argparse
import glob
import boto3
import yaml
import pandas as pd
import numpy as np
import math
import sklearn
from sklearn import preprocessing
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()

#get data from github link
def get_data(url=None):
	"""
	Get data from online url
	Updates: this function has been merged with the cleanData.py
	Args:
		read_path (Str): the url to the online data
		save_path (Str): the directory to save the downloaded data
	Return:
		None
		cleaned Data saved as a csv in the save_path
	"""
	logging.info('Downloading data from online url...')

	df = pd.read_csv(url, sep = ',', header = 0, encoding = 'cp1252')
	logging.info('* Used car data downloaded from online url')
	logging.info('Cleaning data...')

	#drop columns above, also unuseful dates
	df = df.drop(['abtest', 'offerType', 'nrOfPictures', 'postalCode',
	          'dateCrawled', 'dateCreated', 'lastSeen', 'seller'],
	         axis='columns')

	"""drop rows with missings"""
	df = df.dropna()

	"""drop duplicates"""
	df = df.drop_duplicates(['name', 'price', 'vehicleType', 'yearOfRegistration',
                        'gearbox', 'powerPS', 'model', 'kilometer',
                        'monthOfRegistration', 'fuelType', 'brand', 'notRepairedDamage'])

	"""clean outliers for cars too old, extremely high and low prices and power"""
	df = df[(df.yearOfRegistration >= 1999)
	& (df.price >= 1500) & (df.price <= 100000) 
    & (df.powerPS >= 10) & (df.powerPS <= 500)]

    #replace German Yes & No
	df['notRepairedDamage'] = df['notRepairedDamage'].replace(['ja', 'nein'], ['Yes', 'No'])
	#rename column to reduce confusion, notrepairedDamage = yes -> exists damage
	df = df.rename(columns = {'notRepairedDamage': 'damageExist'})

	logging.info('* Data is clean')
	logging.info('Saving csv to data file...')

	df.to_csv('data/autos.csv', index = None, header = True)
	logging.info('* Data saved as "autos.csv" in data file')
	return df

def run_getting(args):
	with open(args.config, 'r') as f:
		config = yaml.load(f)
	config_clean = config['get_data']
	df = get_data(**config_clean['get_data'])
	df.to_csv(args.output, index = False)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="download CSV from online url")
	parser.add_argument('--config', default = 'config/car_config.yml', help = 'Path to yaml file with configurations')
	parser.add_argument('--input', default = None, help = 'path to input csv file')
	parser.add_argument('--output', default = None, help = 'path to output csv file')

	args = parser.parse_args()
	run_getting(args)