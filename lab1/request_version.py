import requests

print(requests.__version__)
response = requests.get('http://www.google.com/')