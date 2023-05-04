import requests
import os
os.environ['ALL_PROXY']='http://127.0.0.1:7890'
# url = "https://api.openai.com/v1/chat/completions"
your_apikey = " "
# headers = {"Authorization": your_apikey,"Content-Type": "application/json"}
# json ={
#     "model": "gpt-3.5-turbo",
#     "messages": [{"role": "user", "content": "Hello!"}]
#   }
text="Since diffusion models (DM) and the more recent Poisson flow generative models (PFGM) are inspired by physical processes, it is reasonable to ask: Can physical processes offer additional new generative models? We show that the answer is yes. We introduce a general family, Generative Models from Physical Processes (GenPhys), where we translate partial differential equations (PDEs) describing physical processes to generative models. We show that generative models can be constructed from s-generative PDEs (s for smooth). GenPhys subsume the two existing generative models (DM and PFGM) and even give rise to new families of generative models, e.g., \"Yukawa Generative Models\" inspired from weak interactions. On the other hand, some physical processes by default do not belong to the GenPhys family, e.g., the wave equation and the Schrödinger equation, but could be made into the GenPhys family with some modifications. Our goal with GenPhys is to explore and expand the design space of generative models. "
api_url = "https://api.openai.com/v1/chat/completions"
headers = {"Authorization": f"Bearer {your_apikey}","Content-Type": "application/json"}
payload = {
"model": "gpt-3.5-turbo",
"messages": [{"role": "user", "content": f"Please summarize the following text:\n{text}"}]
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
