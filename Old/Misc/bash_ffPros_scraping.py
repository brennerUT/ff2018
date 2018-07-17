from subprocess import check_output

years=['2016','2017']
expCodeDic={'seanKoerner':'120','numberFire':'73'}
for year in years:
    for exp in expCodeDic.keys():
        if year=='2017' and exp=='numberFire':
            continue
        for pos in ['qb','rb','wr','te','dst']:
            command="""curl 'https://www.fantasypros.com/nfl/projections/"""+pos+""".php?week=draft&year="""+year+"""&filters="""+expCodeDic[exp]+':'+expCodeDic[exp]+"""' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: __qca=P0-191665562-1499352868149; fp_lb=1; fp_hp=1; _vwo_uuid_v2=754FDE2186753FC169F66CEFF54E0886|693aa93639395859e3e1e47ed8bf61b9; is5vHOtZn65zpLqA=7xc280zakwx503wh27xunaoptd3flz5w; fp_user="YmNkYTIzNTjB8hW/PD7mqHQYaxkim5Cx88Xahrzm3fopOt6klX5yLcx4i3CCv6yrf8VofToFLL/C\012roM0H9/RWjybvMNc5md+o7FHhOOUM+Yw5swYQj83azIfHTiS+kYNjp1d6mdOOJVOkjOMcPs547dc\012mh2HjLA8FlC0oLC87n7v6WbT5A3hxNLv9EzsmBX3xkDJSqcgwvw8ZNVxRcbrhVnfrmkopsKD75Se\012yazrR1gCXSScvOXdSyrhBa4LxMv1QTyNuh5F6L6CO8subovVsYoQbSZ7WkRTyAgiBRcWh9apxy88\012SF0HbzEbOno9uB8Z8ZUnGZTDZ2r0pTx5uWNFFVoAjxxRyj5Y\012"; __zlcmid=hNgZh4oxVfcLtY; _ga=GA1.2.867728428.1499352867; _gid=GA1.2.745793604.1500077161; cookies_enabled=1' -H 'Connection: keep-alive' --compressed -o """+exp+'_'+pos+'_'+year+'.html'

            print(command)
        
            check_output(command,shell=True)

            break
        break
    break
