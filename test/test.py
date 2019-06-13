"""
Create date: 06/10/19
@author: SophieDu
"""
import os
import warnings
warnings.filterwarnings('ignore')
import sys
sys.path.insert(0, '../MSiA-ValueChain-WebApp-repo/src')
import pytest
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
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()

#import functions
from src.get_data import get_data
from src.generate_features import generate_features
from src.train_model import train_model
from src.evaluate_model import evaluate_model
from src.prediction import prediction


def test_get_data():
	logging.info('Testing data acquisition step...')
	#load downloaded data
	df = pd.read_csv('data/autos.csv')
	#length and columns to be tested
	df_len = len(df)
	df_col = list(df.columns)
	#desired clean data shape and columns
	test_df_len = 169963
	test_df_col = ['name','price','vehicleType','yearOfRegistration','gearbox',
	'powerPS','model','kilometer','monthOfRegistration','fuelType','brand','damageExist']
	#raise AssertError if the length of downloaded data doesn't match with length of original data
	assert (df_len == test_df_len)
	assert (df_col == test_df_col)

def test_generate_features():
	logging.info('Testing feature generation step...')
	#load csv which stored features
	features = pd.read_csv('data/features.csv')
	"""TEST LENGTH"""
	#length to be tested
	features_len = len(features)
	#desired features length
	test_flen = 169803

	"""TEST ENTRIES"""
	#feature columns to be tested
	feature_col = list(features.columns)
	#desired list of features
	feature_list = ['price', 'yearOfRegistration', 'powerPS', 'kilometer',
                'brand_feature', 'gearbox_feature', 'damageExist_feature', 
                'fuelType_feature', 'vehicleType_feature']
	#raise AssertError if the length of saved features doesn't match with length of actually generated features
	assert (features_len == test_flen)
	#raise AssertError if the columns in saved features don't match with the desired list of features
	assert (feature_col == feature_list)

def test_split_data():
	"""Test functionality of split training and testing data"""
	logging.info('Testing model training step...')
	#load features
	final_df = pd.read_csv('data/features.csv')
	Y = np.log10(final_df['price'])
	X = final_df.drop(['price'], axis = 'columns', inplace = False)
	#Split into train and validation
	X_train, X_val, y_train, y_val = train_test_split(X, Y, test_size=0.33, random_state = 3)
	#split data using split function
	#raise AssertError if training set has smaller length than testing set
	assert len(X_train) > 2 * len(X_val)
	assert len(y_train) > 2 * len(y_val)

	"""Test if X has dropped price column"""
	assert X_train.columns[0] != 'price'
	assert X_val.columns[0] != 'price'
	assert X_train.columns[0] == 'yearOfRegistration'
	assert X_val.columns[0] == 'yearOfRegistration'

def test_model_type():
	"""Test if train_model fitted is a random forest"""
	fit = train_model(features='test/test_data.csv',
		save_best_model_obj='test/test_model.pkl')
	#model type to be tested
	model_type = str(type(fit))
	#desired model type
	test_type = "<class 'sklearn.ensemble.forest.RandomForestRegressor'>"
	"""Test if fitted model type matches desired model type"""
	assert (model_type == test_type)


def test_evaluation():
	"""Test model evaluation result"""
	#load model fitted with test data
	with open('test/test_model.pkl','rb') as f:
		fit = pickle.load(f)
	#split data
	final_df = pd.read_csv('test/test_data.csv')
	Y = np.log10(final_df['price'])
	X = final_df.drop(['price'], axis = 'columns', inplace = False)
	#Split into train and validation
	X_train, X_val, y_train, y_val = train_test_split(X, Y, test_size=0.33, random_state = 3)
	#predict with test dataset
	y_pred = fit.predict(X_val)
	MSE = mean_squared_error(y_val, y_pred)
	r2 = r2_score(y_val, y_pred)
	#evaluation gives MSE and R2, check null
	assert MSE is not np.nan
	assert r2 is not np.nan
	#check value ranges
	assert (MSE.item() > 0) & (MSE.item() < 1)
	assert (r2.item() >= 0) & (r2.item() <= 1)

def test_evaluation_input_model():
	"""Test model evaluation with bad input"""
	with pytest.raises(ValueError) as excinfo1:
		with open('test/test_model.pkl','rb') as f:
			fit = pickle.load(f)

		#split data
		final_df = pd.read_csv('test/bad_test_data.csv')
		Y = np.log10(final_df['price'])
		X = final_df.drop(['price'], axis = 'columns', inplace = False)
		#Split into train and validation
		X_train, X_val, y_train, y_val = train_test_split(X, Y, test_size=0.33, random_state = 3)
		#predict with test dataset
		y_pred = fit.predict(X_val)
	assert str(excinfo1.value) == 'Number of features of the model must match the input. Model n_features is 8 and input n_features is 9 '

def test_prediction():
	"""Test prediction with one sample car"""
	pred = prediction(path_to_model='test/test_model.pkl', sample_data='test/one_sample.csv')
	#check value type, price should be integer
	assert (type(pred) is int) & (pred > 100)

def test_prediction_input():
	"""Test model prediction with bad input"""
	with pytest.raises(ValueError) as excinfo1:
		# test data input
		path_to_model = 'test/bad_test_model.pkl'
		sample_data='test/one_sample.csv'
		prediction(path_to_model, sample_data)

	assert str(excinfo1.value) == 'Number of features of the model must match the input. Model n_features is 9 and input n_features is 8 '
