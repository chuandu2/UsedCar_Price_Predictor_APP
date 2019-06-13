import os

DEBUG = True
LOGGING_CONFIG = 'config/logging/local.conf'
PORT = 3002
APP_NAME = 'usedCar-pricePredictor'


# local: export SQLALCHEMY_DATABASE_URI='sqlite:///src/sql/price_prediction.db'
# rds: export SQLALCHEMY_DATABASE_URI='{conn_type}://{user}:{password}@{host}:{port}/{DATABASE_NAME}''

#SQLALCHEMY_DATABASE_URI='sqlite:///src/sql/usedCar_pricePrediction.db'
#SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, DATABASE_NAME)

SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI")
conn_type = 'mysql+pymysql'
user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
host = os.environ.get('MYSQL_HOST')
port = os.environ.get('MYSQL_PORT')
DATABASE_NAME = 'msia423'
print(SQLALCHEMY_DATABASE_URI)
SQLALCHEMY_DATABASE_URI =SQLALCHEMY_DATABASE_URI.format(conn_type=conn_type, user=user, password=password, host=host, port=port, DATABASE_NAME=DATABASE_NAME)

SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = '127.0.0.1'
MAX_ROWS_SHOW = 30
PATH_TO_MODEL = 'models/price_prediction_model.pkl'
