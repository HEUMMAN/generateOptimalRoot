import pprint
from itertools import chain

start_point = '{},{},1'.format(x, y)
end_point = '{},{},1'.format(x, y)

res = session.get(SEARCH_DISTANCE_URL(start_point, end_point)).text
res_dict = json.loads(res)

target = res_dict['routes'][0]['legs'][0]['steps']#[1]['path']
routes = [steps['path'] for steps in target]
#pprint.pprint(target)

routes = [x for x in routes if x]
temp_routes = [i.split(' ') for i in routes]

temp_routes = list(chain(*temp_routes))
temp_routes = [list(map(float,i.split(','))) for i in temp_routes]
result_path = [x[::-1] for x in temp_routes]

#==USE ONLY DISPLAY==
#import folium
#map2 = folium.Map(location=result_path[int(len(result_path)/2)], zoom_start=8,tiles='Stamen Terrain')
#folium.PolyLine(result_path, color="red", weight=4, opacity=1).add_to(map2)
#map2