import urllib.request

print('Beginning file download with urllib2...')

url = 'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/boro/boroughs-case-hosp-death.csv'
urllib.request.urlretrieve(url, 'NYCGovData.csv')