import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import itertools

import os

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

print(tf.__version__)

# Make numpy printouts easier to read.
np.set_printoptions(precision=3, suppress=True)

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

# want this to return hashtable of by year
def extractDataMinYear(rel_path, min_year, column_names=None):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    abs_file_path = os.path.join(script_dir, rel_path)

    mega_dataset = extractData(rel_path)
    trimmed_dataset = mega_dataset[mega_dataset['Year'] >= min_year]

    return trimmed_dataset

if __name__ == '__main__':

    dataset_20 = extractData("2020/nba_2020_per_game.csv")

    # print(dataset_20.tail().loc[:,["Player", "FG%", "PTS"]])

    # let's get data for year 2021 now

    dataset_21 = extractData("2021/nba_2021_per_game.csv")
    # print(dataset_21.tail().loc[:,["Player", "FG%", "PTS"]])

    # now need to get years 2016 up till 2019
    dataset_multiyear = extractDataMinYear("uptill2019/Seasons_stats_complete.csv", 2016)

    # print(dataset_multiyear.head().loc[:,["Year", "Player", "FG%", "PTS"]])
    # print(dataset_multiyear.tail().loc[:,["Year", "Player", "FG%", "PTS"]])

    # want 2016 and later data
    # so 2016 -> next year played w/ 20+ games (e.g. Ben Simmons)
    # 2017 -> ..
    # 2018 -> ..
    # 2019 -> ..
    # 2020 -> ..

    # 5 sets of data should be good and most 2020ers except killian hayes played in 2021

    datasets = {2021: dataset_21, 2020: dataset_20}

    for year in range(2016, 2020):
        datasets[year] = dataset_multiyear[dataset_multiyear['Year'] == year]

    for year, dataset in datasets.items():
        print("should be year:", year)
        if year <= 2019:
            print(dataset.head().loc[:,["Year", "Player", "FG%", "PTS"]])
        else:
            print(dataset.head().loc[:,["Player", "FG%", "PTS"]])




