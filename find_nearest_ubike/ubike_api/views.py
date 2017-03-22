from math import sqrt
from django.http import JsonResponse
import requests


def get_user_location(lat, lng):
    google_geo_api = 'http://maps.google.com/maps/api/geocode/json?latlng={},{}&language=zh-TW&sensor=true'.format(
        lat, lng)
    data = requests.get(google_geo_api)
    try:
        address_components = data.json()['results'][0]['address_components']
        user_location = 'undefined'
        for comp in address_components:
            if comp['types'][0] == 'administrative_area_level_1':
                user_location = comp['long_name']
                break
            elif comp['types'][0] == 'administrative_area_level_2':
                user_location = comp['long_name']
                break
        return user_location
    except:
        return 'Not belong to any country'

def num2str(value):
    str_num = str(value)
    if len(str_num) <= 4:
        return '0' * (4 - len(str_num)) + str_num
    return str_num

def find_nearest_two_stop(lat, lng):
    """
    return two nearest stop with given lat and lng
    """

    # get data from data.taipei
    gz_data = requests.get('http://data.taipei/youbike')
    json_data = gz_data.json()

    # get all stop location
    ubike_locations = []
    for key, loc in json_data['retVal'].items():
        stop_info = dict(loc)
        ubike_locations.append({'lat': stop_info['lat'], 'lng': stop_info['lng'], 'stop_index': key})

    # calculate all the distance between user location and stops
    # [{ 'dist': 0.444, 'stop_index': 1 }, {...}]
    dist_map = []
    for num, loc in enumerate(ubike_locations):
        stop_lat = float(loc['lat'])
        stop_lng = float(loc['lng'])
        dist = sqrt((lat - stop_lat) ** 2 + (lng - stop_lng) ** 2)
        dist_map.append({'dist': dist, 'stop_index': loc['stop_index']})  # enumerate counts from 0

    # sorted by distance
    sorted_dist_map = sorted(dist_map, key=lambda x: x['dist'])

    results = []
    for stop in sorted_dist_map:
        stop_data = json_data['retVal'][stop['stop_index']]
        if len(results) < 2:
            if stop_data['act'] == '1': # station is avaliable
                result = {}
                result['station'] = stop_data['sna']
                result['num_ubike'] = int(stop_data['sbi'])
                result['total'] = stop_data['tot']
                results.append(result)
        else:
            break
    # the nearest two stop
    # nearest_two_stop = sorted_dist_map[0:2]
    # results = []
    # for stop in nearest_two_stop:
    #     print(json_data['retVal'][stop['stop_index']]['act'])
    #     result = {}
    #     result['station'] = json_data['retVal'][stop['stop_index']]['sna']
    #     result['num_ubike'] = json_data['retVal'][stop['stop_index']]['sbi']
    #     result['total'] = json_data['retVal'][stop['stop_index']]['tot']
    #     results.append(result)

    return results

def isProperCoordinate(lat, lng):
    if (lat < -90 or lat > 90) or (lng < -180 or lng > 180):
        return False
    else:
        return True


def server_response(request):
    """
    1: all ubike stations are full
    0: OK
    -1: invalid latitude or longitude
    -2: given location not in Taipei City
    -3: system error

    :param request:
    :return: JsonResponse
    """
    if request.method == 'GET':
        try:
            lat = float(request.GET.get('lat'))
            lng = float(request.GET.get('lng'))

            response = dict({'code': '', 'result': []})
            if isProperCoordinate(lat, lng) == False:
                response['code'] = -1

            elif get_user_location(lat, lng) != '台北市':
                response['code'] = -2

            else:
                results = find_nearest_two_stop(lat, lng)
                result_filter = []

                for result in results:
                    if int(result['num_ubike']) != int(result['total']):
                        result_filter.append({key: value for key, value in result.items() if key != 'total'})

                if len(result_filter) == 0:
                    response['code'] = 1 # no zoom to park
                else:
                    response['code'] = 0 # normal

                response['result'] = result_filter

            return JsonResponse(response)
        except:
            status_code = -3
            result = {}
            return JsonResponse({'code': status_code, 'result': result})
    else:
        return JsonResponse({'error': 'method not allowed'})

