from requests import get,post,delete, patch
print(post('http://localhost:80/orders', json={
  "data": [
    {
      "order_id": 3,
      "weight": 0.23,
      "region": 2,
      "delivery_hours": '09:00-18:00'
    },
    {
      "order_id": 4,
      "weight": 0.23,
      "region": 1,
      "delivery_hours": '09:00-18:00'
    },
{
      "order_id": 1,
      "weight": 0.23,
      "region": 2,
      "delivery_hours": '09:00-18:00'
    },
    {
      "order_id": 5,
      "weight": 0.23,
      "region": 1,
      "delivery_hours": '09:00-18:00'
    }
  ]
}).json())