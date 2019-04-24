import urllib, urllib2

BASE_URL = 'https://api.thingspeak.com/update.json'
WRITE_KEY = 'KZ34WHKW50OY83HS'

def send_hcho(hcho):
    data = urllib.urlencode({'api_key' : WRITE_KEY, 'field1' : hcho})
    response = urllib2.urlopen(url=BASE_URL, data=data)
    print response.read()