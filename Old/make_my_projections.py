import os
os.chdir('C:/Users/ericb/Desktop/FF_machine_learning')
import brennerFF as ff

ff.beersheets_2017(day='23',df=df)

# download FFAnalytics stuff; for FFA_weighted, exclude WalterFootball
ff.add_espn(2017)
ff.add_fantasyData(years_ago=0,year=2017)
ff.add_FFToday(2017)
ff.add_cbs(2017)
ff.add_scout(2017)
ff.add_numberfire_2017()
ff.add_FFAnalytics(2017,'ffAnalytics_weighted')
ff.add_FFAnalytics(2017,'nfl')
ff.add_FFAnalytics(2017,'yahoo')
ff.add_FFAnalytics(2017,'fantasySharks')
#check file
ff.cleanup(2017)

ff.machine_learning('2016_actual_and_proj.csv','2017_projections.csv')
ff.calc_VORs()
