#here we define commom functionalities which the entire project can use
import os
import sys
import numpy as np
import pandas as pd
import dill as pickle
from src.exception import CustomException
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
def save_object(file_path, obj):
    #obj can be model, preprocessor, encoder, scaler, etc.
    try:
        dir_path= os.path.dirname(file_path)# this line will extract the directory path from the file path. For example, if the file path is "artifacts/preprocessor.pkl", the directory path will be "artifacts"
        os.makedirs(dir_path, exist_ok=True)# this line will create the directory if it doesn't exist. The exist_ok=True parameter means that if the directory already exists, it will not raise an error
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)# this line will save the object in the file path specified in the file_path variable. The "wb" parameter means that the file will be opened in write binary mode
    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report={}
        for i in range(len(list(models))):
            model = list(models.values())[i]# this line will extract the model from the models dictionary.
            para= param[list(models.keys())[i]]# this line will extract the parameters for the model from the param dictionary.
            gs = GridSearchCV(model, para, cv=3)# this line will create a GridSearchCV object for the model and the parameters.
            gs.fit(X_train, y_train)# this line will fit the GridSearchCV object to the training data.

            model.set_params(**gs.best_params_)# this line will set the parameters of the model to the best parameters found by the GridSearchCV object.
            model.fit(X_train, y_train)# this line will fit the model to the training data

            y_train_pred = model.predict(X_train)# this line will predict the target variable for the training data.
            train_model_score = r2_score(y_train, y_train_pred)# this line will calculate the R2 score for the training data.
            y_test_pred = model.predict(X_test)# this line will predict the target variable for the test data.
            test_model_score = r2_score(y_test, y_test_pred)# this line will calculate
            report[list(models.keys())[i]] = test_model_score# this line will add the test model score to the report dictionary with the model name as the key.
        return report
    except Exception as e:
        raise CustomException(e, sys)