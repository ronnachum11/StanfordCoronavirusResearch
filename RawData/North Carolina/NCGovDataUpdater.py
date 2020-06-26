import urllib.request

print('Beginning file download with urllib2...')

url = 'https://public.tableau.com/vizql/w/NCDHHS_COVID-19_DataDownload/v/DailyMetrics/vudcsv/sessions/F34560CB5FC346D2BE9FE47A3294AAD3-0:0/views/4771422506905449664_9024048749190726675?summary=true'
urllib.request.urlretrieve(url, 'NCGovData.csv')