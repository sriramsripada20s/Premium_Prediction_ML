import numpy as np
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from Insurance.predictor import ModelResolver
import pandas as pd
from Insurance.utils import load_object
import os
import sys
from datetime import datetime

PREDICTION_DIR = "prediction"


def start_batch_prediction(input_file_path):
    try:
        # Create prediction directory if it doesn't exist
        os.makedirs(PREDICTION_DIR, exist_ok=True)

        # Log information about creating a model resolver object
        logging.info(f"Creating model resolver object")
        # During batch prediction, the model resolver selects the best model file from the 'saved_models' directory
        model_resolver = ModelResolver(model_registry="saved_models")

        # Log information about reading the input file
        logging.info(f"Reading file: {input_file_path}")
        # Load the data from the CSV file into a pandas DataFrame
        df = pd.read_csv(input_file_path)
        # Replace string 'na' with NaN values in the DataFrame
        df.replace({"na": np.NAN}, inplace=True)

        # Log information about loading the transformer to transform the dataset
        logging.info(f"Loading transformer to transform dataset")
        # Load the transformer (likely for feature transformation/scaling)
        transformer = load_object(file_path=model_resolver.get_latest_transformer_path())

       
        # Log information about using a target encoder to convert predicted column into categorical
        logging.info(f"Target encoder to convert predicted column into categorical")
        # Load the target encoder (probably for transforming predicted categorical values)
        target_encoder = load_object(file_path=model_resolver.get_latest_target_encoder_path())


        # Loop through input features to check and transform categorical variables
        input_feature_names = list(transformer.feature_names_in_)
        for i in input_feature_names:       
            if df[i].dtypes =='object':
                # Fit and transform categorical columns using the target encoder
                df[i] = target_encoder.fit_transform(df[i])
                    
        # Transform the input array using the loaded transformer
        input_arr = transformer.transform(df[input_feature_names])

        # Log information about loading the model for making predictions
        logging.info(f"Loading model to make prediction")
        # Load the model for prediction
        model = load_object(file_path=model_resolver.get_latest_model_path())
        # Make predictions using the loaded model on the transformed input array
        prediction = model.predict(input_arr)

        # Add the predictions to the DataFrame
        df["prediction"] = prediction


        # Generates a unique file name for prediction file based on the current date and time
        prediction_file_name = os.path.basename(input_file_path).replace(".csv", f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        # Create the full path for the prediction file
        prediction_file_path = os.path.join(PREDICTION_DIR, prediction_file_name)
        # Save the DataFrame with predictions to a CSV file without index and headers
        df.to_csv(prediction_file_path, index=False, header=True)
        
        # Return the path of the generated prediction file
        return prediction_file_path
    except Exception as e:
        # In case of any exception, raise an InsuranceException with the captured exception and system information
        raise InsuranceException(e, sys)


#This code seems to handle the entire process of loading a trained model, transforming input data, making predictions, 
# and saving the results to a CSV file, considering categorical encoding and transformations