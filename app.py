from flask import render_template, request, redirect, url_for
import logging.config
#from app import db, app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pickle
import xgboost
import pandas as pd
import numpy as np
import traceback
from src.sql.model import pricePrediction

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from config.py
app.config.from_object('config')

# Define LOGGING_CONFIG in config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger()
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)
print(db)


@app.route('/')
def index():
    """Main view that lists songs in the database.
    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/index.html template.
    Returns: rendered html template
    """

    return render_template('index.html')


@app.route('/add', methods=['GET','POST'])
def add_entry():
    """
    This function collects user inputs and returns the price to the webpage
    """

    # get numerical data
    YEAR_OF_REGISTRATION = int(request.form['yearOfRegistration'])
    KILOMITER = 1.6 * int(request.form['mile'])
    POWER_PS = int(request.form['powerPS'])
    # get categorical data
    brand_feature = request.form['brand_feature']
    vehicleType_feature = request.form['vehicleType_feature']
    gearbox_feature = request.form['gearbox_feature']
    fuelType_feature = request.form['fuelType_feature']
    damageExist_feature = request.form['damageExist_feature']

    # filter for categories and assignments
    pair_brand = {'alfa_romeo':0, 'audi':1, 'bmw':2, 'chevrolet':3, 'chrysler':4,
        'citroen':5, 'dacia':6, 'daewoo':7, 'daihatsu':8, 'fiat':9, 'ford':10,
        'honda':11, 'hyundai':12, 'jaguar':13, 'jeep':14, 'kia':15,
        'lada':16, 'lancia':17, 'land_rover':18, 'mazda':19, 'mercedes_benz':20,
        'mini':21, 'mitsubishi':22, 'nissan':23, 'opel':24, 'peugeot':25,
        'porsche':26, 'renault':27, 'rover':28, 'saab':29, 'seat':30,
        'skoda':31, 'smart':32, 'subaru':33, 'suzuki':34, 'toyota':35,
        'volkswagen':36, 'volvo':37}
    for key in pair_brand:
        if brand_feature == key:
            CAR_BRAND = pair_brand[key]

    pair_vehicle = {'andere':0, 'bus':1, 'cabrio':2, 'coupe':3,
                'kleinwagen':4, 'kombi':5, 'limousine':6, 'suv':7}
    for key in pair_vehicle:
        if vehicleType_feature == key:
            VEHICLE_TYPE = pair_vehicle[key]

    GEARBOX_TYPE = 0 if gearbox_feature=='automatik' else 1

    pair_fuel = {'andere':0, 'benzin':1, 'cng':2, 'diesel':3,
             'elektro':4, 'hybrid':5, 'lpg':6}
    for key in pair_fuel:
        if fuelType_feature == key:
            FUEL_TYPE = pair_fuel[key]
    

    DAMAGE_EXIST = 0 if damageExist_feature=='No' else 1

    #load model for prediction
    path_to_tmo = 'models/price_prediction_model.pkl'
    with open(path_to_tmo, "rb") as f:
        model = pickle.load(f)

    # create predict df
    X = pd.DataFrame(columns=['YEAR_OF_REGISTRATION', 'POWER_PS', 'KILOMITER', 
        'CAR_BRAND', 'GEARBOX_TYPE', 'DAMAGE_EXIST', 'FUEL_TYPE', 'VEHICLE_TYPE'])

    X.loc[0] = [YEAR_OF_REGISTRATION, POWER_PS, KILOMITER, CAR_BRAND, GEARBOX_TYPE,
    DAMAGE_EXIST, FUEL_TYPE, VEHICLE_TYPE]

    # prediction
    pred_price = int(round(0.66 * 10 ** model.predict(X)[0]))

    #pred_prob = float(model.predict_proba(X)[:,1])

    #print(type(pred_prob))
    result = "  $" + str(pred_price)
   
    try:
        input1 = pricePrediction(
            yearOfRegistration = YEAR_OF_REGISTRATION,
            powerPS = POWER_PS,
            kilometer = KILOMITER,
            brand_feature = CAR_BRAND,
            gearbox_feature = GEARBOX_TYPE,
            damageExist_feature = DAMAGE_EXIST,
            fuelType_feature = FUEL_TYPE,
            vehicleType_feature = VEHICLE_TYPE,
            predicted_price = pred_price)
        db.session.add(input1)
        db.session.commit()
        logger.info("Used car price evaluation added: %s", result)
        return render_template('index.html', result=result)
    except:
        traceback.print_exc()
        logger.warning("Unable to show price evaluation, return to home page")
        return render_template('error.html', result = 'NO RESULT AVAILABLE')



if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
