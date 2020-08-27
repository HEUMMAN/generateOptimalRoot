import requests
import urllib.request as req
from bs4 import BeautifulSoup
#URL = "https://m.map.naver.com/spirra/findCarRoute.nhn?route=route3&output=json&result=web3&coord_type=latlng&search=2&car=0&mileage=12.4&start=126.7462481,37.3492939&destination=126.9913250,37.4221762"
URL = "https://m.map.naver.com/spirra/findCarRoute.nhn?route=route3&output=json&result=web3&coord_type=latlng&search=2&car=0&mileage=12.4&start=126.7462481,37.3492939&destination=126.7620500,37.3493154"

res = requests.get(URL)

open_url = req.urlopen(URL)

soup = BeautifulSoup(res.content, 'html.parser')

path = open_url.read().decode("utf-8")

print(path)