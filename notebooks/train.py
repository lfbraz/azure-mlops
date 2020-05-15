# Databricks notebook source
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None  # default='warn'

class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

def download_dataset():
  dataset_path = keras.utils.get_file("auto-mpg.data", "http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data")

  column_names = ['MPG','Cylinders','Displacement','Horsepower','Weight',
                  'Acceleration', 'Model Year', 'Origin']

  raw_dataset = pd.read_csv(dataset_path, names=column_names,
                            na_values = "?", comment='\t',
                            sep=" ", skipinitialspace=True)
  
  dataset = raw_dataset.copy()  
  
  return dataset

def transform_data(dataset):
  dataset = dataset.dropna()
  
  origin = dataset.pop('Origin')
  
  dataset['USA'] = (origin == 1)*1.0
  dataset['Europe'] = (origin == 2)*1.0
  dataset['Japan'] = (origin == 3)*1.0
  
  return dataset

def split_dataset(dataset):
  train_dataset = dataset.sample(frac=0.8,random_state=0)
  test_dataset = dataset.drop(train_dataset.index)
  
  return train_dataset, test_dataset

def train_stats(dataset):
  train_stats = dataset.describe()
  #dataset.pop("MPG")
  train_stats = train_stats.transpose() 
  
  return train_stats

def get_labels(train_dataset, test_dataset):
  train_labels = train_dataset.pop('MPG')
  test_labels = test_dataset.pop('MPG')
  
  return train_labels, test_labels

def norm(dataset, train_stats):
  return (dataset - train_stats['mean']) / train_stats['std']

def build_model(keys):
  model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=[len(keys)]),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)
  ])

  optimizer = tf.keras.optimizers.RMSprop(0.001)

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
  return model


def train(epochs, validation_split, patience=10, verbose=0):
  dataset = download_dataset()
  dataset = transform_data(dataset)
  train_dataset, test_dataset = split_dataset(dataset)
  stats = train_stats(train_dataset)
  train_labels, test_labels = get_labels(train_dataset, test_dataset)
  train_dataset = norm(train_dataset, stats)
  test_dataset = norm(test_dataset, stats)
  
  model = build_model(train_dataset.keys())

  # O paramêtro patience é o quantidade de epochs para checar as melhoras
  early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=patience)

  history = model.fit(train_dataset, train_labels, epochs=epochs,
                      validation_split = validation_split, verbose=verbose, callbacks=[early_stop, PrintDot()])
  
  return history, model

# COMMAND ----------

EPOCHS = 1000
VALIDATION_SPLIT = 0.2
PATIENCE = 100

history, model = train(EPOCHS, VALIDATION_SPLIT, PATIENCE)