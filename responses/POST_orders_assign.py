from requests import get,post,delete, patch
print(post('http://130.193.55.13:8080/orders/assign', {'courier_id': 1}).json())