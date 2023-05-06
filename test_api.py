import requests
import os
os.environ['ALL_PROXY']='http://127.0.0.1:7890'
# url = "https://api.openai.com/v1/chat/completions"
your_apikey = ""
# headers = {"Authorization": your_apikey,"Content-Type": "application/json"}
# json ={
#     "model": "gpt-3.5-turbo",
#     "messages": [{"role": "user", "content": "Hello!"}]
#   }
text="Hi"
api_url = "https://api.openai.com/v1/chat/completions"
headers = {"Authorization": f"Bearer {your_apikey}","Content-Type": "application/json"}
payload = {
"model": "gpt-3.5-turbo",
"messages": [{"role": "user", "content": text}]
}
response = requests.post(api_url, json=payload,headers=headers)

# response = requests.get(url, headers=headers)
# response = requests.post(url, headers=headers,json=json)


# api_url = "https://en.wikipedia.org/w/api.php"
# params = {
#     "action": "query",
#     "format": "json",
#     "prop": "extracts",
#     "pageids": pageid,
#     "explaintext": 1,
#     "exsectionformat": "wiki",
#     "utf8": 1,
#     "formatversion": 2
# }
# response = requests.get(api_url, params=params)

# if response.status_code == 200:
#     data = response.json()
#     if "extract" in data["query"]["pages"][0]:
#         print(data["query"]["pages"][0]["extract"])
print(response.status_code)
print(response.text)
