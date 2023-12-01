from Insurance.pipeline.batch_prediction import start_batch_prediction
#from Insurance.pipeline.training_pipeline import start_training_pipeline
#from Insurance.components.model_trainer import start_training_pipeline

file_path=r"C:\Users\SRIRAM SRIPADA\Downloads\Project-EWB-final-main\Project-EWB-final-main\artifact\02122023__032919\data_ingestion\feature_store\insurance.csv"

print(__name__)
if __name__=="__main__":
    try:
        #output_file = start_training_pipeline()
        output_file = start_batch_prediction(input_file_path=file_path)
        print(output_file)
    except Exception as e:
        print(e)