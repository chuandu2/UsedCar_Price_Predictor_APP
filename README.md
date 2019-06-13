## **Developer**: [Sophie Du](https://github.com/chuandu2)
### **QA**: Kejin (Karen) Qian
----------------------------------------------------------------

The APP is running on http://18.222.209.147:3000/ until June 16, 2019 (Try it without cloning this repo before the date.)

# Outline
<!-- toc -->

- [Project Charter](#project-charter)
- [Project Backlog](#project-backlog)
- [Repo Structure](#repo-structure)
- [Documentation](#documentation)
- [Running the application](#running-the-application)
  * [Set up environment](#1-set-up-environment)
    + [With `virtualenv` and `pip`](#with-virtualenv)
    + [With `conda`](#with-conda)
  * [Configure Flask app](#2-configure-flask-app)
  * [Initialize the database](#3-initialize-the-database)
  * [Reproduce Model Development](#reproduce-model-development)
  * [Run the application](#4-run-the-application)
  * [Interact with the application](#5-interact-with-the-application)
- [Testing](#testing)
- [Work Cited](#work-cited)

<!-- tocstop -->

## Project Charter 

**Vision**: To predict used car prices based on user inputs of 8 significant car features

**Mission**: Enable users to input features of the used cars they want to buy or sell (car age, vehicle type, fuel type, miles etc.) and evaluate the car price based on their entries.

**Success criteria**:
- (Business) Users can clearly understand the meanings of the features that need inputs, and successfully get predicted used car values within 10 seconds each time based on their entries.
- (Machine Learning) Optimize the predictive model for predicting the used car prices to achieve Mean Square Error (MSE) lower than 0.1 and R-squared value greater than 75%.

## Project Backlog

**Theme 1**

The 1st theme of this project is to explore the historical data of used cars including the features that determine the values of the cars, and construct predictive models for predicting used car prices based on user inputs by trying diverse models (linear model, regularized regression models, tree models) and selecting the final model with best performance for later use in the WebApp.

**Epics**

**Epic 1: Exploratory Data Analysis**

In this section, data manipulations will be performed to explore the relationships among variables and determine the subset of variables to be included in the predictive models.

<*Stories*>

*  *Data Overview:* drop useless columns, check descriptive statistics of variables, do visualizations to see distributions of variables and detect outliers and skewness. (1 point)
* *Data Cleansing:* remove unwanted observations (duplicated and irrelevant), fix structural errors (typos or inconsistent capitalization), filter outliers, and impute or remove missing values (numeric and categorical). (2 points)

**Epic 2: Feature Engineering** *(planned for next 2 weeks)*

In this section, new features will be created based on interactions and correlations among existed variables.

<*Stories*>

* *Variable Relationships:* check correlations among variables and detect multicollinearity. (1 point)
*  *Feature Creation:* create interaction features (products, sums, differences, etc.), combine sparse classes for categorical variables by grouping similar classes, add dummy variables based on necessity, and remove unused features. (2 points)

<*Ice Box*>

* Categorize the used cars by sellers and compare if there exists significant difference among the sellers for the used cars they sell.
* Set price thresholds and label the used cars with price levels (1: x<5000, 2: 5000<=x<10000, etc.) to see the common features of the used cars within the same price level and compare across different price levels.

**Epic 3: Model Construction**

In this section, different models will be built based on the cleaned data for predicting used car prices, and important features for predicting prices will be determined, which will be used as user inputs for the user engagement on the WebApp.

<*Stories*>

* *Data Preparation:* split the data into training data and testing data. (0 point) 
* *Initial Model Selection:*  besides the most basic linear regression model, several effective machine learning algorithms for regression tasks will be trained on the training data, including regularized regression models (Lasso, Ridge, Elastic-Net) and tree models (Decision Tree, Random Forests, Boosted Trees). (1 points)
* *Fit & Tune Models:* for each model, for each set of selected parameters, perform 10-fold cross-validation using the training set and calculate the cross-validation error. (4 points)
* *Find Model Representatives:* for each model, check the set of parameter values which yields the lowest cross-validation errors, so that the representatives for each type of the potential models with their corresponding best parameters have been selected. (1 point)

**Epic 4: Model Performances & Evaluations**

In this section, the best model among all models for predicting used car prices will be selected through performance evaluations and comparisons.

<*Stories*>

* *Performance Metrics:* for each representative model, predict on the testing set. Calculate performance metrics (MSE: Mean Squared Error will be used, the lower the better) for the predictions, and choose the best model. (2-4 points)
* *Final Model Selection:* The model with the lowest MSE among all representative models will be selected as the best model to predict used car values in the WebApp. The interpretability of the model will also be considered as choosing the best predictive model. (2 points)

<*Ice Box*>

* 10 replicates of 10-fold cross validation will be performed on the representative models so that the predictive power of each model can be assessed using the same partition of cross-validation, and the final best model with lowest cross-validation error will be selected as the final model. 

**Theme 2**

The 2nd theme of this project is to build a WebApp which enables users to predict used car prices based on their inputs for related features, including the backend data infrastructure, UI design and testing.

**WebApp Building**

<*Stories*>

* Web app UI design
* Deploy the web app (Flask) on AWS
* Create database on local and RDS
* Testing (Unit tests on each function and Configured reproducibility testsc)

## Repo Structure

```
├── README.md                         <- You are here
│
├── config
│   ├── car_config.yml                <- YAML configuration
│   │  
│   ├── logging                       <- Folder holding logging configuratins
│
├── data                              <- Folder that will contain acquired data and generated data
│   ├── autos.csv                     <- Original dataset downloaded online after running 'src/get_data.py'
│   │
│   ├── features.csv                  <- Features generated after running 'src/generate_features.py'
│   │
│   ├── sample_usedCar.csv	           <- A sample car data generated after running 'src/add_sample.py' 
│
│
├── models                            <- Folder that contains trained model
│
├── slides                            <- Folder that contains presentation decks (midpoint and final)
│
├── src                               <- Source data for the project.
│   ├── get_data.py                   <- Script for downloading data from online source and basic cleaning
│   │  
│   ├── uploadData.py                 <- Script for uploading data to a specific busket (can be private)  
│   │ 
│   ├── generate_features.py          <- Script for generating features  
│   │ 
│   ├── train_model.py                <- Script for model training   
│   │ 
│   ├── evaluate_model.py             <- Script for model performance evaluation
│   │    
│   ├── run.py                        <- Script for running the pipeline from get_data to evaluate_model
│   │    
│   ├── add_sample.py                 <- Script for adding entry for prediction 
│   │    
│   ├── prediction.py                 <- Script for predicting price with sample in 'data/sample_usedCar.csv'
│   │    
│   ├── sql			                        <- Folder contains SQL source code
│        │  
│        ├── model.py                       <- Script for creating database (Local or RDS)
│        │   
│        ├── usedCar_pricePrediction.db    	<- databased created in local
│        │ 
│        ├── logfile                  		    <- Logfile for database updates  
│
├── static                            <- Folder contains images for the web pages
│
├── templates                         <- Folder contains html files
│
├── test                              <- Files necessary for running model tests
│
├── .gitignore                        <- Specifies intentionally untracked files to ignore
│
├── Makefile                          <- Make file for reproduction
│
├── app.py                            <- Flask wrapper for running the model 
│
├── config.py                         <- Configuration file for Flask app
│
├── requirements.txt                  <- Python package dependencies
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Documentation

* Open up `docs/build/html/index.html` to see Sphinx documentation docs. 
* See `src/README.md` for documentations for each step in the pipeline.
* See `README.md` for all updated documentations for developing and deploying the app.

## Running the application

### 1. Set up environment

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways.

First, `cd <path_to_repo>`

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv usedcar

source usedcar/bin/activate

pip install -r requirements.txt

```

#### With `conda`

```bash
conda create -n usedcar python=3.7
conda activate usedcar
pip install -r requirements.txt
(optional): to solve Command 'pip' not found: conda install pip then pip install -r requirements.txt
```

### 2. Configure Flask app 

`config.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
SQLALCHEMY_DATABASE_URI # URL for database that contains bank customers
PORT = 3002  # What port to expose app on - CHANGE TO 3000 if running on RDS
HOST = "127.0.0.1" # Host IP for the app - CHANGE TO "0.0.0.0" if running on RDS
```

### 3. Initialize the database

To create a database in the local location configured in `config.py`, run:

    python src/sql/model.py

Note: the default setting is `--RDS==False`

To set up environment variable SQLALCHEMY_DATABASE_URI (URL for database that contains bank customers) from command line in the main project repository:
 ```bash
 Run locally: export SQLALCHEMY_DATABASE_URI='sqlite:///src/sql/usedCar_pricePrediction.db'
 Run on RDS: export SQLALCHEMY_DATABASE_URI="{conn_type}://{user}:{password}@{host}:{port}/{DATABASE_NAME}"
 ```
 
## 4. Reproduce Model Development

Note: This step is neccessary, since the dataset is quite large and the model pickle is larger than 60MB, so it can't be saved in Github and thus needs to be reproduced.

To reproduce the whole model development process in local using Makefile, run following from command line in the main project repository:

```bash
make all
```

### 5. Run the application 

Run:

    python app.py

:bulb: Tip:
When getting the following error:

    OSError: [Errno 8] Exec format error
Please add the following line at the very beginning of `app.py`:

    #!/usr/bin/env python

### 6. Interact with the application

Go to [http://127.0.0.1:3002/](http://127.0.0.1:3002/) to interact with the current LOCAL version of the app.

## Testing

`cd` to the main project repository, then run `python test/test.py` from command line. 8 tests will be running including both good entry tests and bad entry tests.

## Work Cited

* Template credit to W3Schools: https://www.w3schools.com/w3css/tryw3css_templates_parallax.htm
* General HTML credit to Colorlib https://colorlib.com/wp/template/
* Main page Car image from http://crispme.com/wp-content/uploads/2015/07/The-Best-Vintage-Car-Wallpapers-23.jpg
* Prediction page side images from 
   - [Car mirror](http://image.baidu.com/search/detail?ct=503316480&z=&tn=baiduimagedetail&ipn=d&word=%E8%80%81%E7%88%B7%E8%BD%A6%E5%90%8E%E8%A7%86%E9%95%9C&step_word=&ie=utf-8&in=&cl=2&lm=-1&st=-1&hd=&latest=&copyright=&cs=734067906,3079807821&os=1882614368,111343973&simid=0,0&pn=70&rn=1&di=111220&ln=1317&fr=&fmq=1559851151763_R&fm=result&ic=&s=undefined&se=&sme=&tab=0&width=&height=&face=undefined&is=0,0&istype=2&ist=&jit=&bdtype=15&spn=0&pi=0&gsm=1e&objurl=http%3A%2F%2Fdpic.tiankong.com%2Fmc%2Fx3%2FQJ8382609643.jpg&rpstart=0&rpnum=0&adpicid=0&force=undefined&ctd=1559851211779^3_1229X617%1)
  - [Car front light](https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwjB0vj6-OTiAhVmU98KHbY7BQcQjRx6BAgBEAU&url=https%3A%2F%2Fwww.52112.com%2Fsearch%2F%25E8%2580%2581%25E7%2588%25B7%25E8%25BD%25A6.html&psig=AOvVaw2djtUCcQF7gvgPZEpTRTeV&ust=1560463208818315) (Credit to: Mariusz Blach - Fotolia)
  - [Car steering wheel](https://www.wix.com/website-template/view/html/1732?siteId=648ae4f3-0bc8-46c6-becc-8bbf3ccc2ab3&metaSiteId=cb21959b-8635-4fa8-9fd7-b85fe6cd7f3c&originUrl=https%3A%2F%2Fwww.wix.com%2Fwebsite%2Ftemplates)
