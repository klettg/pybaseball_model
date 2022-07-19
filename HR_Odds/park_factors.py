import pandas as pd
from pandas import DataFrame

park_factors = pd.read_csv('Park_Factors/2021_Park_Factors.csv')
print('this line executed') #TODO: remove

def getParkFactor(handedness: str, location_short_code: str): 
    if handedness == 'L':

        factor = park_factors.loc[park_factors['SHORT_CODE'] == location_short_code]
        return factor['HR as L'].values[0]
    if handedness == 'R':
        factor = park_factors.loc[park_factors['SHORT_CODE'] == location_short_code]
        return factor['HR as R'].values[0] 

def fill_park_factor_column(home: str, opp_short_code: str, home_short_code: str, handedness: str):
    if (home == 'Y'):
        return getParkFactor(park_factors, handedness, home_short_code)
    else: 
        return getParkFactor(park_factors, handedness, opp_short_code)