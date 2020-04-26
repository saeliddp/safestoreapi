import requests, json 

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
        stores.append([y[i]['name'],y[i]['formatted_address']])
    #print(stores)
    return stores