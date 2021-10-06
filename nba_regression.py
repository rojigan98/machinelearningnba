import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import itertools

import torch

import os
import csv

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
    return mega_dataset[mega_dataset['Year'] >= min_year]

if __name__ == '__main__':

    df_20 = extractData("2020/nba_2020_per_game.csv")
    df_21 = extractData("2021/nba_2021_per_game.csv")

    df_20.loc[:, "Year"] = np.array([2020] * len(df_20))
    df_21.loc[:, "Year"] = np.array([2021] * len(df_21))

    # get years 2016 up till 2019
    df_m = extractDataMinYear("uptill2019/Seasons_stats_complete.csv", 2012)

    # want all columns to match
    columns = list(df_20.columns)

    # trim games started, not tracking that
    columns.remove('GS')

    df_m = df_m.loc[:, columns]

    totals_columns = ["MP", "FG", "FGA", "3P", "3PA", "2P", "2PA", "FT", \
    "FTA", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]

    df_m.loc[:,totals_columns] = df_m.loc[:,totals_columns].divide(df_m['G'], axis=0).round(1)

    # trim GS from these two datasets
    df_21 = df_21.loc[:, columns]
    df_20 = df_20.loc[:, columns]

    df_m = pd.concat([df_m, df_20, df_21])


    # need to group data, so each player has one line per year
    # check how many entries per player per year
    # if 1 good! or or if more take the "TOT" one

    rookie_list = []

    for year in range(2011, 2021):
        with open("rookies/" + str(year) + ".csv", newline ='', \
        encoding="utf8") as f:
            reader = csv.reader(f)
            rookie_list.extend(list(reader))

    rookie_columns = rookie_list[0]
    # now transform this into df then call it a day

    rookie_df = pd.DataFrame(data=rookie_list, columns=rookie_columns)
    rookie_df = rookie_df[rookie_df["Pk"] != "Pk"]

    rookie_years = np.array([[year] * 60 for year in range(2012, 2022)])
    rookie_years = rookie_years.flatten()

    rookie_df.loc[:, "Year"] = np.array(rookie_years)

    # need to do TOT scraping too
    # do by year first 60 2012, next 60 2013, etc.

    # temp_rookie_df = extractData("rookies/" + str(year) + ".csv")
    # temp_rookie_df.loc[:, "Year"] =  np.array([year + 1] * \
    # len(temp_rookie_df))
    # rookie_df = rookie_df.append(temp_rookie_df)

    # mapping for each nba player to their rookie and sophomore years
    # years have to be 2012 and later for both, minimum 40 games played for
    # each

    # rookie_pairs = {}
    #
    # for year in range(2020, 2021):
    #
    #     for rookie in rookies[year].loc[:, "Player"]:
    #
    #         valid_years = []
    #
    #         for pot_year in range(year, 2022):
    #             try:
    #                 rookie_stats = \
    #                 datasets[pot_year][datasets[pot_year]["Player"] == rookie]
    #
    #                 if rookie_stats.size > len(columns) + 1:
    #                     rookie_stats = rookie_stats[rookie_stats["Tm"] == "TOT"]
    #
    #                 elif rookie_stats.size == 0 or \
    #                 rookie_stats[rookie_stats['G'] >= 25].size == 0:
    #                     continue
    #
    #                 valid_years.append(pot_year)
    #
    #             except KeyError:
    #                 pass


