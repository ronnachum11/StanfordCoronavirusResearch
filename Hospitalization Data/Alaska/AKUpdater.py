import urllib.request

print('Beginning file download with urllib2...')

url = 'https://opendata.arcgis.com/datasets/797cbc3e398241a2b11e76fc06dd2b8b_0.csv'
urllib.request.urlretrieve(url, 'AKGovData.csv')