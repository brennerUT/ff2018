import requests
import pandas as pd

keep={'qb':32,'rb':78,'wr':78,'te':25,'dst':15}
scoring='STD' # or 'HALF' or 'PPR'

def initiate(year):
    def fantPros(pos):
        res=requests.get('https://www.fantasypros.com/nfl/projections/'+pos+'.php?year='+year+'&filters=71:11:73:152&week=draft&scoring='+scoring)
        df=pd.io.html.read_html(res.text,index_col=0)[0]
        df.index=df.index.str.rsplit(None,1).str[0]
        ser=df.iloc[:,-1]
        ser.rename('points',inplace=True)
        ser2=pd.Series([pos]*ser.shape[0],index=ser.index).rename('position',inplace=True)
        df=pd.concat([ser,ser2],axis=1)
        return df
    qb_df=fantPros(pos='qb').iloc[:keep['qb'],:]
    rb_df=fantPros(pos='rb').iloc[:keep['rb'],:]
    wr_df=fantPros(pos='wr').iloc[:keep['wr'],:]
    te_df=fantPros(pos='te').iloc[:keep['te'],:]
    dst_df=fantPros(pos='dst').iloc[:keep['dst'],:]
    bigDF=pd.concat([qb_df,rb_df,wr_df,te_df,dst_df]).drop('points',axis=1)
    return bigDF
DF2017=initiate('2017')
DF2018=initiate('2018')

def add2017Results():
    posDic={'qb':'0','rb':'2','wr':'4','te':'6','dst':'16'}
    def scrape(pos):

pos='qb'
res=requests.get('http://games.espn.com/ffl/leaders?slotCategoryId='+posDic[pos]+'&leagueId=0')
df=pd.io.html.read_html(res.text)[0] 
df.drop([0,1],inplace=True)
df.rename(columns=df.loc[2,:],inplace=True)
df.drop(2,inplace=True)
df=df.loc[:,['PLAYER, TEAM POS','PTS','REC']]

df['PLAYER, TEAM POS']=df.loc[:,'PLAYER, TEAM POS'].str.replace(r'\s(Q|SSPD)$','')
df['player']=df['PLAYER, TEAM POS'].str.rsplit(None,2).str[0].str.replace(',','')
df['position']=df['PLAYER, TEAM POS'].str.rsplit(None,2).str[2]
df.drop('PLAYER, TEAM POS',axis=1,inplace=True)

 
        return
    return


