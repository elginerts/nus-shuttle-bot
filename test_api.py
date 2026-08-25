import requests
url = "https://fms.connectx.com.sg/apiy/NUSETA/ShuttleService"

parameters={"busstopname": "BIZ2"}

response = requests.get(url, params=parameters)
data = response.json()

print(response.url)
print(response.status_code)
print(data)