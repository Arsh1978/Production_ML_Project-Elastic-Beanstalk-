#In data ingestion we will be reading the data from the source.

import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.componenets.data_transformation import DataTransformation
from src.componenets.data_transformation import DataTransformationConfig

from src.componenets.model_trainer import ModelTrainerConfig
from src.componenets.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:  #provides all the inputs needed for data ingestion component.
    train_data_path: str = os.path.join('artifacts',"train.csv")
    test_data_path: str = os.path.join('artifacts',"test.csv")
    raw_data_path: str = os.path.join('artifacts',"data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        #the about 3 paths will be saved in ingestion_config object as soon as we call the DataIngestion class.(sub objects)

    def initiate_data_ingestion(self):
        logging.info("Data ingestion has started")
        try:
            df = pd.read_csv('notebook\data\stud.csv') #instead of this we can read from api, database, cloud storage etc.
            logging.info('read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info('Train Test Split Initiated')

            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('Ingestion of data is Completed')

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )


        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    obj = DataIngestion()
    train_data,test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr,test_arr,_ = data_transformation.initiate_data_transformation(train_data, test_data)

    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))