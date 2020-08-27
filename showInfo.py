import openpyxl

wb = openpyxl.load_workbook('gps.xlsx')
ws = wb['Sheet1']

gps = [0]*100

for i in range(4):
	gps[i] = ws.cell((i+1), 2).value
#	print(gps[i])

import requests as r
import json
http_header = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'x-requested-with': 'XMLHttpRequest'}

session = r.Session()
session.headers.update(http_header)
start = '126.7462481,37.3492939'
end = '126.9913250,37.4221762'

search_distance_url_base = 'https://m.map.naver.com/spirra/findCarRoute.nhn?route=route3&output=json&result=web3&coord_type=latlng&search=2&car=0&mileage=12.4'

def SEARCH_DISTANCE_URL(start_point, end_point):
    return search_distance_url_base+'&start={}&destination={}'.format(start_point, end_point)


def GET_INFO(start, end):
			start_point = gps[0]
			end_point = gps[1]

			res = session.get(SEARCH_DISTANCE_URL(start_point, end_point)).text
			res_dict = json.loads(res)
			import pprint
			import sys
			sys.stdout = open('output.txt','w')
			pprint.pprint(res_dict)
			target = res_dict['routes'][0]['summary']
			distance = target['distance']
			sec = target['duration']

			print('출발지: {}, 도착지: {}'.format(gps[0], gps[1]))
			print('추천경로 이동 거리: {}km'.format(distance / 1000))
			print('예상 소요시간: {}분'.format(sec / 60))

GET_INFO(start, end)