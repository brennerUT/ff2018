import pandas as pd
import os
import sklearn.linear_model as linear_model
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import StandardScaler
import numpy as np
import requests
import re
import time
os.chdir('C:/Users/ericb/Desktop/FF_machine_learning')
#%%
def beersheets_2017(day,df=None):
    day=str(day)
    if df is None:
        res=requests.get('https://www.reddit.com/user/Beer4TheBeerGod/submitted/',headers={'user-agent':'Mozilla/5.0'})
        baseWeekUrl='https://www.reddit.com/r/fantasyfootball/comments'
        weekUrl=baseWeekUrl+re.search('/[^/]*/beersheets_201708'+day+'_[^/]*/',res.text).group(0)
        res2=requests.get(weekUrl,headers={'user-agent':'Mozilla/5.0'})
        cloudUrl=re.search('http://64.52.85.212/nextcloud/index.php/s/[^)]*',res2.text).group(0)
        xlsxUrl=cloudUrl+'/download?path=%2FStandard%20Snake%2F10%20Team%2F0%20PPR%2F1%20QB&files=2017-08-'+day+'%2010%20TM%200%20PPR%201QB%202RB%202WR%201TE%201FLX%204%20PaTD%20Snake.xlsx'
        df=pd.read_excel(xlsxUrl,index_col=1,header=4)
    df=df.filter(regex=('(NAME.*)|(VAL.*)')).reset_index().drop('index',axis=1).iloc[0:60]
    df.ix[0:32,'position']='QB'
    df.ix[32:,'position']='TE'
    qb_te_df=df[['NAME','VAL','position']].rename(columns={'NAME':'player','VAL':'beerSheets_proj_pts'}).drop([32,33,34])
    rb_df=df[['NAME (POS)','VAL.1']].rename(columns={'NAME (POS)':'player','VAL.1':'beerSheets_proj_pts'})
    wr_df=df[['NAME (POS).1','VAL.2']].rename(columns={'NAME (POS).1':'player','VAL.2':'beerSheets_proj_pts'})
    df=pd.concat([qb_te_df,rb_df],ignore_index=True)
    df.fillna('RB',inplace=True)
    df=pd.concat([df,wr_df],ignore_index=True)
    df.fillna('WR',inplace=True)
    df['player']=df['player'].str.replace(r'\s\(.*$','')
    df=df[['player','position','beerSheets_proj_pts']].reset_index().drop('index',axis=1)
    df.to_csv('2017_projections.csv',index=False)
    return
#%%
def add_espn(year):
    year=str(year)
    posDic={'QB':'0','RB':'2','WR':'4','TE':'6','DST':'16'}
    cutoffs={'QB':40,'RB':85,'WR':90,'TE':35,'DST':15}
    dfDic={}
    def procc_page(pos,page):
        res=requests.get('http://games.espn.com/ffl/tools/projections?&seasonId='+year+'&leagueId=156099&slotCategoryId='+posDic[pos]+'&startIndex='+str(40*(page-1)))
        df=pd.io.html.read_html(res.text)[0]
        df.drop([0,1],inplace=True)
        df.rename(columns=df.loc[2,:],inplace=True)
        df.drop(2,inplace=True)
        df=df.loc[:,['RNK','PLAYER, TEAM POS','PTS']]
        df.RNK=pd.to_numeric(df.RNK)
        df=df.loc[df['RNK'] <= cutoffs[pos]]
        df['PLAYER, TEAM POS']=df['PLAYER, TEAM POS'].str.replace(r'\s(Q|SSPD|O)$','')
        # Ty Montgomery
        df['player']=df['PLAYER, TEAM POS'].str.rsplit(None,2).str[0].str.replace(',','')
        df['position']=df['PLAYER, TEAM POS'].str.rsplit(None,2).str[2]
        df.drop('PLAYER, TEAM POS',axis=1,inplace=True)
        df.rename(columns={'RNK':'posRank','PTS':'espn_proj_pts'},inplace=True)
        return df
    for pos in posDic.keys():
        if pos in ['WR','RB']:
            dfDic[pos]=pd.concat([procc_page(pos,pg) for pg in [1,2,3]],ignore_index=True)
        else:
            dfDic[pos]=procc_page(pos,1)
    bigdf=pd.concat([df for df in dfDic.values()],ignore_index=True)
    bigdf.drop('posRank',axis=1,inplace=True)
    bigdf=bigdf[['player','position','espn_proj_pts']]
    bigdf['player']=bigdf['player'].str.replace(r'\s(Jr.|Sr.|V)$','')
    bigdf['player']=bigdf['player'].str.replace(r"\*|'",'')
    bigdf['player']=bigdf['player'].str.replace('\.J\.','J')
    bigdf['player']=bigdf['player'].str.replace('T\.Y\.','TY')
    bigdf['player']=bigdf['player'].str.replace('Robert Kelley','Rob Kelley')
    bigdf['position']=bigdf['position'].str.replace(r'D/ST','DST')
    multisource_df=pd.read_csv(year+'_projections.csv')
    multisource_df=multisource_df.merge(bigdf,on=['player','position'],how='left')
    multisource_df=multisource_df.merge(bigdf.loc[bigdf['position']=='DST'],on=['player','position','espn_proj_pts'],how='outer')
    multisource_df.to_csv(year+'_projections.csv',index=False)
    return
#%%
def add_fantasyData(years_ago,year):
    years_ago=str(years_ago)
    year=str(year)
    mastDf=pd.read_csv(year+'_projections.csv')
    mastDf['fantasyData_proj_pts']=np.nan
    mastDf['player_espn']=mastDf['player']
    mastDf.player=mastDf.player.str.replace('.','')
    mastDf.player=mastDf.player.str.lower()
    posDic={'QB':'1','RB':'2','WR':'3','TE':'4','DST':'6','all':'0'}
    def procc_page(pos='all',name='',team=0,mastDf=mastDf):
        res=requests.get('https://fantasydata.com/nfl-stats/fantasy-football-weekly-projections.aspx?fs=0&stype=0&sn='
                         +str(years_ago)+'&scope=0&w=0&ew=0&s='+name+'&t='+str(team)+'&p='
                         +posDic[pos]+'&st=FantasyPoints&d=1&ls=&live=false&pid=false&minsnaps=4')
        df=pd.io.html.read_html(res.text)[0]
        df.columns=df.iloc[0] #changes header row
        df.drop(0,inplace=True)
        df=df[['Player','Pos','Fantasy Points',]]
        df.rename(columns={'Player':'player','Pos':'position','Fantasy Points':'fantasyData_proj_pts_x'},inplace=True)
        df.fantasyData_proj_pts_x=pd.to_numeric(df.fantasyData_proj_pts_x)
        if name!='' and df.shape[0]>2:
            raise Exception('multiple players named '+name)
        df.loc[df.position=='DST','player']=df.loc[df.position=='DST','player'].str.split().str[-1]
        df.player=df.player.str.lower()
        df['player']=df['player'].str.replace(r'\s(jr|sr|v)$','')
        df['player']=df['player'].str.replace(r"'",'')
        mastDf=mastDf.merge(df,on=['player','position'],how='left')
        mastDf['fantasyData_proj_pts'].fillna(mastDf['fantasyData_proj_pts_x'],inplace=True)
        mastDf.drop('fantasyData_proj_pts_x',axis=1,inplace=True)
        return mastDf
    for pos in posDic.keys():
        mastDf=procc_page(pos,mastDf=mastDf)
    for t in range(1,33):
        mastDf=procc_page(team=t,mastDf=mastDf)
    mastDf.player=mastDf.player.str.replace(r'\s(jr|sr|v)$','')
    nullDf=mastDf[mastDf.fantasyData_proj_pts.isnull()]
    for index, row in nullDf.iterrows():
        try:
            mastDf=procc_page(row['position'],name=row['player'],mastDf=mastDf)
        except:
            print(row['player'])
    player=mastDf['player_espn']
    mastDf.drop(['player','player_espn'],axis=1,inplace=True)
    mastDf.insert(0, 'player', player)
    mastDf.to_csv(year+'_projections.csv',index=False)
    return
#%%
def add_fantasySharks(year):
    year=str(year)
    mastDf=pd.read_csv(year+'_projections.csv')
    mastDf['fantasySharks_proj_pts']=np.nan
    mastDf['player_espn']=mastDf['player']
    mastDf.player=mastDf.player.str.replace(r'\s(Jr.|Sr.|V|III)$','')
    mastDf.player=mastDf.player.str.replace("'",'')
    mastDf.player=mastDf.player.str.replace('Robert Kelley','Rob Kelley')
    mastDf.player=mastDf.player.str.replace('Benjamin Cunningham','Benny Cunningham')
    if time.time() - os.path.getmtime('C:/Users/ericb/Downloads/sharks.csv') > 86400:
        raise Exception('FanatasySharks file is old')
    df=pd.read_csv('C:/Users/ericb/Downloads/sharks.csv')
    df=df.loc[df['team'] != 'FA']
    df=df[['player','playerposition','points']]
    df=df.rename(columns = {'playerposition':'position','points':'fantasySharks_proj_pts_x'})
    df.drop_duplicates(inplace=True)
    new_Ty=df.loc[df.player=='Ty Montgomery',:]
    new_Ty['position']='RB'
    df=df.append(new_Ty,ignore_index=True)
    df['player']=df['player'].str.replace('\.J\.','J')
    df['player']=df['player'].str.replace('T\.Y\.','TY')
    mastDf=mastDf.merge(df,on=['player','position'],how='left')
    mastDf['fantasySharks_proj_pts'].fillna(mastDf['fantasySharks_proj_pts_x'],inplace=True)
    player=mastDf['player_espn']
    mastDf.drop(['fantasySharks_proj_pts_x','player','player_espn'],axis=1,inplace=True)
    mastDf.insert(0, 'player', player)
    mastDf.to_csv(year+'_projections.csv',index=False)
    return
#%% scrape FFToday ------------------------------------------------------------
def add_FFToday(year):
    year=str(year)
    posDic={'QB':'10','RB':'20','WR':'30','TE':'40','DST':'99'}
    mastDf=pd.read_csv(year+'_projections.csv')
    mastDf['ffToday_proj_pts']=np.nan
    mastDf['player_espn']=mastDf['player']
    mastDf.player=mastDf.player.str.replace(r'\s(Sr.|V)$','')
    mastDf.player=mastDf.player.str.replace('Robert Kelley','Rob Kelley')
    mastDf.player=mastDf.player.str.replace('Benjamin Cunningham','Benny Cunningham')
    mastDf.player=mastDf.player.str.replace('Duke Johnson Jr.','Duke Johnson')
    def procc_page(pos,page=1,mastDf=mastDf):
        res=requests.get('http://www.fftoday.com/rankings/playerproj.php?Season='
                         +year+'&PosID='+posDic[pos]+'&LeagueID=26955&cur_page='+str(page-1))
        df=pd.io.html.read_html(res.text)[10]
        df.columns=df.iloc[1]
        df.drop([0,1],inplace=True)
        if pos=='DST':
            df.rename(columns={'Team':'player','FPts':'ffToday_proj_pts_x'},inplace=True)
            df.player=df.player.str.split().str[-1]
        else:
            df.rename(columns={'Player  Sort First: Last:':'player','FPts':'ffToday_proj_pts_x'},inplace=True)
        df['position']=pos
        df=df[['player','position','ffToday_proj_pts_x']]
        df['player']=df['player'].str.replace('\.J\.','J')
        df['player']=df['player'].str.replace('T\.Y\.','TY')
        df['player']=df['player'].str.replace(r'\s(Jr.|Sr.|V)$','')
        df['player']=df['player'].str.replace(r"'",'')
        mastDf=mastDf.merge(df,on=['player','position'],how='left')
        mastDf['ffToday_proj_pts'].fillna(mastDf['ffToday_proj_pts_x'],inplace=True)
        mastDf.drop('ffToday_proj_pts_x',axis=1,inplace=True)
        return mastDf
    for pos in posDic.keys():
        mastDf=procc_page(pos,mastDf=mastDf)
        if pos in ['WR','RB']:
            mastDf=procc_page(pos,page=2,mastDf=mastDf)
    player=mastDf['player_espn']
    mastDf.drop(['player','player_espn'],axis=1,inplace=True)
    mastDf.insert(0, 'player', player)
    mastDf.to_csv(year+'_projections.csv',index=False)
    return
#%% CBS scraping --------------------------------------------------------------
def add_cbs(year):
    year=str(year)
    posDic={'QB':'10','RB':'20','WR':'30','TE':'40','DST':'99'}
    mastDf=pd.read_csv(year+'_projections.csv')
    mastDf['cbs_proj_pts']=np.nan
    mastDf['player_espn']=mastDf['player']
    mastDf.player=mastDf.player.str.replace(r'\s(Jr.|Sr.|V)$','')
    mastDf.player=mastDf.player.str.replace('Robert Kelley','Rob Kelley')
    mastDf.player=mastDf.player.str.replace('Benjamin Cunningham','Benny Cunningham')
    def procc_page(pos,page=1,mastDf=mastDf):
        res=requests.get('http://www.cbssports.com/fantasy/football/stats/sortable/points/'
                         +pos+'/standard/projections/'+year+'/?&print_rows=9999')
        df=pd.io.html.read_html(res.text)[0]
        if pos=='DST':
            df.columns=df.iloc[1]
            df.drop([0,1],inplace=True)
        else:
            df.columns=df.iloc[2]
            df.drop([0,1,2],inplace=True)
        df.rename(columns={'Player':'player','FPTS':'cbs_proj_pts_x'},inplace=True)
        df['position']=pos
        df=df[['player','position','cbs_proj_pts_x']]
        df=df[:-1]
        df['player']=df.player.str.split(',').str[0]
        df['player']=df['player'].str.replace('\.J\.','J')
        df['player']=df['player'].str.replace('T\.Y\.','TY')
        df['player']=df['player'].str.replace(r"'",'')
        mastDf=mastDf.merge(df,on=['player','position'],how='left')
        mastDf['cbs_proj_pts'].fillna(mastDf['cbs_proj_pts_x'],inplace=True)
        mastDf.drop('cbs_proj_pts_x',axis=1,inplace=True)
        return mastDf
    for pos in posDic.keys():
        mastDf=procc_page(pos,mastDf=mastDf)
    player=mastDf['player_espn']
    mastDf.drop(['player','player_espn'],axis=1,inplace=True)
    mastDf.insert(0, 'player', player)
    mastDf.to_csv(year+'_projections.csv',index=False)
    return
#%%
def numberfire_scraping_2016(pos):
    res=requests.get('https://web.archive.org/web/20160824162545/http://www.numberfire.com:80/nfl/fantasy/fantasy-football-cheat-sheet/'+pos)
    df1=pd.io.html.read_html(res.text)[0]
    df2=pd.io.html.read_html(res.text)[1]
    df3=pd.concat([df1,df2],axis=1)
    return df3
def add_numberfire_2017():
    year=str(2017)
    posDic={'QB':'qb','RB':'rb','WR':'wr','TE':'te','DST':'d'}
    mastDf=pd.read_csv(year+'_projections.csv')
    mastDf['numberFire_proj_pts']=np.nan
    def procc_page(pos,page=1,mastDf=mastDf):
        res=requests.get('https://www.numberfire.com/nfl/fantasy/fantasy-football-cheat-sheet/'+posDic[pos])
        df=pd.io.html.read_html(res.text)[0]
        df.rename(columns=lambda x: x.strip(),inplace=True)
        df.rename(columns={'Player':'player','FP':'numberFire_proj_pts_x'},inplace=True)
        df['position']=pos
        df=df[['player','position','numberFire_proj_pts_x']]
        df['player']=df.player.str.split(r'\sUndraft\s*').str[1]
        if pos=='DST':
            df['player']=df['player'].str.replace('\s*D/ST\s.*','')
            df['player']=df['player'].str.strip()
            teamDic={
                    'Seattle':'Seahawks',
                    'Denver':'Broncos',
                    'Kansas City':'Chiefs',
                    'Houston':'Texans',
                    'Arizona':'Cardinals',
                    'Minnesota':'Vikings',
                    'New England':'Patriots',
                    'New York Giants':'Giants',
                    'Carolina':'Panthers',
                    'Cincinnati':'Bengals',
                    'Baltimore':'Ravens',
                    'Los Angeles Rams':'Rams',
                    'Jacksonville':'Jaguars',
                    'Philadelphia':'Eagles',
                    'Atlanta':'Falcons',
                    'Pittsburgh':'Steelers',
                    'Oakland':'Raiders',
                    'Tampa Bay':'Buccaneers',
                    'Los Angeles Chargers':'Chargers',
                    'Miami':'Dolphins',
                    'Buffalo':'Bills',
                    'Chicago':'Bears',
                    'Green Bay':'Packers',
                    'New York Jets':'Jets',
                    'Tennessee':'Titans',
                    'Detroit':'Lions',
                    'Dallas':'Cowboys',
                    'Washington':'Redskins',
                    'San Francisco':'49ers',
                    'Cleveland':'Browns',
                    'Indianapolis':'Colts',
                    'New Orleans':'Saints'
                    }
            df=df.replace(teamDic)
        else:
            df['player']=df['player'].str.replace('\s.\.\s.*','')
            df['player']=df['player'].str.replace('\.J\.','J')
            df['player']=df['player'].str.replace('T\.Y\.','TY')
            df['player']=df['player'].str.replace(r"'",'')
        df['player']=df['player'].str.strip()
        df['player']=df['player'].str.replace(r'\s*(Jr.|Sr.|V)$','')
        df['player']=df['player'].str.replace(r'Lesean McCoy','LeSean McCoy')
        mastDf=mastDf.merge(df,on=['player','position'],how='left')
        mastDf['numberFire_proj_pts'].fillna(mastDf['numberFire_proj_pts_x'],inplace=True)
        mastDf.drop('numberFire_proj_pts_x',axis=1,inplace=True)
        return mastDf
    for pos in posDic.keys():
        mastDf=procc_page(pos,mastDf=mastDf)
    mastDf.to_csv(year+'_projections.csv',index=False)
    return
#%%
def add_FFAnalytics(year,source):
    year=str(year)
    mastDf=pd.read_csv(year+'_projections.csv')
    if source == 'ffAnalytics_weighted':
        fn='weighted.csv'
    elif source == 'fantasySharks':
        fn='sharks.csv'
    else:
        fn=source+'.csv'
    mastDf[source+'_proj_pts']=np.nan
    if time.time() - os.path.getmtime('C:/Users/ericb/Downloads/'+fn) > 86400:
        raise Exception(source+' file is old')
    df=pd.read_csv('C:/Users/ericb/Downloads/'+fn)
    df.loc[df['player']=='Jeremy Maclin','team']='BAL'
    df.loc[df['player']=='Justin Forsett','team']='BAL'
    df=df.loc[df['team'] != 'FA']
    df=df[['player','playerposition','points']]
    df=df.rename(columns = {'playerposition':'position','points':source+'_proj_pts_x'})
    df.drop_duplicates(inplace=True)
    df['player']=df['player'].str.replace('\.J\.','J')
    df['player']=df['player'].str.replace('T\.Y\.','TY')
    mastDf=mastDf.merge(df,on=['player','position'],how='left')
    mastDf[source+'_proj_pts'].fillna(mastDf[source+'_proj_pts_x'],inplace=True)
    mastDf.drop(source+'_proj_pts_x',axis=1,inplace=True)
    mastDf.to_csv(year+'_projections.csv',index=False)
    return
#%% scrape Scout.com ----------------------------------------------------------
def add_scout(year):
    year=str(year)
    mastDf=pd.read_csv(year+'_projections.csv')
    mastDf['scout_proj_pts']=np.nan
    posDic={'QB':'qb','RB':'rb','WR':'wr','TE':'te','DST':'def'}
    def procc_page(pos,page=1,mastDf=mastDf):
        if year == '2016':
            raise Exception('May not work for current year')
        headers={ 
                'Host': 'fftoolbox.scout.com',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.8',
                'Cookie': '__qca=P0-310033962-1499354829809; ATC=8047c1fb-4e59-41d0-a813-09ac4f3081a7; GID=1f642163-a9fb-4a52-8c0e-5e718c09e648; optimizelyEndUserId=oeu1503286824710r0.1190343956944302; CBS_INTERNAL=0; s_vnum=1505878828185%26vn%3D1; AMCV_10D31225525FF5790A490D4D%40AdobeOrg=-227196251%7CMCMID%7C00347519072957567933083881010212837704%7CMCAAMLH-1503891628%7C9%7CMCAAMB-1503891628%7CNRX38WO0n5BH8Th-nqAG_A%7CMCOPTOUT-1503294028s%7CNONE%7CMCAID%7C2BD0907B851D0608-4000015120016862%7CMCCIDH%7C1691448318; CFID=2535496; CFTOKEN=27ad73d9d0ffcdd2-1CEB9CE5-D951-32AB-427B8E3C2EB76239; ASC=4d4b3bc3-7a83-4fef-8216-4567306b89f9; optimizelySegments=%7B%225464210744%22%3A%22none%22%2C%225451640945%22%3A%22referral%22%2C%225456550765%22%3A%22false%22%2C%225449612654%22%3A%22gc%22%7D; optimizelyBuckets=%7B%7D; XFP_FIRSTPAGE=0; utag_main=v_id:015d1b1c156b0013187237993f3104073005706b0086e$_sn:4$_ss:0$_st:1503288934008$ses_id:1503286827348%3Bexp-session$_pn:4%3Bexp-session; s_invisit=true; s_getNewRepeat=1503287134380-Repeat; s_lv_undefined=1503287134380; s_lv_undefined_s=More%20than%207%20days; b2b-aam-segments=t%3DSoftware%2CProject%20Management%2CAfter%20Hours; aam_uuid=00126623782825012493070240543081815088; PHPSESSID=52hrkd6k7ss2qm2f82q1kn6a77; surround=e|4; _ga=GA1.2.1429139302.1499354829; _gid=GA1.2.350625261.1503286827; __utma=113414992.1429139302.1499354829.1503286893.1503286893.1; __utmb=113414992.4.10.1503286893; __utmc=113414992; __utmz=113414992.1503286893.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); com.silverpop.iMAWebCookie=4a9ed11e-010e-0501-3426-755a88a78cb6; com.silverpop.iMA.session=c2a8bb4d-57c9-74a3-6cc7-6ab4165be9ba; XFP_FIRSTPAGE=0'
                }
        res=requests.get('http://fftoolbox.scout.com/football/rankings/index.php?noppr=true&qb4=true&pos='+posDic[pos],headers=headers)
        df=pd.io.html.read_html(res.text)[0]

        df.rename(columns={'Player':'player','Projected Pts.':'scout_proj_pts_x'},inplace=True)
        df['position']=pos
        df=df[['player','position','scout_proj_pts_x']]
        df.dropna(axis=0,how='any',inplace=True)
        df['player']=df['player'].str.replace(r'\s\s.*','')
        if pos=='DST':
            teamDic={
                    'Seattle':'Seahawks',
                    'Denver':'Broncos',
                    'Kansas City':'Chiefs',
                    'Houston':'Texans',
                    'Arizona':'Cardinals',
                    'Minnesota':'Vikings',
                    'New England':'Patriots',
                    'New York Giants':'Giants',
                    'Carolina':'Panthers',
                    'Cincinnati':'Bengals',
                    'Baltimore':'Ravens',
                    'Los Angeles':'Rams',
                    'Jacksonville':'Jaguars',
                    'Philadelphia':'Eagles',
                    'Atlanta':'Falcons',
                    'Pittsburgh':'Steelers',
                    'Oakland':'Raiders',
                    'Tampa Bay':'Buccaneers',
                    'San Diego':'Chargers',
                    'Miami':'Dolphins',
                    'Buffalo':'Bills',
                    'Chicago':'Bears',
                    'Green Bay':'Packers',
                    'New York Jets':'Jets',
                    'Tennessee':'Titans',
                    'Detroit':'Lions',
                    'Dallas':'Cowboys',
                    'Washington':'Redskins',
                    'San Francisco':'49ers',
                    'Cleveland':'Browns',
                    'Indianapolis':'Colts',
                    'New Orleans':'Saints'
                    }
            df=df.replace(teamDic)
        df['player']=df['player'].str.replace('\.J\.','J')
        df['player']=df['player'].str.replace('Ty Hilton','TY Hilton')
        df['player']=df['player'].str.replace(r"'",'')
        mastDf=mastDf.merge(df,on=['player','position'],how='left')
        mastDf['scout_proj_pts'].fillna(mastDf['scout_proj_pts_x'],inplace=True)
        mastDf.drop('scout_proj_pts_x',axis=1,inplace=True)
        return mastDf
    for pos in posDic.keys():
        mastDf=procc_page(pos,mastDf=mastDf)
    mastDf.to_csv(year+'_projections.csv',index=False)
    return
#%%
def cleanup(year):
    year=str(year)
    df1=pd.read_csv(year+'_projections.csv')
    df1.to_csv(year+'_projections_uncleaned.csv',index=False)
    df1.replace(0,np.nan,inplace=True)
    if df1.isnull().sum(axis=1).max() > 5:
        raise Exception('Some rows are mainly NaNs')
## fill missing values
    def calcRatioAndFill(df):
        df.dropna(axis=1,how='all',inplace=True)
        if df.isnull().values.any() == False:
            return df
        df['median']=df.median(axis=1)
        for source in list(df.filter(regex=('.*_proj_pts'))):
            if df[source].isnull().values.any():
                if df[source].isnull().sum() > df[source].shape[0]/2.0:
                    raise Exception('Most values are missing')
                df['ratio']=df[source]/df['median']
                medRatio=df['ratio'].median()
                df[source].fillna(df['median']*medRatio,inplace=True)
                df.drop('ratio',axis=1,inplace=True)
        return df.drop('median',axis=1)
    d={}
    for pos in ['DST','QB','RB','WR','TE']:
        d[pos]=calcRatioAndFill(df1.loc[df1['position']==pos])
    df2=pd.concat([x for x in d.values()])
    df2=df2.loc[:,list(df1)]
## check for duplicates
    if df2['player'].duplicated().values.any():
        raise Exception('Duplicate names')
    df2.to_csv(year+'_projections.csv',index=False)
    return
#%% machine learning ----------------------------------------------------------
def machine_learning(train_file,predict_file):
    def ridge_pipeline(df,df_2017):
        x_unscaled=df.filter(regex=('.*_proj_pts'))
        x_unscaled.dropna(axis=1,how='all',inplace=True)
        x=StandardScaler().fit_transform(x_unscaled)
        y=df.actual_points
        param_grid={'alpha':[0.0001,0.001,0.1,1,10,100,500,1000]}
        grid = GridSearchCV(linear_model.Ridge(), param_grid, cv=10,n_jobs=-1)
        grid.fit(x, y)
        best_alph=grid.best_params_['alpha']
        if best_alph in [0.0001,1000]:
            raise Exception('best_alph at endpoint'+': '+str(best_alph))
        else:
            x_2017=df_2017.loc[:,list(x_unscaled)]
            x_2017.dropna(axis=1,how='all',inplace=True)
            x_2017=StandardScaler().fit_transform(x_2017)
            df_2017['my_proj']=grid.predict(x_2017)
            return df_2017.loc[:,['player','position','my_proj']].sort_values('my_proj',ascending=False)
    masterDf=pd.read_csv(train_file)
    df_2017=pd.read_csv(predict_file)
    d={}
    for pos in ['DST','QB','RB','WR','TE']:
        result=ridge_pipeline(masterDf.loc[masterDf['position']==pos],df_2017.loc[df_2017['position']==pos])
        d[pos]=result
    myProjDf=pd.concat([df for df in d.values()],ignore_index=True)
    myProjDf.to_csv('my_projections.csv',index=False)
    return
#%%
def calc_VORs():
    myProjDf=pd.read_csv('my_projections.csv')
    vorDic={'DST':3.0,'QB':7.0,'TE':10.0,'RB':39.0,'WR':43.0,'flex':92.0}
    myProjDf['posRank'] = myProjDf.groupby(['position'])['my_proj'].rank(ascending=False)
    for name, group in myProjDf.groupby('position'):
        repl=vorDic[name]
        vor=group.loc[group['posRank'].between(repl-1,repl+1),'my_proj'].mean()
        myProjDf.loc[myProjDf.position==name,'VOR']=group['my_proj']-vor
    negVOR=myProjDf.loc[myProjDf['VOR']<0]
    for name, group in negVOR.groupby('position'):
        negVOR.loc[group.index,'VOR']=group['my_proj']-group['my_proj'].min()
    negVOR.loc[:,'VOR']=negVOR['VOR']-negVOR['VOR'].max()-1
    myProjDf.loc[negVOR.index,'VOR']=negVOR['VOR']
    flexDf=myProjDf[(myProjDf['position']=='RB')|(myProjDf['position']=='WR')|(myProjDf['position']=='TE')]
    flexDf['flexRank']=flexDf['my_proj'].rank(ascending=False)
    repl=vorDic['flex']
    flexVor=flexDf.loc[flexDf['flexRank'].between(repl-1,repl+1),'my_proj'].mean()
    flexDf['flexVOR']=flexDf['my_proj']-flexVor
    negFlexVOR=flexDf.loc[flexDf['flexVOR']<0]
    negFlexVOR.loc[:,'flexVOR']=negFlexVOR['my_proj']-negFlexVOR['my_proj'].min()
    negFlexVOR.loc[:,'flexVOR']=negFlexVOR['flexVOR']-negFlexVOR['flexVOR'].max()-1
    flexDf.loc[negFlexVOR.index,'flexVOR']=negFlexVOR['flexVOR']
    myProjDf=myProjDf.merge(flexDf[['player','position','flexRank','flexVOR']],on=['player','position'],how='left')
    myProjDf['flexVOR'].fillna(myProjDf['VOR'],inplace=True)
    myProjDf.sort_values('VOR',ascending=False,inplace=True)
    myProjDf.to_excel('player_rankings_VOR.xlsx',index=False)
    return
