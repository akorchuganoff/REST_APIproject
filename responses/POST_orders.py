from requests import get,post,delete, patch
print(post('http://0.0.0.0:8080/orders', json={
  "data": [
    {
      "order_id": 1,
      "weight": 35,
      "region": 3,
      "delivery_hours": ['13:00-15:00']
    }, {
      "order_id": 2,
      "weight": 35,
      "region": 3,
      "delivery_hours": ['09:00-10:00']
    }, {
      "order_id": 3,
      "weight": 35,
      "region": 3,
      "delivery_hours": ['14:00-14:30']
    }, {
      "order_id": 4,
      "weight": 35,
      "region": 3,
      "delivery_hours": ['13:30-14:30']
    },
{
      "order_id": 5,
      "weight": 5,
      "region": 3,
      "delivery_hours": ['15:00-17:00']
    },
           {
      "order_id": 6,
      "weight": 5,
      "region": 3,
      "delivery_hours": ['17:00-18:00']
    }, {
      "order_id": 7,
      "weight": 5,
      "region": 3,
      "delivery_hours": ['18:30-19:30']
    }, {
      "order_id": 8,
      "weight": 5,
      "region": 3,
      "delivery_hours": ['17:00-19:00']
    },
      {
      "order_id": 9,
      "weight": 5,
      "region": 3,
      "delivery_hours": ['19:10-19:20']
    },
           {
      "order_id": 10,
      "weight": 5,
      "region": 3,
      "delivery_hours": ['12:30-13:30']
    }, {
      "order_id": 11,
      "weight": 5,
      "region": 3,
      "delivery_hours": ['13:30-14:30']
    }, {
      "order_id": 12,
      "weight": 5,
      "region": 3,
      "delivery_hours": ['16:30-16:45']
    }
  ]
}).json())