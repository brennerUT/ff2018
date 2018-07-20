import pandas as pd
import os
import pickle
import datetime
import string
#import other functions of mine

##inputs example
directory='C:/Users/ericb/Desktop/ff2018/'#stats directory
ppr=0.5
season='2017'

def actualStats(directory,season,ppr=0.0):
    source='actual'
    ##Scrape and pickle
    base_url='http://games.espn.com/ffl/leaders?'
    pos={'QB':'0','RB':'2','WR':'4','TE':'6','DST':'16','K':'17'}
    pages=["0","50","100",'150','200']
    urls=[base_url+'&slotCategoryId='+po+'&startIndex='+pa for po in pos.values() for pa in pages]
    
    if season != str(datetime.datetime.now().year) and os.path.exists(directory+source+season+'.p'):
        DFs=pickle.load(open(directory+source+season+'.p',"rb"))
    else:
        DFs=[pd.read_html(url)[0] for url in urls]
        pickle.dump(DFs,open(directory+source+season+'.p','wb'))
    
    ##Clean data
    varNames=["player","passCompAtt","passYds","passTds","passInt","rushAtt","rushYds","rushTds","rec","recYds","recTds","points"]
    dstNames=["player","points"]
    kNames=["player","points"]
    
    cleanedDFs=[]
    for i in range(0,len(DFs)):
        df=DFs[i]
        df=df.drop([0,1]).dropna(axis=1,how='all')
        if df.shape[0] > 0:
            position=[po for po in list(pos) for pa in range(0,len(pages))][i]
            ##Trim dimensions
            df=df.iloc[1:,:]
            ##Add variable names
            if position == 'DST':
                df=df.iloc[:,[0,-1]]
                df.columns=dstNames
            elif position == 'K':
                df=df.iloc[:,[0,-1]]
                df.columns=kNames
            else:
                df=df.iloc[:,list(range(0,11))+[-1]]
                df.columns=varNames
            df['pos']=position
            cleanedDFs.append(df)
    
    ##Merge
    stats=pd.concat(cleanedDFs,ignore_index=True) #note: reorders columns
    
    ##Replace NaN's with value of zero
    stats.fillna(0,inplace=True)
    stats['passCompAtt'].replace(0,'0/0',inplace=True)
    stats['passCompAtt'].replace('--/--','0/0',inplace=True)
    stats.replace('--',0,inplace=True)
    
    ##Separate pass completions from attempts
    stats['passComp']=stats['passCompAtt'].str.split('/').str[0]
    stats['passAtt']=stats['passCompAtt'].str.split('/').str[1]
    
    ##Convert variables from character strings to numeric
    cols = stats.columns.drop(['passCompAtt','player','pos'])
    stats[cols] = stats[cols].apply(pd.to_numeric)
    
    ##Player teams
    stats['team']=stats['player'].str.split(',.').str[1].str[:3].str.strip().str.upper()
    stats['player']=stats['player'].str.replace(r'D/ST.*','').str.strip()
    teamsDf=pd.read_csv(directory+'nflTeams.csv')
    stats.loc[stats['team'].isnull(),'team']=stats.merge(teamsDf,left_on='player',right_on='name')['abb'].values
    
    ##Player names
    stats['player']=stats['player'].str.split(',').str[0]
    stats['player']=stats['player'].str.translate(str.maketrans(dict.fromkeys(string.punctuation,'')))
    stats['player']=stats['player'].str.replace(r'\s(Sr|Jr|II|III|IV|V)$','')
    stats.at[(stats['team']=='LAR')&(stats['player']=='Michael Thomas'),'player']='Michael D Thomas'
    
    
    ##Check for duplicates
    if stats[['player','pos']].duplicated().any():
        raise Exception('Multiple players with same name and position')
        #stats.loc[stats[['player','pos']].duplicated(),['player','pos']]
    
    ##Reorder columns
    stats=stats[['player','pos','points']+[c for c in stats if c not in ['player','pos','points']]]
    
    ##Adjust for ppr
    stats['points']=stats['points']-stats['rec']*(1.0-ppr) 
    return stats
