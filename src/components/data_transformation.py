# aim to get whatever input from data ingestion and do transformation on it and then save it in the feature store
#feature enegeniering and data cleaning will be done in this component
import os
import sys
from dataclasses import dataclass

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()#creating an object of the data transformation config class to access the path where we will save the preprocessor object)
    
    def get_data_transformer_object(self):
        #responsible for data transformation
        try:
            numerical_columns=['writing_score','reading_score']
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]
            num_pipeline= Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")), # this will fill the missing values with the median value of the column
                    ("scaler",StandardScaler()), # this will scale the numerical columns
                ]
            )  
            cat_pipeline= Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")), # this will fill the missing values with the most frequent value of the column
                    ("one_hot_encoder",OneHotEncoder()), # this will encode the categorical columns into numerical columns
                    ("scaler",StandardScaler(with_mean=False)), # this will scale the categorical columns
                ]
            )
            logging.info(f"numerical columns: {numerical_columns}")
            logging.info(f"categorical columns: {categorical_columns}")
            preprocessor= ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns),
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("read train and test data completed")
            logging.info("obtaining preprocessor object")

            preprocessor_obj = self.get_data_transformer_object() 
            target_column_name="math_score"
            numerical_columns=['writing_score','reading_score']

            input_feature_train_df=train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info("applying preprocessing object on training and testing dataframe")

            input_feature_train_arr= preprocessor_obj.fit_transform(input_feature_train_df)#the fit_transfrom machi bach nlearniw walkain bachc nwjdo data 
            input_feature_test_arr= preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj
            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except  Exception as e:
            CustomException(e, sys)