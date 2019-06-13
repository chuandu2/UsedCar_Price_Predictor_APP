# Documentation for Source Code of Pipeline

To run each of the step, first `cd` to the main project file

### get_data.py
- To cquire data from online source, run:

        python src/get_data.py
  
  - Args:
      - read_path (Str): the url to the online data
      - save_path (Str): the directory to save the downloaded data
      
  - Return:
      - None
      - Cleaned data saved as a csv in the save_path
      
      
### uploadData.py
To upload data to specific aws S3 bucket (can be private), run:

        python src/uploadData.py
  
  - Args:
      - --input_file_path: local file path for uploaded file
      - --bucket_name: s3 bucket name
      - --output_file_path: output file path in S3 for uploaded file
      
  - Return:
      - None
      - Data uploaded to S3 bucket


### generate_features.py
To generate features from 'data/autos.csv' for modeling, run:

        python src/generate_features.py
  
  - Args:
      - csv_file (str): `clouds.csv`, got from load_csv function from online url
      - columns (:obj: `list`):  List of features to extract
      
  - Return:
      - features (:py:class: `pd.DataFrame`): a new dataframe with selected variables and new features


### train_model.py
To train model with features using random forest model, run:

        python src/train_model.py
  
  - Args:
      - features (:obj: list): a list of features
      - save_best_model_obj (str): the path to save the model
      
  - Return:
      - fit (:obj: model): the fitted model with random forest


### evaluate_model.py
To evaluate model performance, run:

        python src/evaluate_model.py
  
  - Args:
      - path_to_model (str): the path to the pickle file where model was saved
      
  - Return:
      - None
      - prints result in a text file named 'Evaluation.txt' in models folder


### add_sample.py
To ADD USER INPUT for a used car to make single price prediction, run:

        python src/add_sample.py
  
  - Input:
      - user_input (:obj: list): a list of sample car features (CHANGE the values in the `user_input`)
  
  - Output:
      - 'sample_usedCar.csv': a csv file in 'data' folder containing the sample car data and will be taken into `prediction.py` for price prediction


### prediction.py
To predict a sample used car price (taken from user input in 'sample_usedCar.csv'), run:

        python src/prediction.py
  
  - Args:
      - path_to_model (str): the path to the pickle file where model was saved
 
  - Return:
      - None
      - The predicted price is saved in a txt file


### run.py
To reproduce the whole pipeline from acquiring data to model evaluation, combining `get_data + generate_features + train_model + evaluate_model`, run:

         python src/run.py
