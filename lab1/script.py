import requests

print(requests.__version__)
response = requests.get('http://www.google.com/')
github = requests.get('https://raw.githubusercontent.com/houstonle/CMPUT404-Labs/main/script.py')
print(github.text)
