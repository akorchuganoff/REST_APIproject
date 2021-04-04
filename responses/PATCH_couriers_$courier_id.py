from requests import get,post,delete, patch
print(patch('http://130.193.55.13:8080/couriers/1', {"working_hours": ['09:00-14:00']}).json())
# {'courier_id': 1,
#  'courier_type': 'car',
#  'max_weight': 50.0,
#  'regions': [1, 2, 3],
#  'weight_of_food': 75.0,
#  'working_hours': '09:00-14:00'}