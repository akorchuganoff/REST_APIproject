from requests import get,post,delete, patch
print(patch('http://0.0.0.0:8080/couriers/1', {"regions": [2, 5, 6]}).json())