import requests
import os
from PIL import Image
import io
proxies = {"https":"http://127.0.0.1:7890"}
url = "https://api.openai.com/v1/images/generations"
your_apikey = "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"
headers = {"Authorization": f"Bearer {your_apikey}","Content-Type": "application/json"}
image_desc ="A nice sunny day"
json ={
    "prompt": image_desc,
    "n": 1,
    "size": "256x256"
  }
response = requests.post(url, headers=headers,json=json,proxies=proxies)
print(response.status_code)
print(response.text)
if response.status_code == 200:
    # Loop through generated images and download them
    for index, image_url in enumerate(response.json()["data"]):
        print(image_url)
        image_data = requests.get(image_url["url"],proxies=proxies).content
        image = Image.open(io.BytesIO(image_data))
        image.show()
        image.save(f"{image_desc}_{index}.jpg")
    print("Images downloaded successfully!")
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")


