from ContentGenerator import ContentGenerator
from ContentParameters import ContentParameters
from Music import Music
from random import choice
import generate_video
from youtube_upload import upload_video
from generate_prompt import get_content
import os


topics = ['celebrities', 'space', 'philosophy', 'photography', 'health', 'relationships', 
          'family', 'movies', 'business', 'politics', 'books', 'computers', 'fitness', 'food', 
          'home', 'robots', 'art', 'beauty', 'cowboys', 'science', 'fashion', 'aliens', 'pets', 
          'weather', 'nature', 'religion', 'travel', 'society', 'education', 'technology', 
          'music',  'places', 'cars', 'money', 'styxle', 'history', 'hobbies', 'sports', 
          'world news', 'writing', 'work', 'people']
topic = choice(topics)

prompt = get_content()
content_identifier = "generated-image-slideshow" 
music = Music(os.path.abspath('./content_resources/motivating_uplifting.mp3'), 'motivating_uplifting', 0)

content_parameters = ContentParameters(prompt.story_subject, content_identifier)
fable_content = ContentGenerator(prompt, content_parameters, music)
upload_video(fable_content.destination, "{0} in tha {1}?! \u1F92F \u1F92F".format(prompt.story_subject, prompt.story_setting),
 "#storytelling", "kids", "", "public")