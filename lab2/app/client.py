import requests

url = 'http://localhost:8000/checkcrime'
params = {'lat':'37.334164', 'lon':'-121.884301', 'radius':'0.02'}
r = requests.get(url=url, params=params)
print r.text