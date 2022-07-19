from HR_Odds.park_factors import getParkFactor
from HR_Odds.player_info import get_active_players, get_active_starters, get_batter_fundamentals_df, get_pitcher_fundamentals_df
from pybaseball.datasources.fangraphs import fg_batting_data
from pybaseball.enums.fangraphs.batting_data_enum import FangraphsBattingStats
from pybaseball import statcast
from pybaseball.datasources.fangraphs import FangraphsBattingStatsTable
from pybaseball.split_stats import get_game_logs_batter
import pandas as pd

if __name__=='__main__':
    #data = fg_batting_data(2019, max_results=50)
    #player_info = get_player_info_modified('francty01')
    #res, info = get_splits(playerid='francty01', year=2021, player_info=True)
    #res.head()
    #print(res)
    #pitch_or_bat='b'
    #year=2022
    #park_factors = pd.read_csv('Park_Factors/2021_Park_Factors.csv')
    #TODO: add data from 2021, etc. 
    playerid = 'francty01'
    test_players = ['Ty France', 'Tim Anderson']
    test_pitchers = ['Marco Gonzales', 'Clayton Kershaw']




    player_info = pd.read_csv('Player_Map/SFBB-Player-ID-Map.csv')
    active_players = get_active_players(player_info)
    active_pitchers = get_active_starters(player_info)
    players_info_test = active_players[active_players['PLAYERNAME'].isin(test_players)]
    pitchers_info_test = active_pitchers[active_pitchers['PLAYERNAME'].isin(test_pitchers)]

    batter_fundamentals = get_batter_fundamentals_df(players_info_test)
    pitcher_fundamentals = get_pitcher_fundamentals_df(pitchers_info_test)


    #TODO: somehow combine fundamentals with game log
    #getParkFactor(park_factors, 'L', 'MIN')
    game_logs = get_game_logs_batter(playerid, 2022)
    game_logs['Park_Factor'] = game_logs.apply(lambda x: getParkFactor(''))

    playerInfo = 1



    #TODO:
    #1. expand get_game_logs to accept multiple, append batter fundamentals
    #2. apply function to fill park factor for each entry in game log
    #3. apply funciton to pull pitcher fundamental for each entry in game log
    #4. log regression model
    #5. Pull odds from BettingPros and insert into game logs
    #6. compare

    #Misc: multiple year splits, confirm that park factors doesn't execute each time, add restrictions on min innings pitched/PAs, convert date