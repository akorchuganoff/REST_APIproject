from requests import get,post,delete, patch
print(get('http://0.0.0.0:8080/couriers/1').json())