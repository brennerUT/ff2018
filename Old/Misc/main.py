import pandas as pd
import os
import sklearn.linear_model as linear_model
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import StandardScaler
import requests
os.chdir('C:/Users/ericb/Desktop/FF_machine_learning')
#%% create one dataframe with the projections from all experts ----------------
def processing(file):
    df=pd.read_csv(file)
    df=df.loc[df['team'] != 'FA']
    df=df[['player','playerposition','positionRank','points']]
    df=df.rename(columns = {'playerposition':'position','points':file[:-9]+'_proj_pts'})
    df.drop_duplicates(inplace=True)
    return df
def merge_projections(year):
    expertsDf=processing('espn_2017.csv')
    posCutoffDic={'QB':40,'RB':85,'WR':90,'TE':35,'DST':15}
    for pos in posCutoffDic.keys():
        expertsDf.drop(expertsDf[(expertsDf.position==pos)&(expertsDf.positionRank > posCutoffDic[pos])].index, inplace=True)
    expertsDf.drop('positionRank',1,inplace=True)
    for file in os.listdir():
        if file.endswith('_'+year+'.csv') and file.startswith('espn')==False:
            expertsDf=expertsDf.merge(processing(file).drop('positionRank',1),on=['player','position'],how='left')
    expertsDf.to_csv(year+'_projections_nonppr.csv',index=False)
    return
merge_projections('2017')
#%% scrape projections from FantasyData site-----------------------------------
expertsDf=pd.read_csv('2017_projections_nonppr.csv')
nullDf=expertsDf[expertsDf.fantasyData_proj_pts.isnull()]
for name in nullDf.player:
    if name in ['Rob Kelley']:
        continue
    
    # REMEMBER TO SET THE YEAR
    fDataRes=requests.get('https://fantasydata.com/nfl-stats/fantasy-football-weekly-projections.aspx?fs=0&stype=0&sn=0&scope=0&w=0&ew=0&s='+name+'&t=0&p=0&st=FantasyPoints&d=1&ls=&live=false&pid=false&minsnaps=4')
    print(name)
    df=pd.io.html.read_html(fDataRes.text)[0]
    if df.shape[0]>2:
        print('WARNING: multiple players named '+name)
        continue
    df.columns=df.iloc[0]
    expertsDf.ix[nullDf[nullDf.player==name].index,'fantasyData_proj_pts']=float(df.ix[1,'Fantasy Points'])
expertsDf.to_csv('2017_projections_nonppr_FD.csv',index=False)
#%% seanKoerner and numberFire ------------------------------------------------
yearSuff='_2016.html'
expCodeDic={'120':'seanKoerner','73':'numberFire'}
def file_to_df(expCode):
    dfDic={}
    for pos in ['qb','wr','rb','te','dst']:
        df=pd.io.html.read_html(expCode+'_'+pos+yearSuff)[0]
        df=df.loc[:,['Player','FPTS']]
        df['position']=pos.upper()
        df.rename(columns={'FPTS':expCodeDic[expCode]+'_proj_pts'},inplace=True)
        dfDic[pos]=df
    allPos=pd.concat([df for df in dfDic.values()],ignore_index=True)
    return allPos
allExpsDf=file_to_df(list(expCodeDic.keys())[0])
for exp in list(expCodeDic.keys())[1:]:
    allExpsDf=allExpsDf.merge(file_to_df(exp),on=['Player','position'],how='outer')
allExpsDf.rename(columns={'Player':'player'},inplace=True)
allExpsDf.loc[allExpsDf['position']!='DST','player']=allExpsDf.loc[allExpsDf['position']!='DST','player'].str.rsplit(None,1).str[0]
allExpsDf.loc[allExpsDf['position']=='DST','player']=allExpsDf.loc[allExpsDf['position']=='DST','player'].str.split().str[-1]
allExpsDf=allExpsDf.loc[allExpsDf.player!='Ryan Hewitt']
proj16df=pd.read_csv('2016_projections_nonppr.csv')
proj16df=proj16df.merge(allExpsDf,on=['player','position'],how='left')
proj16df.to_csv('2016_projections_nonppr.csv',index=False)
#%% combining actual 2016 scores with projections
actualDf=pd.read_csv('2016_actual_points.csv')
actualDf.drop('ppr_points',axis=1,inplace=True)
actualDf.rename(columns = {'nonppr_points':'actual_points'},inplace=True)
expertsDf=pd.read_csv('2016_projections_nonppr.csv')
masterDf=actualDf.merge(expertsDf,on=['player','position'],how='right')
#%% machine learning
def ridge_pipeline(df,df_2017):
    df=df.drop(['numberFire_proj_pts','seanKoerner_proj_pts'],axis=1)
    df=df.dropna(axis=1, how='all')
    df=df.dropna(axis=0, how='any')
    x_unscaled=df.filter(regex=('.*_proj_pts'))
    x=StandardScaler().fit_transform(x_unscaled)
    y=df.actual_points
    param_grid={'alpha':[0.0001,0.001,0.1,1,10,100,1000]}
    grid = GridSearchCV(linear_model.Ridge(), param_grid, cv=10,n_jobs=-1)
    grid.fit(x, y)
    best_alph=grid.best_params_['alpha']
    if best_alph in [0.0001,1000]:
        return 'WARNING: best_alph at endpoint'+': '+str(best_alph)
    else:
        ridge=linear_model.Ridge(alpha=best_alph).fit(x,y)
        df_2017=df_2017.dropna(axis=1, how='all')
        df_2017=df_2017.dropna(axis=0, how='any')
        x_2017=df_2017.loc[:,list(x_unscaled)]
        x_2017=StandardScaler().fit_transform(x_2017)
        df_2017['my_proj']=ridge.predict(x_2017)
        return df_2017.loc[:,['player','position','my_proj']].sort_values('my_proj',ascending=False)
df_2017=pd.read_csv('2017_projections_nonppr.csv')
d={}
for pos in ['DST','QB','RB','WR','TE']:
    result=ridge_pipeline(masterDf.loc[masterDf['position']==pos],df_2017.loc[df_2017['position']==pos])
    d[pos]=result
myProjDf=pd.concat([df for df in d.values()],ignore_index=True)
vorDic={'DST':3.0,'QB':7.0,'TE':10.0,'RB':39.0,'WR':43.0}
#add D. Pumphrey,Kyle Juszczyk, Mike Tolbert, Bridgewater,Christian Hackenberg,
myProjDf['posRank'] = myProjDf.groupby(['position'])['my_proj'].rank(ascending=False)
for name, group in myProjDf.groupby('position'):
    repl=vorDic[name]
    vor=group.loc[group['posRank'].between(repl-1,repl+1),'my_proj'].mean()
    myProjDf.loc[myProjDf.position==name,'VOR']=group['my_proj']-vor
myProjDf.sort_values('VOR',ascending=False,inplace=True)
myProjDf.player.to_csv('player_rankings.txt',index=False,header=False)
