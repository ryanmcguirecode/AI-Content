import openai
import urllib.request
from credentials.open_ai import API_KEY
from generate_prompt import Prompt, get_art_style

openai.api_key = API_KEY

def generate(text: str, our_prompt : Prompt, filepath: str):
    """ Generate DALL-E image based on prompt, save to filepath """
    
    response = openai.Image.create(
        prompt="{0} in the {1}. {2} in {3} style.".format(our_prompt.story_subject, our_prompt.story_setting, text, get_art_style()),
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    urllib.request.urlretrieve(image_url, filepath)