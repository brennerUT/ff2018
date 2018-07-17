import pandas as pd
import requests
import os
import pickle
import datetime
#import other functions of mine

## inputs
directory='C:/Users/ericb/Desktop/ff2018/'#projections directory
ppr=1.0
season='2017'

#def espnProjections(directory=os.getcwd(),ppr=0.0,season):

suffix='espn'

##Scrape and pickle
base_url="http://games.espn.com/ffl/tools/projections?seasonId="+season
pos={'QB':'0','RB':'2','WR':'4','TE':'6','DST':'16','K':'17'}
pages=["0","40","80"]
urls=[base_url+'&slotCategoryId='+po+'&startIndex='+pa for po in pos.values() for pa in pages]

if season != str(datetime.datetime.now().year) and os.path.exists(directory+suffix+season+'.p'):
    DFs=pickle.load(open(directory+suffix+season+'.p',"rb"))
else:
    DFs=[pd.read_html(url)[0] for url in urls]
    pickle.dump(DFs,open(directory+suffix+season+'.p','wb'))


##Clean data
qbNames=rbNames=wrNames=teNames=kNames=dstNames=["rank","player","passCompAtt","passYds","passTds","passInt","rushAtt","rushYds","rushTds","rec","recYds","recTds","points"]
dstNames=["rank","player","points"]
kNames=["rank","player","points"]

cleanedDFs=[]
for i in range(0,len(DFs)):
    df=DFs[i]
    df=df.drop([0,1]).dropna(axis=1,how='all')
    if df.shape[0] > 0:
        position=[po for po in list(pos) for pa in range(0,len(pages))][i]
        ##Trim dimensions
        df=df.iloc[1:,:]
        ##Add variable names
        if position == 'QB':
            df.columns=qbNames
        elif position == 'RB':
            df.columns=rbNames
        elif position == 'WR':
            df.columns=wrNames
        elif position == 'TE':
            df.columns=teNames
        elif position == 'DST':
            df=df.iloc[:,[0,1,-1]]
            df.columns=dstNames
        elif position == 'K':
            df=df.iloc[:,[0,1,-1]]
            df.columns=kNames
        df['pos']=position
        cleanedDFs.append(df)

##Merge
projections=pd.concat(cleanedDFs,ignore_index=True) #note: reorders columns

##Replace NaN's with value of zero
projections.fillna(0,inplace=True)
projections['passCompAtt'].replace(0,'0/0')

##Separate pass completions from attempts
projections['passComp']=projections['passCompAtt'].str.split('/').str[0]
projections['passAtt']=projections['passCompAtt'].str.split('/').str[1]

##Convert variables from character strings to numeric
cols = projections.columns.drop(['passCompAtt','player','pos'])
projections[cols] = projections[cols].apply(pd.to_numeric)

##Player teams
projections['team']=projections['player'].str.split(',.').str[1].str[:3].str.strip().str.upper()
projections['player']=projections['player'].str.replace(r'D/ST.*','').str.strip()
teamsDf=pd.read_csv(directory+'nflTeams.csv')
projections.loc[projections['team'].isnull(),'team']=projections.merge(teamsDf,left_on='player',right_on='name')['abb'].values



