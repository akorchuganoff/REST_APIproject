from requests import get,post,delete, patch
print(get('http://localhost:80/couriers/1').json())