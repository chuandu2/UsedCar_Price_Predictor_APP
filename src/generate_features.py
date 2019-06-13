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

def generate_features(csv_file=None):
	"""
	Generate features for modeling
	Args:
		csv_file (str): `clouds.csv`, got from load_csv function from online url
		columns (:obj: `list`):  List of features to extract
	Returns:
		features (:py:class: `pd.DataFrame`): a new dataframe with selected variables and new features
	"""

	logging.info('Reading in data...')
	df = pd.read_csv(csv_file)
	logging.info('* Car data successfully loaded')
	
	logging.info('Building features...')
	"""Define rare models with sample sizes less than 90% of all models"""
	models = df.model
	rare_models = []
	model_count = df.groupby('model').size()
	
	#check lower 10% sample sizes
	low_model_size = np.percentile(np.array(model_count), 10)
	for m in models: 
	    #model size for model m
	    if model_count[m] <= low_model_size:
	        rare_models.append(m)

	rare_models = set(rare_models) #rare_models
	"""binary encoding for rare models"""
	df['rareModel'] = df.model.isin(rare_models).astype(int)
	#drop rare models
	df = df[df.rareModel == 0]
	#remove "rareModel" column since all models left are popular ones
	df = df.drop('rareModel', axis = 1)

	#feature engineering
	df['nameLength'] = [min(70, len(n)) for n in df['name']]

	"""
	Normalize labels (categorical variables)
	transform non-numerical labels to numerical labels and normalize
	"""
	labels = ['name', 'brand', 'model', 'gearbox', 'damageExist', 'fuelType', 'vehicleType']
	#label encoders
	les = {}

	for l in labels:
	    #set label encoder for all labels
	    les[l] = preprocessing.LabelEncoder()
	    #encode all non-numerical labels
	    les[l].fit(df[l])
	    tr = les[l].transform(df[l])
	    df.loc[:, l + '_feature'] = pd.Series(tr, index=df.index)
	    #print(les[l])

	#name length doesn't make sense to be used as a user input, so finally decide not to use
	features = df[['price','yearOfRegistration','powerPS','kilometer',
	               'monthOfRegistration']
	              + [x + "_feature" for x in labels]]

	features = features.drop(['name_feature'], axis = 'columns')

	# drop last 2 vars for low correlations
	features = features.drop(['monthOfRegistration', 'model_feature'], axis = 'columns')

	logging.info('* Features successfully built')
	logging.info('Saving features for model...')
	#save the cleaned data into a new csv file
	features.to_csv('data/features.csv', index = None, header = True)
	logging.info('* Features saved in "features.csv" in data file')


# def generate_target(csv_file=None):
# 	target = pd.read_csv(csv_file)['class']
# 	return target

def run_generate(args):
	with open(args.config, 'r') as f:
		config = yaml.load(f)

	config_generate = config['generate_features'] #this .py
	config_feature = config_generate['generate_features'] # feature function
	#config_target = config_generate['generate_target'] #target function

	features = generate_features(**config_feature)
	#target = generate_target(**config_target)
	return features #, target

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="used loaded csv to select and create features")
	parser.add_argument('--config', default = 'config/car_config.yml', help = 'Path to yaml file with configurations')
	parser.add_argument('--input', default = None, help = 'path to input csv file')
	parser.add_argument('--output', default = None, help = 'path to output csv file')

	args = parser.parse_args()

	run_generate(args)
