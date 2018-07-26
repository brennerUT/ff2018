import pandas as pd
import os
import pickle
import datetime
import string
import requests
import certifi

###inputs example
#directory='C:/Users/ericb/Desktop/ff2018/'#projections directory
#ppr=1.0
#season='2017'

##def fantasydataProjections(directory,season,ppr=0.0):
#source='fantasydata'
###Scrape and pickle
#if season == str(datetime.datetime.now().year) or os.path.exists(directory+source+season+'.p') == False:
#    baseUrl='https://fantasydata.com/nfl-stats/fantasy-football-weekly-projections?season='+season
#    test=pd.read_html(baseUrl+'&team=1')[1]
#    DFs=[]
#    pickle.dump(DFs,open(directory+source+season+'.p','wb'))
#DFs=pickle.load(open(directory+source+season+'.p',"rb"))
#
#    return projections

def nflProjections(directory,season):
    source='nfl'
    ##Scrape and pickle
    if season == '2017':
        projections=pd.read_csv(directory+source+season+'.csv')
    elif int(season) > 2017:
        if season != str(datetime.datetime.now().year) and os.path.exists(directory+source+season+'.p'):
            DFs=pickle.load(open(directory+source+season+'.p',"rb"))
        else:
            baseUrl='http://fantasy.nfl.com/research/projections?offset='
            qb1=pd.read_html(baseUrl+'1&position=1&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=seasonProjectedStats&statWeek=1#researchProjections=researchProjections%2C%2Fresearch%2Fprojections%253Fposition%253D2%2526statCategory%253DprojectedStats%2526statSeason%253D2018%2526statType%253DseasonProjectedStats%2526statWeek%253D1%2Creplace')[0]
            qb2=pd.read_html(baseUrl+'26&position=1&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=seasonProjectedStats&statWeek=1#researchProjections=researchProjections%2C%2Fresearch%2Fprojections%253Fposition%253D2%2526statCategory%253DprojectedStats%2526statSeason%253D2018%2526statType%253DseasonProjectedStats%2526statWeek%253D1%2Creplace')[0]
            rb1=pd.read_html(baseUrl+'1&position=2&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=seasonProjectedStats&statWeek=1#researchProjections=researchProjections%2C%2Fresearch%2Fprojections%253Fposition%253D2%2526statCategory%253DprojectedStats%2526statSeason%253D2018%2526statType%253DseasonProjectedStats%2526statWeek%253D1%2Creplace')[0]
            rb2=pd.read_html(baseUrl+'26&position=2&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=seasonProjectedStats&statWeek=1#researchProjections=researchProjections%2C%2Fresearch%2Fprojections%253Fposition%253D2%2526statCategory%253DprojectedStats%2526statSeason%253D2018%2526statType%253DseasonProjectedStats%2526statWeek%253D1%2Creplace')[0]
            rb3=pd.read_html(baseUrl+'51&position=2&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=seasonProjectedStats&statWeek=1#researchProjections=researchProjections%2C%2Fresearch%2Fprojections%253Fposition%253D2%2526statCategory%253DprojectedStats%2526statSeason%253D2018%2526statType%253DseasonProjectedStats%2526statWeek%253D1%2Creplace')[0]
            rb4=pd.read_html(baseUrl+'76&position=2&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=seasonProjectedStats&statWeek=1#researchProjections=researchProjections%2C%2Fresearch%2Fprojections%253Fposition%253D2%2526statCategory%253DprojectedStats%2526statSeason%253D2018%2526statType%253DseasonProjectedStats%2526statWeek%253D1%2Creplace')[0]
            wr1=pd.read_html(baseUrl+'1&position=3&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=seasonProjectedStats&statWeek=1#researchProjections=researchProjections%2C%2Fresearch%2Fprojections%253Fposition%253D2%2526statCategory%253DprojectedStats%2526statSeason%253D2018%2526statType%253DseasonProjectedStats%2526statWeek%253D1%2Creplace')[0]
            wr2=pd.read_html(baseUrl+'26&position=3&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=seasonProjectedStats&statWeek=1#researchProjections=researchProjections%2C%2Fresearch%2Fprojections%253Fposition%253D2%2526statCategory%253DprojectedStats%2526statSeason%253D2018%2526statType%253DseasonProjectedStats%2526statWeek%253D1%2Creplace')[0]
            wr3=pd.read_html(baseUrl+'51&position=3&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=seasonProjectedStats&statWeek=1#researchProjections=researchProjections%2C%2Fresearch%2Fprojections%253Fposition%253D2%2526statCategory%253DprojectedStats%2526statSeason%253D2018%2526statType%253DseasonProjectedStats%2526statWeek%253D1%2Creplace')[0]
            wr4=pd.read_html(baseUrl+'76&position=3&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=seasonProjectedStats&statWeek=1#researchProjections=researchProjections%2C%2Fresearch%2Fprojections%253Fposition%253D2%2526statCategory%253DprojectedStats%2526statSeason%253D2018%2526statType%253DseasonProjectedStats%2526statWeek%253D1%2Creplace')[0]
            te1=pd.read_html(baseUrl+'1&position=4&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=seasonProjectedStats&statWeek=1#researchProjections=researchProjections%2C%2Fresearch%2Fprojections%253Fposition%253D2%2526statCategory%253DprojectedStats%2526statSeason%253D2018%2526statType%253DseasonProjectedStats%2526statWeek%253D1%2Creplace')[0]
            te2=pd.read_html(baseUrl+'26&position=4&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=seasonProjectedStats&statWeek=1#researchProjections=researchProjections%2C%2Fresearch%2Fprojections%253Fposition%253D2%2526statCategory%253DprojectedStats%2526statSeason%253D2018%2526statType%253DseasonProjectedStats%2526statWeek%253D1%2Creplace')[0]
            dst=pd.read_html(baseUrl+'1&position=8&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=seasonProjectedStats&statWeek=1#researchProjections=researchProjections%2C%2Fresearch%2Fprojections%253Fposition%253D2%2526statCategory%253DprojectedStats%2526statSeason%253D2018%2526statType%253DseasonProjectedStats%2526statWeek%253D1%2Creplace')[0]
            kickers=pd.read_html(baseUrl+'1&position=7&sort=projectedPts&statCategory=projectedStats&statSeason=2018&statType=seasonProjectedStats&statWeek=1#researchProjections=researchProjections%2C%2Fresearch%2Fprojections%253Fposition%253D2%2526statCategory%253DprojectedStats%2526statSeason%253D2018%2526statType%253DseasonProjectedStats%2526statWeek%253D1%2Creplace')[0]
            DFs=[qb1,qb2,rb1,rb2,rb3,rb4,wr1,wr2,wr3,wr4,te1,te2,dst,kickers]
            pickle.dump(DFs,open(directory+source+season+'.p','wb'))
        varNames=["player","opp","gp","passYds","passTds","passInt","rushYds","rushTds","recYds","recTds","fumbleTds","twoPts","fumbles","points"]
        dstkNames=['player','points']
        cleanedDFs=[]
        for i in range(0,len(DFs)):
            df=DFs[i].copy()
            position=[po for po in ['QB','QB','RB','RB','RB','RB','WR','WR','WR','WR','TE','TE','DST','K']][i]
            ##Add variable names
            if position in ['DST','K']:
                df=df.iloc[:,[0,-1]]
                df.columns=dstkNames
            else:
                df.columns=varNames
            df['pos']=position
            cleanedDFs.append(df)
        ##Merge and clean
        projections=pd.concat(cleanedDFs,ignore_index=True)
        projections.loc[projections['pos']=='DST','player']=projections.loc[projections['pos']=='DST','player'].str.extract(r'(.*)\sDEF.*',expand=False).str.strip().str.rsplit(None).str[-1]
        projections.loc[projections['pos']!='DST','player']=projections.loc[projections['pos']!='DST','player'].str.extract(r'(.*)\s\S*\s-.*',expand=False)
    
    ##Convert to numeric
    projections['points']=pd.to_numeric(projections['points'])
    
    ##Player names
    projections['player']=projections['player'].str.translate(str.maketrans(dict.fromkeys(string.punctuation,'')))
    projections['player']=projections['player'].str.replace(r'\s(Sr|Jr|II|III|IV|V)$','')
    
    ##Check for duplicates
    if projections[['player','pos']].duplicated().any():
        raise Exception('Multiple players with same name and position')
        #projections.loc[projections[['player','pos']].duplicated(),['player','pos']]
        
    ##Reorder columns
    projections=projections[['player','pos','points']+[c for c in projections if c not in ['player','pos','points']]]
    return projections

def edsfootballProjections(directory,season,ppr=0.0):
    source='edsfootball'
    ##Scrape and pickle
    if season == str(datetime.datetime.now().year) or os.path.exists(directory+source+season+'.p') == False:
        qb=pd.read_html('http://www.eatdrinkandsleepfootball.com/fantasy/projections/'+season+'/qb/',header=0)[1]
        rb=pd.read_html('http://www.eatdrinkandsleepfootball.com/fantasy/projections/'+season+'/rb/',header=0)[1]
        wr=pd.read_html('http://www.eatdrinkandsleepfootball.com/fantasy/projections/'+season+'/wr/',header=0)[1]
        te=pd.read_html('http://www.eatdrinkandsleepfootball.com/fantasy/projections/'+season+'/te/',header=0)[1]
        DFs=[qb,rb,wr,te]
        pickle.dump(DFs,open(directory+source+season+'.p','wb'))
    DFs=pickle.load(open(directory+source+season+'.p',"rb"))
    
    #Add variable names
    qb.columns=["positionRank","player","team",'bye',"passComp","passAtt","passYds","passTds","passInt","rushAtt","rushYds","rushTds","points"]
    rb.columns=["positionRank","player","team",'bye',"rushAtt","rushYds","rushTds","rec","recYds","recTds","points"]
    wr.columns=["positionRank","player","team",'bye',"rec","recYds","recTds","rushAtt","rushYds","rushTds","points"]
    te.columns=["positionRank","player","team",'bye',"rec","recYds","recTds","points"]
    
    ##Add position names
    qb['pos']='QB'
    rb['pos']='RB'
    wr['pos']='WR'
    te['pos']='TE'
    
    ##Merge
    projections=pd.concat([qb,rb,wr,te],ignore_index=True)
    
    ##Convert variables from character strings to numeric
    cols = projections.columns.drop(['player','pos','team'])
    projections[cols] = projections[cols].apply(pd.to_numeric)
    
    ##Player name and team
    projections['player']=projections['player'].str.translate(str.maketrans(dict.fromkeys(string.punctuation,'')))
    projections['player']=projections['player'].str.replace(r'\s(Sr|Jr|II|III|IV|V)$','')
    projections['team']=projections['team'].str.rsplit().str[-1]
    teamsDf=pd.read_csv(directory+'nflTeams.csv').drop('city',axis=1)
    projections=projections.merge(teamsDf,left_on='team',right_on='name')
    projections=projections.drop(['team','name'],axis=1).rename(columns={'abb':'team'})
    
    ##Check for duplicates
    if projections[['player','pos']].duplicated().any():
        raise Exception('Multiple players with same name and position')
    
    ##Reorder columns
    projections=projections[['player','pos','points']+[c for c in projections if c not in ['player','pos','points']]]
    
    ##Adjust for ppr
    projections['rec']=projections['rec'].fillna(0.0)
    projections['points']=projections['points']+projections['rec']*ppr
    return projections

def walterfootballProjections(directory,season,ppr=0.0):
    source='walterfootball'
    ##Scrape and pickle
    if season == str(datetime.datetime.now().year) or os.path.exists(directory+source+season+'.xlsx') == False:
        resp = requests.get('http://walterfootball.com/fantasy'+season+'rankingsexcel.xlsx')
        with open(directory+source+season+'.xlsx', 'wb') as output:
            output.write(resp.content)
    qb=pd.read_excel(directory+source+season+'.xlsx',sheet_name='QBs')
    rb=pd.read_excel(directory+source+season+'.xlsx',sheet_name='RBs')
    wr=pd.read_excel(directory+source+season+'.xlsx',sheet_name='WRs')
    te=pd.read_excel(directory+source+season+'.xlsx',sheet_name='TEs')
    dst=pd.read_excel(directory+source+season+'.xlsx',sheet_name='DEFs')
    kickers=pd.read_excel(directory+source+season+'.xlsx',sheet_name='Ks')
    
    ##Variable names
    qb.columns=rb.columns=wr.columns=te.columns=['lastName','firstName','team','bye','pos','passYds','passTds','passInt','rushYds','rec','recYds','rushRecTds','bonus','dynasty','points','vbdReg','pprPts','pprVBD','tdPts','vbdTd','pts2QB','vbd2QB','ptsCustom','vbdCustom','NA1','NA2','NA3','NA4','NA5']
    dst.columns=['team','bye','points','vbdReg','pprPts','pprVBD','tdPts','vbdTd','pts2QB','vbd2QB','ptsCustom','vbdCustom','NA1','NA2','NA3','NA4','NA5']
    kickers.columns=["lastName","firstName","team","bye","pos","fg0039","fg4049","fg50","xp","points","vbdReg","pprPts","pprVBD","tdPts","vbdTd","pts2QB","vbd2QB","ptsCustom","vbdCustom","NA1","NA2","NA3","NA4","NA5"]
    dst['pos']='DST'
    
    ##Merge
    projections=pd.concat([qb,rb,wr,te,dst,kickers],ignore_index=True)
    projections=projections.iloc[:,5:]
    
    ##Convert variables from character strings to numeric
    cols = projections.columns.drop(['firstName','lastName','pos','team'])
    projections[cols] = projections[cols].apply(pd.to_numeric)
    
    ##Player names
    projections['player']=projections['firstName']+' '+projections['lastName']
    projections.loc[projections['pos']=='DST','player']=projections.loc[projections['pos']=='DST','team']
    projections['player']=projections['player'].str.translate(str.maketrans(dict.fromkeys(string.punctuation,'')))
    projections['player']=projections['player'].str.replace(r'\s(Sr|Jr|II|III|IV|V)$','')
    
    ##Teams
    teamsDf=pd.read_csv(directory+'nflTeams.csv').drop('city',axis=1)
    projections=projections.merge(teamsDf,left_on='team',right_on='name')
    projections=projections.drop(['team','name'],axis=1).rename(columns={'abb':'team'})
    
    ##Check for duplicates
    if projections[['player','pos']].duplicated().any():
        raise Exception('Multiple players with same name and position')
    
    ##Reorder columns
    projections=projections[['player','pos','points']+[c for c in projections if c not in ['player','pos','points']]]
    
    ##Adjust for ppr
    projections['rec']=projections['rec'].fillna(0.0)
    projections['points']=projections['points']+projections['rec']*ppr
    return projections

def numberfireProjections(directory,season,ppr=0.0):
    source='numberfire'
    ##Scrape and pickle
    if season != str(datetime.datetime.now().year) and os.path.exists(directory+source+season+'.p'):
        df=pickle.load(open(directory+source+season+'.p',"rb"))
    elif season == '2017':
        DFs=pd.read_html('https://web.archive.org/web/20170831004752/http://www.numberfire.com/nfl/fantasy/remaining-projections',header=0)
        df=pd.concat([DFs[2],DFs[3].drop(0).reset_index()],axis=1,ignore_index=True)
        pickle.dump(df,open(directory+source+season+'.p','wb'))
    elif season == str(datetime.datetime.now().year):
        DFs=pd.read_html('http://www.numberfire.com/nfl/fantasy/remaining-projections',header=0)
        df=pd.concat([DFs[0],DFs[1].drop(0).reset_index()],axis=1,ignore_index=True)
        pickle.dump(df,open(directory+source+season+'.p','wb'))
    df=df.drop([1,3,4,5],axis=1)
    df.columns=['player','points','compAtt',"passYds","passTds","passInt","rushAtt","rushYds","rushTds",'rec',"recYds","recTds"]
    projections=df
    
    ##Separate pass completions from attempts
    projections['passComp']=projections['compAtt'].str.split('/').str[0]
    projections['passAtt']=projections['compAtt'].str.split('/').str[1]
    
    ##Convert variables from character strings to numeric
    cols = projections.columns.drop(['player','compAtt'])
    projections[cols] = projections[cols].apply(pd.to_numeric)
    
    ##Player name, position, and team
    projections['pos']=projections['player'].str.extract(r'\((.*),',expand=False)
    projections['team']=projections['player'].str.extract(r',\s([A-Z]*)\)',expand=False)
    projections['player']=projections['player'].str.split(r'\s.\.').str[0]
    projections['player']=projections['player'].str.translate(str.maketrans(dict.fromkeys(string.punctuation,'')))
    projections['player']=projections['player'].str.replace(r'\s(Sr|Jr|II|III|IV|V)$','')
    
    ##Check for duplicates
    if projections[['player','pos']].duplicated().any():
        raise Exception('Multiple players with same name and position')
    
    ##Reorder columns
    projections=projections[['player','pos','points']+[c for c in projections if c not in ['player','pos','points']]]
    
    ##Adjust for ppr
    projections['rec']=projections['rec'].fillna(0.0)
    projections['points']=projections['points']+projections['rec']*ppr
    return projections

def fantasysharksProjections(directory,season,ppr=0.0):
    source='fantasysharks'
    ##Scrape and pickle
    if season == '2017':
        projections=pd.read_csv(directory+source+season+'.csv')
    elif int(season) > 2017:
        if season != str(datetime.datetime.now().year) and os.path.exists(directory+source+season+'.p'):
            DFs=pickle.load(open(directory+source+season+'.p',"rb"))
        else:
            headers={'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36'}
            r=requests.get('https://www.fantasysharks.com/apps/Projections/SeasonProjections.php?l=11&pos=ALL&format=csv&year='+season,headers=headers)
            with open(directory+source+season+'.csv','w') as fh:
                fh.write(r.text)
            df=pd.read_csv(directory+source+season+'.csv')
            rDst=requests.get('https://www.fantasysharks.com/apps/Projections/SeasonProjections.php?l=11&pos=D&format=csv&year='+season,headers=headers)
            with open(directory+source+season+'_dst.csv','w') as fh:
                fh.write(rDst.text)
            dstDf=pd.read_csv(directory+source+season+'_dst.csv',header=0)
            dstDf['Pos']='DST'
            rK=requests.get('https://www.fantasysharks.com/apps/Projections/SeasonProjections.php?l=11&pos=PK&format=csv&year='+season,headers=headers)
            with open(directory+source+season+'_k.csv','w') as fh:
                fh.write(rK.text)
            kDf=pd.read_csv(directory+source+season+'_k.csv')
            kDf['Pos']='K'
            DFs=[df,dstDf,kDf]
            pickle.dump(DFs,open(directory+source+season+'.p','wb'))
        ##Merge
        projections=pd.concat(DFs,ignore_index=True)
    
        ##Reorder first names and surnames
        projections['surname']=projections['Name'].str.split(r',\s').str[0]
        projections['firstName']=projections['Name'].str.split(r',\s').str[1]
        projections['player']=projections['firstName']+' '+projections['surname']
        projections=projections.drop(['Name','firstName','surname','Average Auction'],axis=1)
    projections['player']=projections['player'].str.translate(str.maketrans(dict.fromkeys(string.punctuation,'')))
    projections['player']=projections['player'].str.replace(r'\s(Sr|Jr|II|III|IV|V)$','')
    
    ##Rename variables
    projections=projections.rename(columns={'Pos':'pos','Team':'team','Rec':'rec','Fantasy Points':'points'})
    
    ##Convert variables from character strings to numeric
    cols = projections.columns.drop(['player','pos','team'],errors='ignore')
    projections[cols] = projections[cols].apply(pd.to_numeric)
    
    ##Check for duplicates
    if projections[['player','pos']].duplicated().any():
        raise Exception('Multiple players with same name and position')
    
    ##Reorder columns
    projections=projections[['player','pos','points']+[c for c in projections if c not in ['player','pos','points']]]
    
    ##Adjust for ppr
    projections['rec'].fillna(0.0,inplace=True)
    projections['points']=projections['points']+projections['rec']*ppr
    return projections
    
def fftodayProjections(directory,season,ppr=0.0):
    source='fftoday'
    ##Scrape and pickle
    if season != str(datetime.datetime.now().year) and os.path.exists(directory+source+season+'.p'):
        DFs=pickle.load(open(directory+source+season+'.p',"rb"))
    else:
        qb1=pd.read_html('http://www.fftoday.com/rankings/playerproj.php?Season='+season+'&PosID='+'10'+'&cur_page='+'0')[10]
        qb2=pd.read_html('http://www.fftoday.com/rankings/playerproj.php?Season='+season+'&PosID='+'10'+'&cur_page='+'1')[10]
        rb1=pd.read_html('http://www.fftoday.com/rankings/playerproj.php?Season='+season+'&PosID='+'20'+'&cur_page='+'0')[10]
        rb2=pd.read_html('http://www.fftoday.com/rankings/playerproj.php?Season='+season+'&PosID='+'20'+'&cur_page='+'1')[10]
        wr1=pd.read_html('http://www.fftoday.com/rankings/playerproj.php?Season='+season+'&PosID='+'30'+'&cur_page='+'0')[10]
        wr2=pd.read_html('http://www.fftoday.com/rankings/playerproj.php?Season='+season+'&PosID='+'30'+'&cur_page='+'1')[10]
        wr3=pd.read_html('http://www.fftoday.com/rankings/playerproj.php?Season='+season+'&PosID='+'30'+'&cur_page='+'2')[10]
        te1=pd.read_html('http://www.fftoday.com/rankings/playerproj.php?Season='+season+'&PosID='+'40'+'&cur_page='+'0')[10]
        te2=pd.read_html('http://www.fftoday.com/rankings/playerproj.php?Season='+season+'&PosID='+'40'+'&cur_page='+'1')[10]
        dst=pd.read_html('http://www.fftoday.com/rankings/playerproj.php?Season='+season+'&PosID='+'99'+'&cur_page='+'0')[10]
        kickers=pd.read_html('http://www.fftoday.com/rankings/playerproj.php?Season='+season+'&PosID='+'80'+'&cur_page='+'0')[10]
        DFs=[qb1,qb2,rb1,rb2,wr1,wr2,wr3,te1,te2,dst,kickers]
        pickle.dump(DFs,open(directory+source+season+'.p','wb'))
    qbNames=["star","player","team","bye","passComp","passAtt","passYds","passTds","passInt","rushAtt","rushYds","rushTds","points"]
    rbNames=["star","player","team","bye","rushAtt","rushYds","rushTds","rec","recYds","recTds","points"]
    wrNames=["star","player","team","bye","rec","recYds","recTds","rushAtt","rushYds","rushTds","points"]
    teNames=["star","player","team","bye","rec","recYds","recTds","points"]
    dstkNames=["star","player","points"]
    cleanedDFs=[]
    for i in range(0,len(DFs)):
        df=DFs[i].copy()
        df=df.drop([0,1])
        position=[po for po in ['QB','QB','RB','RB','WR','WR','WR','TE','TE','DST','K']][i]
        ##Add variable names
        if position in ['DST','K']:
            df=df.iloc[:,[0,1,-1]]
            df.columns=dstkNames
        elif position == 'QB':
            df.columns=qbNames
        elif position == 'RB':
            df.columns=rbNames
        elif position == 'WR':
            df.columns=wrNames
        elif position == 'TE':
            df.columns=teNames
        df['pos']=position
        cleanedDFs.append(df)
    
    ##Merge
    projections=pd.concat(cleanedDFs,ignore_index=True) #note: reorders columns
    
    ##Remove commas
    projections=projections.replace(',','')
    
    ##Convert variables from character strings to numeric
    cols = projections.columns.drop(['player','pos','team'])
    projections[cols] = projections[cols].apply(pd.to_numeric)
    
    #Player names
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

def scoutProjections(directory,season):
    source='scout'
    ##Scrape and pickle
    if season != str(datetime.datetime.now().year) and os.path.exists(directory+source+season+'.p'):
        pgDic=pickle.load(open(directory+source+season+'.p',"rb"))
    elif season == '2017':
        pgDic={}
        pgDic['QB']=pd.read_html('https://web.archive.org/web/20170829020101/http://fftoolbox.scout.com:80/football/rankings/index.php?pos=qb')[2]
        pgDic['RB']=pd.read_html('https://web.archive.org/web/20170829020101/http://fftoolbox.scout.com:80/football/rankings/index.php?pos=rb')[2]
        pgDic['WR']=pd.read_html('https://web.archive.org/web/20170829020101/http://fftoolbox.scout.com:80/football/rankings/index.php?pos=wr')[2]
        pgDic['TE']=pd.read_html('https://web.archive.org/web/20170829020101/http://fftoolbox.scout.com:80/football/rankings/index.php?pos=te')[2]
        pgDic['DST']=pd.read_html('https://web.archive.org/web/20170829020101/http://fftoolbox.scout.com:80/football/rankings/index.php?pos=def')[2]
        pgDic['K']=pd.read_html('https://web.archive.org/web/20170829020101/http://fftoolbox.scout.com:80/football/rankings/index.php?pos=k')[2]
        pickle.dump(pgDic,open(directory+source+season+'.p','wb'))
    else:            
        cert=requests.get('https://certs.godaddy.com/repository/gdig2.crt.pem').text
        with open(certifi.where(),'r+') as f:
            if cert not in f.read():
                f.write('\n'+cert)
        pgDic={}
        pgDic['QB']=pd.read_html('https://fftoolbox.scoutfantasysports.com/football/rankings/index.php?pos=qb')[2]  
        pgDic['RB']=pd.read_html('https://fftoolbox.scoutfantasysports.com/football/rankings/index.php?pos=rb')[2]
        pgDic['WR']=pd.read_html('https://fftoolbox.scoutfantasysports.com/football/rankings/index.php?pos=wr')[2]
        pgDic['TE']=pd.read_html('https://fftoolbox.scoutfantasysports.com/football/rankings/index.php?pos=te')[2]
        pgDic['DST']=pd.read_html('https://fftoolbox.scoutfantasysports.com/football/rankings/index.php?pos=def')[2]
        pgDic['K']=pd.read_html('https://fftoolbox.scoutfantasysports.com/football/rankings/index.php?pos=k')[2]
        pickle.dump(pgDic,open(directory+source+season+'.p','wb'))
    for key in pgDic.keys():
        df=pgDic[key]
        df.rename(columns={'Player':'player','Projected Pts.':'points','Pos':'pos'},inplace=True)
        df=df[['player','pos','points']]
        df=df.dropna(axis=0,how='any')
        df['player']=df['player'].str.replace(r'\s\s.*','')
        pgDic[key]=df
    
    ##Merge
    projections=pd.concat([pgDic[k] for k in pgDic.keys()] ,ignore_index=True)
    projections['pos']=projections['pos'].str.replace('Def','DST')
    
    ##Convert variables from character strings to numeric
    cols = projections.columns.drop(['player','pos'])
    projections[cols] = projections[cols].apply(pd.to_numeric)
    
    #Player name
    projections.drop(projections[projections['pos']=='DST'].index,inplace=True)
    projections['player']=projections['player'].str.translate(str.maketrans(dict.fromkeys(string.punctuation,'')))
    projections['player']=projections['player'].str.replace(r'\s(Sr|Jr|II|III|IV|V)$','')
    
    ##Check for duplicates
    if projections[['player','pos']].duplicated().any():
        raise Exception('Multiple players with same name and position')
    
    ##Reorder columns
    projections=projections[['player','pos','points']+[c for c in projections if c not in ['player','pos','points']]]
    return projections

def cbsProjections(directory,season,ppr=0.0):
    source='cbs'
    ##Scrape and pickle
    if season != str(datetime.datetime.now().year) and os.path.exists(directory+source+season+'.p'):
        DFs=pickle.load(open(directory+source+season+'.p',"rb"))
    else:
        qb=pd.read_html('https://www.cbssports.com/fantasy/football/stats/sortable/points/QB/standard/projections/'+season+'/?&print_rows=9999')[0]
        rb=pd.read_html('https://www.cbssports.com/fantasy/football/stats/sortable/points/RB/standard/projections/'+season+'/?&print_rows=9999')[0]
        wr=pd.read_html('https://www.cbssports.com/fantasy/football/stats/sortable/points/WR/standard/projections/'+season+'/?&print_rows=9999')[0]
        te=pd.read_html('https://www.cbssports.com/fantasy/football/stats/sortable/points/TE/standard/projections/'+season+'/?&print_rows=9999')[0]
        dst=pd.read_html('https://www.cbssports.com/fantasy/football/stats/sortable/points/DST/standard/projections/'+season+'/?&print_rows=9999')[0]
        kickers=pd.read_html('https://www.cbssports.com/fantasy/football/stats/sortable/points/K/standard/projections/'+season+'/?&print_rows=9999')[0]
        DFs=[qb,rb,wr,te,dst,kickers]
        pickle.dump(DFs,open(directory+source+season+'.p','wb'))
    varNames=["player","passAtt","passComp","passYds","passTds","passInt",'passRating',"rushAtt","rushYds","rushYdsPerAtt","rushTds",'recTgt',"rec","recYds","recYdsPerRec","recTds",'fumbles',"points"]
    dstNames=kNames=["player","points"]
    cleanedDFs=[]
    for i in range(0,len(DFs)):
        df=DFs[i].copy()
        position=[po for po in ['QB','RB','WR','TE','DST','K']][i]
        ##Add variable names
        if position == 'DST':
            df=df.drop([0,1]).iloc[:,[0,-1]]
            df.columns=dstNames
        elif position == 'K':
            df=df.drop([0,1]).iloc[:,[0,-1]]
            df.columns=kNames
        else:
            df=df[:-1].drop([0,1,2])
            df.columns=varNames
        df['pos']=position
        cleanedDFs.append(df)
        
    ##Merge
    projections=pd.concat(cleanedDFs,ignore_index=True) #note: reorders columns
    
    ##Convert variables from character strings to numeric
    cols = projections.columns.drop(['player','pos'])
    projections[cols] = projections[cols].apply(pd.to_numeric)
    
    #Player name and team
    projections['team']=projections['player'].str.split(',').str[1].str.strip()
    projections['player']=projections['player'].str.split(',').str[0].str.strip()
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

def yahooProjections(directory,season,ppr=0.0):
    source='yahoo'
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

def pickingprosProjections(directory,season,ppr=0.0):
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
    projections['player']=projections['player'].str.replace('Mitch Trubisky','Mitchell Trubisky')
    
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