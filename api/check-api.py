import requests

response = requests.get('http://localhost:8000/get_artist/3AUIYVmhwrsw8UOPHEv91Z')
print("GET Request Code of :")
print(response.status_code)
print("GET JSON of :")
print(response.json())  