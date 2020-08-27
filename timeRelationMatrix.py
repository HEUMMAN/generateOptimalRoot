import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import pprint
from sklearn.cluster import KMeans
import folium

data = pd.read_excel(file_path)
address_list = data['주소지'].tolist()
print(address_list)

locations_lat = [];
locations_lng = [];

for addr in address_list:
    URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyBP5766yBfJirdZXwkm05u5_NcWFAoGa-k' \
          '&sensor=false&language=ko&address={}'.format(addr)
    response = requests.get(URL)
    dj = response.json()
    lat = dj['results'][0]['geometry']['location']['lat']
    lng = dj['results'][0]['geometry']['location']['lng']
    locations_lat.append(lat)
    locations_lng.append(lng)

ser_lat = pd.Series(locations_lat)
ser_lng = pd.Series(locations_lng)
frame = { 'lat': ser_lat, 'lng': ser_lng }
result = pd.DataFrame(frame)

wcss = []
for i in range(1, 15):
  model = KMeans(n_clusters=i)
  model.fit(result[['lat', 'lng']])
  wcss.append(model.inertia_)

#== USE DISPLAY ONLY ==
#plt.figure(figsize=(12,6))
#plt.plot(range(1, 15), wcss)
#plt.title('The Elbow Method')
#plt.xticks(range(1,15))
#plt.xlabel('Clusters')
#plt.ylabel('wcss')
#plt.show()

model = KMeans(n_clusters=12)
model.fit(result[['lat', 'lng']])
result['Cluster'] = model.predict(result[['lat', 'lng']])

df12 = result[result.Cluster==0]
print(df12)
print(df12['lat'])

df12.groupby(['Cluster'], as_index=False).mean()
clus_result = result.groupby(['Cluster'], as_index=False).mean()
mean_result = clus_result.mean()
mean_loc = [mean_result.lat,mean_result.lng]

loc_result = clus_result[['lat','lng']]

clus_list = loc_result.values.tolist()

#== USE DISPLAY ONLY ==
#map = folium.Map(location=mean_loc, zoom_start=8,tiles='Stamen Terrain')
#for i in range(12):
#    folium.Marker(clus_list[i]).add_to(map)
#map

#temp_list = result.values.tolist()
#map1 = folium.Map(location=mean_loc, zoom_start=8,tiles='Stamen Terrain')
#for i in range(100):
#    folium.Marker(temp_list[i]).add_to(map1)
#map1

###===============================================
import json
import requests as r

http_header = {
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'x-requested-with': 'XMLHttpRequest'
}
session = r.Session()
session.headers.update(http_header)
search_distance_url_base = 'https://m.map.naver.com/spirra/findCarRoute.nhn?route=route3&output=json&result=web3&coord_type=latlng&search=2&car=0&mileage=12.4'

def SEARCH_DISTANCE_URL(start_point, end_point):
    return search_distance_url_base+'&start={}&destination={}'.format(start_point, end_point)
def SEARCH_POINT_URL(q):
    return 'https://m.map.naver.com/apis/search/poi?query={}&page=1'.format(q)
def GET_END_POINT(loc_list):
    x = loc_list[0]
    y = loc_list[1]
    return '{},{},1'.format(y, x)
def GET_INFO(start, end):
    res = session.get(SEARCH_DISTANCE_URL(GET_END_POINT(start),GET_END_POINT(end))).text
    res_dict = json.loads(res)
    target = res_dict['routes'][0]['summary']
    sec = target['duration']
    return sec

def relational_time_matrix(clusted_list):
    last_matrix = []
    for i in range(len(clus_list)):
        temp = []
        for j in range(len(clus_list)):
            if i is j:
                temp.append(0)
            elif(i > j):
                temp.append(last_matrix[j][i])
            else:
                temp.append(GET_INFO(clusted_list[i], clusted_list[j]))
        last_matrix.append(temp)
    return last_matrix

time_mat = relational_time_matrix(clus_list)

np_time = np.array(time_mat)

down_arr = np.asarray(np_time)
np.savetxt("time_relation.csv", down_arr, fmt='%4d', delimiter=",")