import pandas as pd
from numpy import NaN
import requests
from requests.adapters import HTTPAdapter
from pybaseball.split_stats import get_splits
from requests.packages.urllib3.util.retry import Retry
from typing import Dict, Optional, Tuple, Union
import bs4 as bs
import pandas as pd
import re

splits_rows = ['vs RHP', 'vs LHP']
platoon_split_name = 'Platoon Splits'


relevant_b_cols = ['IN_PLAY_PCT', 'HR_PCT', '2B_PCT']

#Get position players, remove anyone not currently on a team and switch hitters:
def get_active_players(df: pd.DataFrame):
    active_non_pitchers = df.loc[(df['POS'] != 'P') & (df['ACTIVE'] == 'Y') & (df['TEAM'].notnull()) & (df['BATS'] != 'B')]
    active_non_pitchers
    players_info = active_non_pitchers[["PLAYERNAME", "BREFID", "BATS", "IDFANGRAPHS"]]
    return players_info

#Get Pitchers, remove any not currently on a team
def get_active_starters(df: pd.DataFrame):
    pitcher_keys = ['P', 'SP']
    active_starters = df.loc[(df['ALLPOS'].isin(pitcher_keys)) & (df['ACTIVE'] == 'Y') & (df['TEAM'].notnull())]
    pitchers_info = active_starters[["PLAYERNAME", "BREFID", "THROWS", "IDFANGRAPHS"]]
    return pitchers_info

def getSplitRelevantColsBatter(bats, row):
  opp_pitch = 'vs RHP' if (bats == 'L') else 'vs LHP'
  split_oppo = row.loc[(platoon_split_name, [opp_pitch]), :]
  split_oppo['IN_PLAY_PCT'] = (split_oppo['PA'] - split_oppo['BB'] - split_oppo['HBP'] - split_oppo['SO'])/(split_oppo['PA'])
  split_oppo['HR_PCT'] = (split_oppo['HR'] / split_oppo['PA'])
  split_oppo['2B_PCT'] =  (split_oppo['2B'] / split_oppo['PA'])
  split_oppo_relevant = split_oppo[relevant_b_cols]
  return split_oppo_relevant

def getSplitRelevantColsPitcher(throws, row):
  opp_bat = 'vs RHB' if (throws == 'L') else 'vs LHB'
  split_oppo = row.loc[(platoon_split_name, [opp_bat]), :]
  split_oppo['IN_PLAY_PCT'] = (split_oppo['PA'] - split_oppo['BB'] - split_oppo['HBP'] - split_oppo['SO'])/(split_oppo['PA'])
  split_oppo['HR_PCT'] = (split_oppo['HR'] / split_oppo['PA'])
  split_oppo['2B_PCT'] =  (split_oppo['2B'] / split_oppo['PA'])
  split_oppo_relevant = split_oppo[relevant_b_cols]
  return split_oppo_relevant


#TODO: get team info
def get_batter_fundamentals_df(df: pd.DataFrame):
    batter_data = []
    for index, row in df.iterrows():
        b_ref_id = row['BREFID']
        bats = row['BATS']
        b_ref_splits = get_splits(playerid=b_ref_id, year=2021)
        cols = getSplitRelevantColsBatter(bats, b_ref_splits)
        batter_data.append([row['PLAYERNAME'], b_ref_id, bats, cols['IN_PLAY_PCT'].values[0], cols['HR_PCT'].values[0], cols['2B_PCT'].values[0]])
    batter_fundamentals_df = pd.DataFrame(batter_data, columns=['PLAYERNAME', 'BREFID', 'BATS', 'b_IN_PLAY_PCT', 'b_HR_PCT', 'b_2B_PCT'])
    return batter_fundamentals_df


#TODO: Get Team info
def get_pitcher_fundamentals_df(df: pd.DataFrame):
    pitcher_data = []
    for index, row in df.iterrows():
        b_ref_id = row['BREFID']
        throws = row['THROWS']
        b_ref_splits = get_splits(playerid=b_ref_id, year=2021, pitching_splits=True)
        cols = getSplitRelevantColsPitcher(throws, b_ref_splits[0])
        pitcher_data.append([row['PLAYERNAME'], b_ref_id, throws, cols['IN_PLAY_PCT'].values[0], cols['HR_PCT'].values[0], cols['2B_PCT'].values[0]])
    pitcher_fundamentals_df = pd.DataFrame(pitcher_data, columns=['PLAYERNAME', 'BREFID', 'THROWS', 'p_IN_PLAY_PCT', 'p_HR_PCT', 'p_2B_PCT'])
    return pitcher_fundamentals_df