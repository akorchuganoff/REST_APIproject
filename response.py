from requests import get,post,delete, patch

print(post('http://localhost:80/couriers', json={
  "data": [
    {
      "courier_id": 1,
      "courier_type": "car",
      "regions": [1, 2, 3],
      "working_hours": ['09:00-18:00']
    },
    {
      "courier_id": 2,
      "courier_type": "bike",
      "regions": [1, 2, 3],
      "working_hours": ['09:00-18:00']
    },
    {
      "courier_id": 3,
      "courier_type": "foot",
      "regions": [1, 2, 3],
      "working_hours": ['09:00-18:00']
    }
  ]
}).json())