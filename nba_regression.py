import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sqlite3
import os

# Make numpy printouts easier to read.
np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

print(tf.__version__)

pd.set_option("display.max.columns", None)
pd.set_option("display.precision", 5)


def extractData(rel_path, column_names=None):
    # from https://stackoverflow.com/questions/7165749/open-file-in-a-
    # relative-location-in-python
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    abs_file_path = os.path.join(script_dir, rel_path)
    raw_dataset = pd.read_csv(abs_file_path)
    dataset = raw_dataset.copy()
    dataset = dataset.fillna(0)
    return dataset

def extractDataMinYear(rel_path, column_names=None):
    pass

dataset_20 = extractData("2020/nba_2020_per_game.csv")

print(dataset_20.tail().loc[:,["Player", "FG%", "PTS"]])

# let's get data for 2021 then years 2016 up till 2019


dataset_21 = extractData("2021/nba_2021_per_game.csv")
print(dataset_21.tail().loc[:,["Player", "FG%", "PTS"]])



datasets = {}
# now need to get years 2016 up till 2019



