from requests import get,post,delete, patch
print(patch('http://127.0.0.1:8080/couriers/1', {"working_hours": ['09:00-12:00']}).json())