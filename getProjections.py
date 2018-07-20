import pandas as pd
import os
import pickle
import datetime
import string
import requests
#import other functions of mine

##inputs example
directory='C:/Users/ericb/Desktop/ff2018/'#projections directory
ppr=0.5
season='2018'

def yahooProjections(directory,season,ppr=0.0):
    source='yahoo'
    #Note: all input data here is initially set with 0 ppr
    ##Scrape and pickle
    if season == '2017':
        projections=pd.read_csv(directory+'yahoo2017.csv')
    elif int(season) > 2017:
        if season != str(datetime.datetime.now().year) and os.path.exists(directory+source+season+'.p'):
            DFs=pickle.load(open(directory+source+season+'.p',"rb"))
        else:
            baseUrl='https://football.fantasysports.yahoo.com/f1/217906/players?&sort=PTS&sdir=1&status=A&stat1=S_PS_2018&jsenabled=1'
            pages=['&count='+str(n) for n in range(0,175,25)]
            pos={'QB':'QB','RB':'RB','WR':'WR','TE':'TE','DST':'DEF','K':'K'}
            urls=[baseUrl+pa+'&pos='+po for po in pos.values() for pa in pages]
            DFs=[pd.read_html(url)[1] for url in urls]
            pickle.dump(DFs,open(directory+source+season+'.p','wb'))
        ##Clean data
        qbTeNames=["star","player","add","owner",'GP','Bye',"points","ownedPct","proj","actual","passYds","passTds","passInt","passAtt","rushYds","rushTds","recTgt","rec","recYds","recTds","returnTds","twoPts","fumbles","missing1"]
        rbWrNames=["star","player","add",'Forecast',"owner",'GP','Bye',"points","ownedPct","proj","actual","passYds","passTds","passInt","passAtt","rushYds","rushTds","recTgt","rec","recYds","recTds","returnTds","twoPts","fumbles","missing1"]
        kNames=["star","player","add","owner",'GP','Bye',"points","ownedPct","proj","actual","fg019","fg2029","fg3039","fg4049","fg50","fg","missing2"]
        dstNames=["star","player","add","owner",'GP','Bye',"points","ownedPct","proj","actual","dstPtsAllowed","dstSack","dstSafety","dstInt","dstFumlRec","dstDTd","dstBlk","dstRetTd","missing3"]
        cleanedDFs=[]
        for i in range(0,len(DFs)):
            df=DFs[i].copy()
            if df.shape[0] > 2:
                position=[po for po in list(pos) for pa in range(0,len(pages))][i]
                ##Add variable names
                if position == 'DST':
                    df.columns=dstNames
                elif position == 'K':
                    df.columns=kNames
                elif position in ['QB','TE']:
                    df.columns=qbTeNames
                else:
                    df.columns=rbWrNames
                df['pos']=position
                cleanedDFs.append(df)     
        ##Merge
        projections=pd.concat(cleanedDFs,ignore_index=True) #note: reorders columns
        projections['dstTd']=projections["dstDTd"]+projections["dstRetTd"]
        
    ##Remove punctuation
    projections=projections.replace({'%':'',',':''})
    
    ##Convert variables from character strings to numeric
    projections=projections.drop(['owner','ownedPct','Forecast','add','star'],axis=1,errors='ignore')
    cols=projections.columns.drop(['player','pos'])
    projections[cols] = projections[cols].apply(pd.to_numeric)
    
    #Player name and team
    if int(season) > 2017:
        projections['player']=projections['player'].str.split(r'Note.\s').str[1].str.rsplit('-',n=1).str[0]
        projections['team']=projections['player'].str.split().str[-1].str.upper().str.strip()
        projections['player']=projections['player'].str.rsplit(n=1).str[0].str.strip()
        teamsDf=pd.read_csv(directory+'nflTeams.csv')
        projections.loc[projections['pos']=='DST','player']=projections.loc[projections['pos']=='DST','team'].map(teamsDf.set_index('abb')['name'])
    projections['player']=projections['player'].str.translate(str.maketrans(dict.fromkeys(string.punctuation,'')))
    projections['player']=projections['player'].str.replace(r'\s(Sr|Jr|II|III|IV|V)$','')
    
    ##Check for duplicates
    if projections[['player','pos']].duplicated().any():
        raise Exception('Multiple players with same name and position')
    
    ##Reorder columns
    projections=projections[['player','pos','points']+[c for c in projections if c not in ['player','pos','points']]]
    
    ##Adjust for ppr
    projections['rec'].fillna(0.0,inplace=True)
    projections['points']=projections['points']+projections['rec']*ppr
    return projections

def beersheetsProjections(directory,season,ppr=0.0):
    source='beersheets'
    if ppr in [0.0,1.0]:
        ppr=str(int(ppr))
    else:
        ppr=str(ppr)
    ##Scrape and pickle
    if int(season) < 2018:
        fn='beersheets'+season+'/'+ppr+' PPR/1 QB/'+season+'-09-05 14 TM '+ppr+' PPR 1QB 2RB 2WR 1TE 1FLX 4 PaTD Snake.xlsx'
        df=pd.read_excel(directory+fn,index_col=1,header=4)
    else:
        url='https://footballabsurdity.com/wp-content/plugins/BeerSheetRequests/CURRENT/14,'+ppr+',1,2,2,1,1,0,0,0,4,6,6,0.04,0.1,0.1,-2,0,0,200.xlsx'
        if season != str(datetime.datetime.now().year) and os.path.exists(directory+source+season+'_'+ppr+'ppr.p'):
            df=pickle.load(open(directory+source+season+'_'+ppr+'ppr.p',"rb"))
        else:
            df=pd.read_excel(url,index_col=1,header=4)
            pickle.dump(df,open(directory+source+season+'_'+ppr+'ppr.p','wb'))
    
    ##Clean and add variable names
    dstDf=df[['TM/BW']].iloc[-15:].rename(columns={'TM/BW':'player'})
    dstDf['pos']='DST'
    dstDf['points']=range(15,0,-1)
    dstDf['player']=dstDf['player'].str.rsplit(None,1).str[1]
    kDf=df[['NAME']].iloc[-15:].rename(columns={'NAME':'player'})
    kDf['pos']='K'
    kDf['points']=range(15,0,-1)
    df=df.filter(regex=('(NAME.*)|(VAL.*)')).reset_index().drop('index',axis=1).iloc[0:78]
    df.loc[df.index[0:32],'pos']='QB'
    df.loc[df.index[32:],'pos']='TE'
    qb_te_df=df[['NAME','VAL','pos']].rename(columns={'NAME':'player','VAL':'points'}).drop([32,33,34]).reset_index(drop=True)[:57]
    rb_df=df[['NAME (POS)','VAL.1']].rename(columns={'NAME (POS)':'player','VAL.1':'points'})
    wr_df=df[['NAME (POS).1','VAL.2']].rename(columns={'NAME (POS).1':'player','VAL.2':'points'})
    
    ##Merge
    df=pd.concat([qb_te_df,rb_df],ignore_index=True)
    df.fillna('RB',inplace=True)
    df=pd.concat([df,wr_df,dstDf,kDf],ignore_index=True)
    df.fillna('WR',inplace=True)
    df['player']=df['player'].str.replace(r'\s\(.*$','')
    projections=df
    
    ##Convert variables from character strings to numeric
    cols=projections.columns.drop(['player','pos'])
    projections[cols] = projections[cols].apply(pd.to_numeric)
    
    ##Player names
    projections['player']=projections['player'].str.translate(str.maketrans(dict.fromkeys(string.punctuation,'')))
    projections['player']=projections['player'].str.replace(r'\s(Sr|Jr|II|III|IV|V)$','')
    
    ##Check for duplicates
    if projections[['player','pos']].duplicated().any():
        raise Exception('Multiple players with same name and position')
    
    ##Reorder columns
    projections=projections[['player','pos','points']+[c for c in projections if c not in ['player','pos','points']]]
    
    return projections

def espnProjections(directory,season,ppr=0.0):
    source='espn'
    ##Scrape and pickle
    base_url="http://games.espn.com/ffl/tools/projections?seasonId="+season
    pos={'QB':'0','RB':'2','WR':'4','TE':'6','DST':'16','K':'17'}
    pages=["0","40","80"]
    urls=[base_url+'&slotCategoryId='+po+'&startIndex='+pa for po in pos.values() for pa in pages]
    
    if season != str(datetime.datetime.now().year) and os.path.exists(directory+source+season+'.p'):
        DFs=pickle.load(open(directory+source+season+'.p',"rb"))
    else:
        DFs=[pd.read_html(url)[0] for url in urls]
        pickle.dump(DFs,open(directory+source+season+'.p','wb'))

    ##Clean data
    qbNames=rbNames=wrNames=teNames=["rank","player","passCompAtt","passYds","passTds","passInt","rushAtt","rushYds","rushTds","rec","recYds","recTds","points"]
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
    projections['passCompAtt'].replace(0,'0/0',inplace=True)
    
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
    
    ##Player names
    projections['player']=projections['player'].str.split(',').str[0]
    projections['player']=projections['player'].str.translate(str.maketrans(dict.fromkeys(string.punctuation,'')))
    projections['player']=projections['player'].str.replace(r'\s(Sr|Jr|II|III|IV|V)$','')
    
    ##Check for duplicates
    if projections[['player','pos']].duplicated().any():
        raise Exception('Multiple players with same name and position')
    
    ##Reorder columns
    projections=projections[['player','pos','points']+[c for c in projections if c not in ['player','pos','points']]]
    
    ##Adjust for ppr, espn default is 1 ppr
    projections['points']=projections['points']-projections['rec']*(1.0-ppr)
    return projections

#def pickingprosProjections(directory,season,ppr=0.0):
source='pickingpros'
##Scrape and pickle
if season != str(datetime.datetime.now().year) and os.path.exists(directory+source+season+'.p'):
    df=pickle.load(open(directory+source+season+'.p',"rb"))
else:    
    if season == '2017':
        df=pd.read_html('https://web.archive.org/web/20170829211042/http://pickingpros.com/nfl/overall-fantasy-projections.php')[2]
    elif season == str(datetime.datetime.now().year):
        df=pd.read_html(requests.get('http://pickingpros.com/nfl/overall-fantasy-projections.php').text)[0]
    pickle.dump(df,open(directory+source+season+'.p','wb'))

##Clean and add variable names
df.columns=df.columns.str.strip()
df['Name']=df['Name'].str.strip()
df=df[['Name','Rec','Fantasy']]
df=df.rename(columns={'Name':'player','Rec':'rec','Fantasy':'points'})
projections=df

##Convert variables from character strings to numeric
cols=projections.columns.drop('player')
projections[cols] = projections[cols].apply(pd.to_numeric)

##Player names
projections['player']=projections['player'].str.translate(str.maketrans(dict.fromkeys(string.punctuation,'')))
projections['player']=projections['player'].str.replace(r'\s(Sr|Jr|II|III|IV|V)$','')
projections['player']=projections['player'].str.replace('Robert Kelley','Rob Kelley')

##Check for multiple players with same name
projections.drop_duplicates(inplace=True)
if projections[['player']].duplicated().any():
    raise Exception('Multiple players with same name')
    #projections.loc[projections['player'].duplicated(),'player']

##Add positions
refDf=espnProjections(directory=directory,season=season)
refDf=refDf[refDf['pos'].isin(['QB','RB','WR','TE'])]
refDf=refDf.sort_values('points',ascending=False)[['player','pos']].drop_duplicates('player')
projections=projections.merge(refDf,on='player',how='left').dropna()

##Reorder columns
projections=projections[['player','pos','points']+[c for c in projections if c not in ['player','pos','points']]]

##Adjust for ppr, pickingpros default is 0 ppr
projections['points']=projections['points']+projections['rec']*ppr
    return projections
