"""
Create date: 05/26/19
@author: SophieDu
"""
import sys
#sys.path.append('')
import os
import json
import warnings
warnings.filterwarnings('ignore')
#appending dates to filenames
import datetime
import numpy as np
import logging
import re
import argparse
import pickle
import glob
import boto3
import yaml
import pandas as pd
import math
import sklearn
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score, train_test_split

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()

#import functions from modules
#from generate_features import run_generate

def train_model(features=None, save_best_model_obj=None):
	"""
	Train model with random forest
	Args:
		features (:obj: list): a list of features
		save_best_model_obj (str): the path to save the model
	Return:
		fit (:obj: model): the fitted model with random forest
	"""

	#set up X and Y from features.csv
	logging.info('Loading features...')
	final_df = pd.read_csv(features)
	Y = np.log10(final_df['price'])
	X = final_df.drop(['price'], axis = 'columns', inplace = False)
	#Split into train and validation
	logging.info('Splitting train and test...')
	X_train, X_val, y_train, y_val = train_test_split(X, Y, test_size=0.33, random_state = 3)

	#set up model and parameters
	rf = RandomForestRegressor()

	"""
	Here GridSearch was used to set the optimal parameters for the regressor
	To simplify this process of training, only the selected best parameters are listed here,
	while other tried parameters are removed
	"""
	param_grid = { "criterion" : ["mse"]
              , "min_samples_leaf" : [3]
              , "min_samples_split" : [3]
              , "max_depth": [10]
              , "n_estimators": [500]}
	
	#try parameters and fit the model
	logging.info('Fitting and scoring Random Forest models...')
	gs = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=1)
	gs = gs.fit(X_train, y_train)
	bp = gs.best_params_
	logging.info('* Optimal parameters selected')

	#fit the final random forest with the best parameter
	logging.info('Fitting the final Random Forest model with best parameters...')
	fit = RandomForestRegressor(criterion=bp['criterion'],
                              min_samples_leaf=bp['min_samples_leaf'],
                              min_samples_split=bp['min_samples_split'],
                              max_depth=bp['max_depth'],
                              n_estimators=bp['n_estimators'])
	fit.fit(X_train, y_train)
	logging.info('* Best model fitted')
	#scoring the best model
	#logging.info('* Explained variance score: %.2f' % fit.score(X_val, y_val))

	#save model to pickle
	if save_best_model_obj is not None:
		with open(save_best_model_obj, 'wb') as s:
			pickle.dump(fit, s)
		logging.info('* Model saved to %s', save_best_model_obj)

	return fit


def run_training(args):
	with open(args.config, 'r') as f:
		config = yaml.load(f)
	return train_model(features = config['train_model']['train_model']['features'],
		save_best_model_obj = config['train_model']['train_model']['save_best_model_obj'])

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="fit random forest model based on training data")
	parser.add_argument('--config', default = 'config/car_config.yml', help = 'Path to yaml file with configurations')
	parser.add_argument('--input', default = None, help = 'path to input file')
	parser.add_argument('--output', default = None, help = 'path to output file')

	args = parser.parse_args()
	#features = run_generate(args)
	run_training(args)