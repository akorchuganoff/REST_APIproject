from requests import get,post,delete, patch
# print(patch('http://localhost:80/couriers/1', {'regions': [1, 2, 3]}).json())

print(post('http://localhost:80/orders/assign', {'courier_id': 1}).json())

# print(post('http://localhost:80/orders', json={
#   "data": [
#     {
#       "order_id": 1,
#       "weight": 0.23,
#       "region": 3,
#       "delivery_hours": '09:00-18:00'
#     }, {
#       "order_id": 2,
#       "weight": 0.23,
#       "region": 3,
#       "delivery_hours": '09:00-18:00'
#     }, {
#       "order_id": 3,
#       "weight": 0.23,
#       "region": 3,
#       "delivery_hours": '09:00-18:00'
#     }, {
#       "order_id": 4,
#       "weight": 0.23,
#       "region": 3,
#       "delivery_hours": '09:00-18:00'
#     }]
# }).json())
# {'assign_time': '2021-04-02 00:57:55.230456', 'order': [{'id': 3}, {'id': 4}, {'id': 5}]}


# print(post('http://localhost:80/couriers', json={
#   "data": [
#     {
#       "courier_id": 1,
#       "courier_type": "car",
#       "regions": [1, 2, 3],
#       "working_hours": ['09:00-18:00']
#     },
#     {
#       "courier_id": 2,
#       "courier_type": "bike",
#       "regions": [1, 2, 3],
#       "working_hours": ['09:00-18:00']
#     },
#     {
#       "courier_id": 3,
#       "courier_type": "foot",
#       "regions": [1, 2, 3],
#       "working_hours": ['09:00-18:00']
#     }
#
#   ]
# }).json())