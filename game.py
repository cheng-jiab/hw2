import urllib
import requests
import json
import csv
import pymysql

db = pymysql.connect('localhost','root','mysql9299','game')
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS company")
sql = '''
    CREATE TABLE company(
    guid VARCHAR(50) NOT NULL,
    name VARCHAR(50),
    date_founded DATE,
    deck VARCHAR(500),
    country VARCHAR(50),
    phone VARCHAR(50),
    website VARCHAR(100),
    location_id INT,
    location_name VARCHAR(50),
    site_detail_url VARCHAR(100),
    location_count INT    
    )
'''
cursor.execute(sql)






user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent':user_agent,}
###url = 'https://www.giantbomb.com/api/accessory/?api_key=75a93f4b071b6002e1f328293149fb3cd166b91a&format=json&limit=1'
url = 'http://www.giantbomb.com/api/companies/?api_key=75a93f4b071b6002e1f328293149fb3cd166b91a&format=json&limit=100'
###url = 'http://www.giantbomb.com/api/company/3010-1/?api_key=75a93f4b071b6002e1f328293149fb3cd166b91a&format=json'
#game #url = 'https://www.giantbomb.com/api/game/3030-66000/?api_key=75a93f4b071b6002e1f328293149fb3cd166b91a&format=json'
print(url)
req = urllib.request.Request(url=url, headers=headers)
json_obj = urllib.request.urlopen(req)
data = json.load(json_obj)
#print(json_obj.read())
#result = (data)['Results']
#print(data['results'])

#print(data['results'])
for i in data['results']:
#    row = i['guid']
    url_c = 'http://www.giantbomb.com/api/company/'+ str(i['guid'])+'/?api_key=75a93f4b071b6002e1f328293149fb3cd166b91a&format=json'
    req_c = urllib.request.Request(url=url_c, headers=headers)
    json_obj_c = urllib.request.urlopen(req_c)
    data_c = json.load(json_obj_c)
    res = data_c['results']
    try:
        for game in res['published_games'][1:5]:
            save = game['api_detail_url'],game['name'],res['guid'],res['name']
            print(save)
            with open('game.csv', 'a')as r:
                r_csv = csv.writer(r)
                r_csv.writerow(save)
        for location in res['locations']:
    #        row = [res['guid'],res['name'],res['date_founded'],res['deck'],res['location_country'],res['phone'],res['website'],
    #               location['id'],location['name'],location['site_detail_url'],location['count']]
            sql = '''
            INSERT INTO company(
            guid, name, date_founded, deck, country, phone, website, location_id, location_name, site_detail_url, location_count   
            )
            VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')'''\
                  % (res['guid'], res['name'], res['date_founded'], res['deck'], res['location_country'], res['phone'],res['website'],
                   location['id'], location['name'], location['site_detail_url'], location['count'])


            cursor.execute(sql)
            db.commit()

            row = [res['guid'], res['name'], res['date_founded'], res['deck'], res['location_country'], res['phone'],
                   res['website'],
                   location['id'], location['name'], location['site_detail_url'], location['count']]
            print(row)
    except:
        print('error')

    #    with open('company.csv', 'a')as r:
    #        r_csv = csv.writer(r)
    #        r_csv.writerow(row)
    #    with open('company.csv', 'a')as r:
    #        r_csv = csv.writer(r)
    #        r_csv.writerow(row)


db.close()

db = pymysql.connect('localhost','root','mysql9299','game')
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS gamelist")
sql = '''
    CREATE TABLE gamelist(
    guid VARCHAR(50) NOT NULL,
    name VARCHAR(50),
    original_release_date DATE,
    com_guid VARCHAR(50),
    publisher VARCHAR(100),
    genres_name VARCHAR(50),
    genres_id VARCHAR(10),
    genres_url VARCHAR(50),
    platform_name VARCHAR(50),
    platform_id VARCHAR(50),
    platform_url VARCHAR(50)     
    )
'''

cursor.execute(sql)



with open('game.csv')as game:
    game_csv = csv.reader(game)
    for rec in game_csv:
        url = rec[0] + '?api_key=75a93f4b071b6002e1f328293149fb3cd166b91a&format=json'
        print(url)

        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent':user_agent,}
        ###url = 'https://www.giantbomb.com/api/accessory/?api_key=75a93f4b071b6002e1f328293149fb3cd166b91a&format=json&limit=1'
        #url = 'http://www.giantbomb.com/api/companies/?api_key=75a93f4b071b6002e1f328293149fb3cd166b91a&format=json&limit=100'
        ###url = 'http://www.giantbomb.com/api/company/3010-1/?api_key=75a93f4b071b6002e1f328293149fb3cd166b91a&format=json'
        ######url = 'https://www.giantbomb.com/api/game/3030-66000/?api_key=75a93f4b071b6002e1f328293149fb3cd166b91a&format=json'
        #url = 'https://www.giantbomb.com/api/games/?api_key=75a93f4b071b6002e1f328293149fb3cd166b91a&sort="original_game_rating"&limit=10&format=json'
        #url = 'https://www.giantbomb.com/api/user_reviews/?api_key=75a93f4b071b6002e1f328293149fb3cd166b91a&limit=10&format=json'
        #url = 'https://www.giantbomb.com/api/genre/3060-43/?api_key=75a93f4b071b6002e1f328293149fb3cd166b91a&format=json'

        print(url)
        req = urllib.request.Request(url=url, headers=headers)
        json_obj = urllib.request.urlopen(req)
        data = json.load(json_obj)
        #print(json_obj.read())
        #result = (data)['Results']
        g = data['results']


        #print(data['results'])
        try:
            for i in g['platforms']:
            #    row = g['publishers'][0]['name']
                row = (g['guid'],g['name'],g['original_release_date'],g['publishers'][0]['name'],g['genres'][0]['name'],g['genres'][0]['id'],g['genres'][0]['api_detail_url'],
               i['name'],i['id'],i['api_detail_url'])
                print(row)
                sql = '''
                        INSERT INTO gamelist(
                        guid, name, original_release_date, com_guid, publisher, genres_name, genres_id, 
                        genres_url, platform_name, platform_id , platform_url    
                        )
                        VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')'''\
                              % (g['guid'],g['name'],g['original_release_date'],rec[2],g['publishers'][0]['name'],g['genres'][0]['name'],g['genres'][0]['id'],g['genres'][0]['api_detail_url'],
                    i['name'],i['id'],i['api_detail_url'])


                cursor.execute(sql)
                db.commit()
        except:
            print("error")

db.close()