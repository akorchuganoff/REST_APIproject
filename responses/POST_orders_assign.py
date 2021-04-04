from requests import get,post,delete, patch
print(post('http://0.0.0.0:8080/orders/assign', {'courier_id': 1}).json())