import requests
import os
os.environ['ALL_PROXY']='http://127.0.0.1:7890'
url = "https://api.openai.com/v1/chat/completions"
your_apikey = " "
headers = {"Authorization": your_apikey,"Content-Type": "application/json"}
json ={
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }
# response = requests.get(url, headers=headers)
response = requests.post(url, headers=headers,json=json)

print(response.status_code)
print(response.text)
