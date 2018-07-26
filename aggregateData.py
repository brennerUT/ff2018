import pandas as pd
import os
import pickle
import datetime
import string
import requests
import certifi

#os.chdir()
from scrapeData import *

##inputs example
directory='C:/Users/ericb/Desktop/ff2018/'#projections directory
ppr=1.0
season='2017'

beersheetsProjections(season=,directory=,ppr=)

cbsProjections(season=,directory=,ppr=)
edsfootballProjections(season=,directory=,ppr=)
espnProjections(season=,directory=,ppr=)
fantasysharksProjections(season=,directory=,ppr=)
fftodayProjections(season=,directory=,ppr=)
nflProjections(season=,directory=)
numberfireProjections(season=,directory=,ppr=)
pickingprosProjections(season=,directory=,ppr=)
scoutProjections(season=,directory=)
walterfootballProjections(season=,directory=,ppr=)
yahooProjections(season=,directory=,ppr=)

actualStats(directory=,season=,ppr=)
