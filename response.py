from requests import get,post,delete, patch
# print(patch('http://localhost:80/couriers/1', {'regions': [1, 2, 3]}).json())

print(post('http://localhost:80/orders/assign', {'courier_id': 4}).json())

# print(post('http://localhost:80/orders', json={
#   "data": [
#     {
#       "order_id": 5,
#       "weight": 0.23,
#       "region": 3,
#       "delivery_hours": '09:00-18:00'
#     }, {
#       "order_id": 6,
#       "weight": 0.23,
#       "region": 3,
#       "delivery_hours": '09:00-18:00'
#     }, {
#       "order_id": 7,
#       "weight": 0.23,
#       "region": 3,
#       "delivery_hours": '09:00-18:00'
#     }, {
#       "order_id": 8,
#       "weight": 0.23,
#       "region": 3,
#       "delivery_hours": '09:00-18:00'
#     }]
# }).json())
# {'assign_time': '2021-04-02 00:57:55.230456', 'order': [{'id': 3}, {'id': 4}, {'id': 5}]}


# print(post('http://localhost:80/couriers', json={
#   "data": [
#     {
#       "courier_id": 4,
#       "courier_type": "car",
#       "regions": [1, 2, 3],
#       "working_hours": ['09:00-18:00']
#     },
#     {
#       "courier_id": 5,
#       "courier_type": "bike",
#       "regions": [1, 2, 3],
#       "working_hours": ['09:00-18:00']
#     },
#     {
#       "courier_id": 6,
#       "courier_type": "foot",
#       "regions": [1, 2, 3],
#       "working_hours": ['09:00-18:00']
#     }
#
#   ]
# }).json())