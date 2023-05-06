import requests
import os
from PIL import Image
import io
import json
os.environ['ALL_PROXY']='http://127.0.0.1:7890'

# # url = 'https://api.worldnewsapi.com/search-news?source-countries=de&entities=LOC:Italy'
# url = 'https://en.wikipedia.org/w/api.php?origin=*&action=opensearch&search=Ryuichi Sakamoto'
# data = requests.get(url).content
# print(data)
# # image = Image.open(io.BytesIO(image_data))
# # image.show()


# Python 3
# Choose your language, and search for articles.

user_message = "wiki"
api_url = "https://en.wikipedia.org/w/api.php"
params = {
    "action": "query",
    "format": "json",
    "list": "search",
    "utf8": 1,
    "formatversion": 2,
    "srsearch": user_message,
    "srlimit": 10,
    "srprop": "snippet"
}
response = requests.get(api_url, params=params)
print(response.text)