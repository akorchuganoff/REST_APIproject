from requests import get,post,delete, patch
print(get('http://130.193.55.13:8080/couriers/1').json())
# {'courier_id': 1,
#  'courier_type': 'car',
#  'earnings': 9000,
#  'rating': '15.3197274083333',
#  'regions': [1, 2, 3],
#  'working_hours': ['09:00-12:00', '14:00-16:00', '17:00-19:00']}