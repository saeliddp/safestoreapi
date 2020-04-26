import requests, json 

def ll2zip(lat,lon):
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + lat + "," + lon + "&key=AIzaSyABrTMzLrfMRYvTI33fQT9OkcKqNY7OSKo"
    r = requests.get(url)
    x = r.json() 
    y = x['results']
    first = y[0]    
    ac = first['address_components']
    for i in ac:
        if "['postal_code']" in str(i):
            pc = i
    zip = pc['short_name']
    return zip 

def get_stores_by_zip(zip):
    api_key = 'AIzaSyABrTMzLrfMRYvTI33fQT9OkcKqNY7OSKo'
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    query = 'grocery store ' + zip
    r = requests.get(url + 'query=' + query +'&key=' + api_key) 
    x = r.json() 
    y = x['results']
    stores = []
    for i in range(len(y)): 
        #print(y[i]['name'])
        #print(y[i]['formatted_address'])
        stores.append([y[i]['name'],y[i]['formatted_address'],y[i]['geometry']['location']['lat'],y[i]['geometry']['location']['lng']])
    #print(stores)
    return stores