"""
Created on 5/12/19

@author: SophieDu
"""
import os
import sys
import logging
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sql

import argparse

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()


Base = declarative_base()

class pricePrediction(Base):
    """Create a data model for the database to be set up for capturing car data """
    __tablename__ = 'usedCar_pricePrediction'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    #uid = Column(Integer,nullable=False)
    #INPUT features for user inputs (features model used)
    yearOfRegistration = Column(Integer,nullable=False, unique=False)
    powerPS = Column(Integer, nullable=False, unique=False)
    kilometer = Column(Integer, nullable=False, unique=False)
    brand_feature = Column(Integer, nullable=False, unique=False)
    gearbox_feature = Column(Integer, nullable=False, unique=False)
    damageExist_feature = Column(Integer, nullable=False, unique=False)
    fuelType_feature = Column(Integer, nullable=False, unique=False)
    vehicleType_feature = Column(Integer, nullable=False, unique=False)
    predicted_price = Column(Integer, nullable=False, unique=False)



def get_engine_string(RDS = False):
  """
    Get the engine string for RDS, get the path of sqlite database schema if RDS=False

    Args:
        RDS(boolean): Default is False.
            If False: create the database schema locally in sqlite
            If True: create the database schema in RDS
    Return:
        engine_string (Str): An engine string if RDS=True
                            Path to store sqlite if RDS=False
  """
  if RDS:
        logging.info('Creating database in RDS...')
        conn_type = "mysql+pymysql"
        user = os.environ.get("MYSQL_USER")
        password = os.environ.get("MYSQL_PASSWORD")
        host = os.environ.get("MYSQL_HOST")
        port = os.environ.get("MYSQL_PORT")
        DATABASE_NAME = 'msia423'
        engine_string = "{}://{}:{}@{}:{}/{}". \
            format(conn_type, user, password, host, port, DATABASE_NAME)
        # print(engine_string)
        #logging.debug("engine string: %s"%engine_string)
        return  engine_string
  else:
        logging.info('Creating database in local...')
        return 'sqlite:///src/sql/usedCar_pricePrediction.db' # consider relative path



def create_db(args,engine=None):
    """Creates a database with the data models inherited from `Base`.
    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`.
            If None, `engine` must be provided.

    Returns:
        None
    """
    if engine is None:
        RDS = eval(args.RDS) # evaluate string to bool
        logger.info("RDS:%s"%RDS)
        #create engine
        engine = sql.create_engine(get_engine_string(RDS = RDS))

    Base.metadata.create_all(engine)
    logger.info("Database created as 'usedCar_pricePrediction.db' in src/sql folder")

    return engine




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create defined tables in database")
    parser.add_argument("--RDS", default="False",help="True if want to create in RDS else None")
    args = parser.parse_args()
    
    engine = create_db(args)

    # create engine
    if args.RDS == True:
        engine = sql.create_engine(get_engine_string(RDS=args.RDS))
        
    # create a db session
    Session = sessionmaker(bind=engine)  
    session = Session()

    #insert a new user input
    input1 = pricePrediction(yearOfRegistration = 2015, powerPS = 177,
        kilometer=10500,brand_feature =14, gearbox_feature=0,damageExist_feature=0,
        fuelType_feature=4, vehicleType_feature =7, predicted_price = 22160)
    session.add(input1)
    session.commit()

    logger.info("Data added")

    query = "SELECT * FROM usedCar_pricePrediction"
    df = pd.read_sql(query, con=engine)
    logger.info(df)
    session.close()
