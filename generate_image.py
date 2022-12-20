import openai
import urllib.request
from credentials.open_ai import API_KEY

openai.api_key = API_KEY

def generate(text: str, filepath: str):
    response = openai.Image.create(
        prompt=text,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    urllib.request.urlretrieve(image_url, filepath)