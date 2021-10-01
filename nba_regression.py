import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import itertools

import torch

import os

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

# returns hashtable of stats by year
def extractDataMinYear(rel_path, min_year, column_names=None):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    abs_file_path = os.path.join(script_dir, rel_path)

    mega_dataset = extractData(rel_path)
    trimmed_dataset = mega_dataset[mega_dataset['Year'] >= min_year]

    return trimmed_dataset

if __name__ == '__main__':

    dataset_20 = extractData("2020/nba_2020_per_game.csv")
    dataset_21 = extractData("2021/nba_2021_per_game.csv")

    # get years 2016 up till 2019
    dataset_multiyear = extractDataMinYear("uptill2019/Seasons_stats_complete.csv", 2016)


    datasets = {2021: dataset_21, 2020: dataset_20}

    for year in range(2012, 2020):
        datasets[year] = dataset_multiyear[dataset_multiyear['Year'] == year]

    # need to make sure all datasets have the same columns
    # dataset_20 and dataset_21 have the same columns, can use either as ref
    columns = list(dataset_20.columns)

    # trim games started, not tracking that
    columns.remove('GS')

    for year, dataset in datasets.items():
        datasets[year] = dataset.loc[:, columns]

    # trim GS from these two datasets
    dataset_21 = dataset_21.loc[:, columns]
    dataset_20 = dataset_20.loc[:, columns]

    datasets[2020] = dataset_20
    datasets[2021] = dataset_21

    # going to predict nba sophomore stats

    # strat, going to compile all data
    # need list of rookies, can get from basketball reference
    # going to use pick number and stats

    rookies = {}

    for year in range(2011, 2021):
        rookies[year] = extractData("rookies/" + str(year) + ".csv")



