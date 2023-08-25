import requests

response = requests.post(
    "http://127.0.0.1:5000/adv/",
    json={
        "title": "Ugly cat for sale",
        "description": "cheap little annoying bastard for sale",
        "owner": "Doggo",
    },
)

print(response.json())
