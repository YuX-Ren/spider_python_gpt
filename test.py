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

language_code = 'en'
search_query = 'solar system'
number_of_results = 1
headers = {
  # 'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
  'User-Agent': 'YOUR_APP_NAME (YOUR_EMAIL_OR_CONTACT_PAGE)'
}

base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
endpoint = '/search/page'
url = base_url + language_code + endpoint
parameters = {'q': search_query, 'limit': number_of_results}
response = requests.get(url, headers=headers, params=parameters)
Json = json.loads(response.content)
print(Json)