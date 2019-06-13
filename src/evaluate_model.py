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

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()

#import functions
from generate_features import run_generate
from train_model import run_training


def evaluate_model(path_to_model=None, features=None):
	"""
	Evaluate model performance
	Args:
		path_to_model (str): the path to the pickle file where model was saved
	Returns:
		None
		prints result in a text file named 'Evaluation.txt' in models folder
	"""
	#load best model
	logging.info('Loading model...')
	with open(path_to_model, 'rb') as f:
		fit = pickle.load(f)
	logging.info('* Model successfully loaded')
	#load data
	logging.info('Loading testing data...')
	final_df = pd.read_csv(features)
	Y = np.log10(final_df['price'])
	X = final_df.drop(['price'], axis = 'columns', inplace = False)
	X_train, X_val, y_train, y_val = train_test_split(X, Y, test_size=0.33, random_state = 3)

	#predict with X_test
	logging.info('Predicting with testing data...')
	y_pred = fit.predict(X_val)
	logging.info('* Prediction done')
	logging.info('Scoring model...')
	MSE = mean_squared_error(y_val, y_pred)
	r2 = r2_score(y_val, y_pred)

	#print evaluation
	logging.info('* Mean squared error: %.3f' % round(MSE, 3))
	logging.info('* Explained variance score (R^2): %.2f' % round(r2, 2))

	#with open('Evaluation.txt', 'w+') as text_file:
	text_file = open("models/Evaluation.txt","w+")
	text_file.write('-----------Evaluation for Random Forest Model-----------')
	text_file.write('\n')
	text_file.write('* Mean squared error: %.3f' % round(MSE, 3))
	text_file.write('\n')
	text_file.write('* Explained variance score (R^2): %.2f' % round(r2, 2))
	text_file.close()
	logging.info('* Evaluation results saved in "Evaluation.txt" in models folder')


def run_evaluate(args):
	"""Run evaluation model function"""
	with open(args.config, 'r') as f:
		config = yaml.load(f)
	return evaluate_model(path_to_model = config['evaluate_model']['evaluate_model']['path_to_model'],
							features = config['evaluate_model']['evaluate_model']['features'])


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="evaluate random forest model")
	parser.add_argument('--config', default = 'config/car_config.yml', help = 'Path to yaml file with configurations')
	parser.add_argument('--input', default = None, help = 'path to input csv file')
	parser.add_argument('--output', default = None, help = 'path to output csv file')

	args = parser.parse_args()
	# features = run_generate(args)
	# fit = run_training(args)
	run_evaluate(args)

	