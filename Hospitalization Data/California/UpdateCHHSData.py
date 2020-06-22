import urllib.request

print('Beginning file download with urllib2...')

url = 'https://data.chhs.ca.gov/dataset/6882c390-b2d7-4b9a-aefa-2068cee63e47/resource/6cd8d424-dfaa-4bdd-9410-a3d656e1176e/download/covid19data.csv'
urllib.request.urlretrieve(url, 'CHHSData.csv')
