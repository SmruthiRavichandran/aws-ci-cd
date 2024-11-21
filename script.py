
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, recall_score, f1_score
import sklearn
import joblib
import boto3
import pathlib
from io import StringIO
import argparse
import os
import pandas as pd
import numpy as np

# Model loading for inference
def model_fn(model_dir):
    clf = joblib.load(os.path.join(model_dir, "model.joblib"))
    return clf

if __name__ == "__main__":
    # Argument parsing
    print("[INFO] Extractiong arguments")
    parser = argparse.ArgumentParser()

    # Hyperparameters sent by the client are passed as command-line arguments to the script.
    #parser.add_argument("--n-estimators", type=int, default=100)
    parser.add_argument("--random_state", type=int, default=0)
    
   

    parser = argparse.ArgumentParser()
    parser.add_argument("--n-estimators", type=int, required=True)
    parser.add_argument("--max-depth", type=int, required=True)
    #parser.add_argument("--train", type=str, required=True)
    #parser.add_argument("--test", type=str, required=True)
    args = parser.parse_args()

    


    # Environment variables
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR"))
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN"))
    parser.add_argument("--test", type=str, default=os.environ.get("SM_CHANNEL_TEST"))
    parser.add_argument("--train-file", type=str, default="trainx_v_1.csv")
    parser.add_argument("--test-file", type=str, default="testx_v_1.csv")
    print("Arguments received:")
    print(args)

    args, _ = parser.parse_known_args()
    
    print("SKlearn  version:", sklearn.__version__)
    print("Joblib version:", joblib.__version__)
    
    print("[INFO] Reading data")
    train_data = pd.read_csv(os.path.join(args.train, args.train_file))
    test_data = pd.read_csv(os.path.join(args.test, args.test_file))
    
    features = list(train_data.columns)
    label =  features.pop(-7)
    
    print("Building training and testing datasets")
    print()
    X_train = train_data[features]
    X_test = test_data[features]
    y_train = train_data[label]
    y_test = test_data[label]
    
    print("Column order:")
    print(features)
    print()
    
    print("Label column:",label)
    print()
    print("Training data shape:")
    print()
    print("---SHAPE OF TRAINING DATA 70%---")
    print(X_train.shape)
    print(y_train.shape)
    print()
    print("---SHAPE OF TESTING DATA 30%---")
    print(X_test.shape)
    print(y_test.shape)
    print()
    
    print("Training randoom forest model")
    print()
    model = RandomForestClassifier(n_estimators=args.n_estimators, random_state=args.random_state, verbose=1)
    model.fit(X_train, y_train)
    print("Model training completed")
    print()
    
    model_path = os.path.join(args.model_dir, "model.joblib")
    joblib.dump(model, model_path)
    print("Model persisted in " + model_path)
    print()
    
    y_pred_test = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred_test)
    test_repoort = classification_report(y_test, y_pred_test)
    print()
    
    print("---METRICS RESULT OF TESTING DATA---")
    print()
    print("total rows are: ", X_test.shape[0])
    print('[TESTING], Model accuracy: ', test_accuracy)
    print('[TESTING], Testing Report: ', test_repoort)
    
    
        
    



   
