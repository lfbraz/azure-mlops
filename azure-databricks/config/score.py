import tensorflow as tf
import json
import pandas as pd
import os

# Called when the deployed service starts
def init():
    global model
    global train_stats

    # Get the path where the deployed model can be found.
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), './models/')
    
    # Load keras
    model = tf.keras.models.load_model(model_path + 'model-regressao-tensorflow.h5')
    
    # Load train_stats
    train_stats = pd.read_pickle(model_path + "train_stats.pkl")

def norm(x):
  return (x - train_stats['mean']) / train_stats['std']

# Handle requests to the service
def run(data):
  # JSON request.
  # {"Cylinders":0, "Displacement":0.0, "Horsepower":0.0, "Weight":0.0, "Acceleration":0.5, "Model Year":0, "USA":0.0, "Europe":0.0, "Japan":0.0}
  data = pd.DataFrame([json.loads(data)])

  # Apply norm function
  data = norm(data)

  # Return the prediction
  prediction = predict(data)
  
  return prediction

def predict(data):
  score = model.predict(data)[0][0]
  return {"MPG_PREDICAO": float(score)}