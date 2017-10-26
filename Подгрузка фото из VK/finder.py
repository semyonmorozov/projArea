# -*- coding: cp1251 -*-
import http.client
import urllib.request, urllib.parse, urllib.error
import json
import datetime
import time
import httplib2
import os

def get_vk(latitude, longitude, distance, min_timestamp, max_timestamp):
    get_request =  '/method/photos.search?lat=' + location_latitude
    get_request+= '&long=' + location_longitude
    get_request+= '&count1000'
    get_request+= '&radius=' + distance
    get_request+= '&start_time=' + str(min_timestamp)
    get_request+= '&end_time=' + str(max_timestamp)
    get_request+= '&sort=0'
    local_connect = http.client.HTTPSConnection('api.vk.com', 443)
    local_connect.request('GET', get_request)
    return local_connect.getresponse().read()

def timestamptodate(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')+' UTC'

def parse_vk(location_latitude, location_longitude, distance, min_timestamp, max_timestamp, date_increment):
    print('Starting parse vkontakte..')
    print('GEO:',location_latitude,location_longitude)
    print('TIME: from',timestamptodate(min_timestamp),'to',timestamptodate(max_timestamp))
    resultdir =datetime.datetime.strftime(datetime.datetime.now(), "y%Ym%md%d h%Hm%Ms%S")
    os.makedirs(resultdir)
    file_inst = open('vk_'+location_latitude+location_longitude+'.html','w')
    file_inst.write('<html>')
    local_min_timestamp = min_timestamp
    while (1):
        if ( local_min_timestamp >= max_timestamp ):
            break
        local_max_timestamp = local_min_timestamp + date_increment
        if ( local_max_timestamp > max_timestamp ):
            local_max_timestamp = max_timestamp
        print(timestamptodate(local_min_timestamp),'-',timestamptodate(local_max_timestamp))
        vk_json = json.loads(get_vk(location_latitude, location_longitude, distance, local_min_timestamp, local_max_timestamp))
        for local_i in vk_json['response']:
            if type(local_i) is int:
                continue
            h = httplib2.Http('.cache')            
            response, content = h.request(local_i['src_big'])
            out = open(resultdir+'/user'+str(local_i['owner_id'])+'date'+str(local_i['created'])+'.jpg', 'wb')
            out.write(content)
            out.close()
            file_inst.write('<br>')
            file_inst.write('<img src='+local_i['src_big']+'><br>')
            file_inst.write(timestamptodate(int(local_i['created']))+'<br>')
            file_inst.write('http://vk.com/id'+str(local_i['owner_id'])+'<br>')
            file_inst.write('<br>')
        local_min_timestamp = local_max_timestamp
    file_inst.write('</html>')
    file_inst.close()

location_latitude = '57.777518'
location_longitude = '60.008434'
distance = '500'
min_timestamp = time.mktime(time.strptime('2017-10-23 21:00:00', '%Y-%m-%d %H:%M:%S'))
max_timestamp = time.mktime(time.strptime('2017-10-23 21:40:00', '%Y-%m-%d %H:%M:%S'))
date_increment = 60*60*2 


parse_vk(location_latitude, location_longitude, distance, min_timestamp, max_timestamp, date_increment)






    
