import sys
import os
import warnings
warnings.filterwarnings('ignore')
#appending dates to filenames
import datetime
import numpy as np
import logging
import re
import argparse
import glob
import boto3
import yaml
import pandas as pd
import pickle
import sklearn
from sklearn import model_selection
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import csv

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()

def prediction(path_to_model=None, sample_data=None):
	"""
	Predict a used car price
	Args:
		path_to_model (str): the path to the pickle file where model was saved
	Returns:
		None
		Prints the predicted price value
	"""
	logging.info('Predicting for a sample used car...')
	with open(path_to_model, 'rb') as f:
		fit = pickle.load(f)
	logging.info('* Model successfully loaded')
	logging.info('Loading sample data for prediction...')
	#read in a csv file to make prediction
	sample = pd.read_csv(sample_data)
	logging.info('Predicting price with the sample car...')
	#predicted result is a numpy array, index 0 to get price value
	pred_price = int(round(0.66*10** fit.predict(sample[0:1])[0]))
	logging.info('The predicted price for this sample car is: $%i' % pred_price)
	return pred_price
	
def run_predicting(args):
	"""Run prediction function"""
	with open(args.config, 'r') as f:
		config = yaml.load(f)
	return prediction(path_to_model = config['prediction']['prediction']['path_to_model'],
						sample_data = config['prediction']['prediction']['sample_data'])


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="make price prediction for a sample car")
	parser.add_argument('--config', default = 'config/car_config.yml', help = 'Path to yaml file with configurations')
	parser.add_argument('--input', default = None, help = 'path to input csv file')
	parser.add_argument('--output', default = None, help = 'path to output csv file')

	args = parser.parse_args()
	# features = run_generate(args)
	# fit = run_training(args)
	run_predicting(args)

