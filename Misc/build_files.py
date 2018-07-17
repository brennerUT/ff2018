import pandas as pd
import os
import requests
os.chdir('C:/Users/ericb/Desktop/ff2018')
#%%
ppr='1'
#%%
def beersheets(year):
    year=str(year)
    if year == '2017':
        baseurl='https://www.dropbox.com/sh/suwt2igewsqdiuj/AACyNzrOjOvTDGGCVQNfZEZEa/Standard%20Snake/14%20Team/'
        fullurl=baseurl+ppr+'%20PPR/1%20QB/2017-09-05%2014%20TM%20'+ppr+'%20PPR%201QB%202RB%202WR%201TE%201FLX%204%20PaTD%20Snake.xlsx?dl=1'
    elif year == '2018':
        baseurl='https://footballabsurdity.com/wp-content/plugins/BeerSheetRequests/CURRENT/14,'
        fullurl=baseurl+ppr+',1,2,2,1,1,0,0,0,4,6,6,0.04,0.1,0.1,-2,0,0,.xlsx'
    df=pd.read_excel(fullurl,index_col=1,header=4)
    dstDf=df[['TM/BW','VAL']].iloc[-15:].rename(columns={'TM/BW':'player'})
    dstDf['position']='dst'
    dstDf.drop('VAL',axis=1,inplace=True)
    dstDf['beerSheetsProjPts']=range(15,0,-1)
    dstDf['player']=dstDf['player'].str.rsplit(None,1).str[1]
    df=df.filter(regex=('(NAME.*)|(VAL.*)')).reset_index().drop('index',axis=1).iloc[0:78]
    df.loc[df.index[0:32],'position']='qb'
    df.loc[df.index[32:],'position']='te'
    qb_te_df=df[['NAME','VAL','position']].rename(columns={'NAME':'player','VAL':'beerSheetsProjPts'}).drop([32,33,34]).reset_index(drop=True)[:57]
    rb_df=df[['NAME (POS)','VAL.1']].rename(columns={'NAME (POS)':'player','VAL.1':'beerSheetsProjPts'})
    wr_df=df[['NAME (POS).1','VAL.2']].rename(columns={'NAME (POS).1':'player','VAL.2':'beerSheetsProjPts'})
    df=pd.concat([qb_te_df,rb_df],ignore_index=True)
    df.fillna('rb',inplace=True)
    df=pd.concat([df,wr_df,dstDf],ignore_index=True)
    df.fillna('wr',inplace=True)
    df['player']=df['player'].str.replace(r'\s\(.*$','')
    df=df[['player','position','beerSheetsProjPts']].reset_index(drop=True)
    df.to_csv(year+'_projections.csv',index=False)
    return
#%%
beersheets(2017)
beersheets(2018)
#%%
def getActualPts():
    posDic={'qb':'0','rb':'2','wr':'4','te':'6','dst':'16'}
    def procc_page(pos,page):
        res=requests.get('http://games.espn.com/ffl/leaders?slotCategoryId='+posDic[pos]+'&leagueId=0'+'&startIndex='+str(50*(page-1)))
        df=pd.io.html.read_html(res.text)[0] 
        df.drop([0,1],inplace=True)
        df.rename(columns=df.loc[2,:],inplace=True)
        df.drop(2,inplace=True)
        if pos == 'dst':
            df=df.loc[:,['PLAYER, TEAM POS','PTS']]
            df['REC']=0
        else:
            df=df.loc[:,['PLAYER, TEAM POS','PTS','REC']]
        df['PLAYER, TEAM POS']=df.loc[:,'PLAYER, TEAM POS'].str.replace(r'\s(O|Q|SSPD)$','')
        df['player']=df['PLAYER, TEAM POS'].str.rsplit(None,2).str[0].str.replace(',','')
        df['position']=df['PLAYER, TEAM POS'].str.rsplit(None,2).str[2]
        df.drop('PLAYER, TEAM POS',axis=1,inplace=True)
        return df
    dfDic={}
    for pos in posDic.keys():
        if pos in ['wr','rb']:
            dfDic[pos]=pd.concat([procc_page(pos,pg) for pg in [1,2,3,4,6]],ignore_index=True)
        elif pos in ['qb','te']:
            dfDic[pos]=pd.concat([procc_page(pos,pg) for pg in [1,2]],ignore_index=True)
        else:
            dfDic[pos]=procc_page(pos,1)
    bigdf=pd.concat([df for df in dfDic.values()],ignore_index=True).drop_duplicates()
    bigdf['player']=bigdf['player'].str.replace(r'\s(Jr.|Sr.|V|II)$','')
    bigdf['player']=bigdf['player'].str.replace(r"\*|'",'')
    bigdf['player']=bigdf['player'].str.replace('\.J\.','J')
    bigdf['player']=bigdf['player'].str.replace('T\.Y\.','TY')
    bigdf=bigdf.drop('position',axis=1).rename(columns={'PTS':'actualPts'})
    playerDf=pd.read_csv('2017_projections.csv').drop('beerSheetsProjPts',axis=1)
    playerDf=playerDf.merge(bigdf,on='player',how='left')
    playerDf.at[playerDf['player']=='Darren McFadden','actualPts']=-0.2
    playerDf.at[playerDf['player']=='Darren McFadden','REC']=0
    return playerDf
#%%
getActualPts().to_csv('2017_actualPts_1PPR.csv',index=False)
#%%
