.PHONY: all
all: run add_sample prediction

# install needed packages
install:
	pip install -r requirements.txt

# To reproduce the whole pipeline from acquiring data to model evaluation, combining `get_data + generate_features + train_model + evaluate_model`

run: config/car_config.yml
	python src/run.py

# To reproduce loading data from url, run `get_data`

get_data: config/car_config.yml
	python src/get_data.py

# To reproduce generating features from loaded data, run `generate_features`

generate_features: config/car_config.yml
	python src/generate_features.py

# To reproduce training model with selected features, run `train_model`

train_model: config/car_config.yml
	python src/train_model.py

# To reproduce evaluating model fitted from last step and get post process, run `evaluate_model`

evaluate_model: config/car_config.yml
	python src/evaluate_model.py

# To add a user input sample car for single prediction, run `add_sample`

add_sample:
	python src/add_sample.py

# To reproduce predicting price for a sample car, run `prediction`

prediction: config/car_config.yml
	python src/prediction.py

# to test the functions from acquiring data to model prediction, run `test`

test:
	pytest test/test.py

# To set up configuration for local database, run 'config'

config:
	python config.py

# To initialize a local database and add sample data inside it, run `database`

database:
	python src/sql/model.py

# To demo the app, run `app`

app:
	python app.py

# clean files that will not be used later

clean:
	rm -r usedcar
