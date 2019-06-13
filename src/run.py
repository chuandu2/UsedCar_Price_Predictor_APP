import argparse
import yaml
from get_data import run_getting
from generate_features import run_generate
from train_model import run_training
from evaluate_model import run_evaluate

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="get_feature_model_eval")
	parser.add_argument('--config', default = 'config/car_config.yml', help = 'Path to yaml file with configurations')
	parser.add_argument('--input', default = None, help = 'path to input csv file')
	parser.add_argument('--output', default = None, help = 'path to output csv file')

	args = parser.parse_args()

	with open(args.config, 'r') as f:
		config = yaml.load(f)

	#get data
	run_getting(args)
	#generate features
	features= run_generate(args)
	#train model
	fit = run_training(args)
	#evaluate model
	run_evaluate(args)