from ContentGenerator import ContentGenerator
from ContentGeneratorTest import ContentGeneratorTest
from ContentParameters import ContentParameters
from Music import Music

from random import choice


topics = ['celebrities', 'space', 'philosophy', 'photography', 'health', 'relationships', 
          'family', 'movies', 'business', 'politics', 'books', 'computers', 'fitness', 'food', 
          'home', 'robots', 'art', 'beauty', 'cowboys', 'science', 'fashion', 'aliens', 'pets', 
          'weather', 'nature', 'religion', 'travel', 'society', 'education', 'technology', 
          'music',  'places', 'cars', 'money', 'style', 'history', 'hobbies', 'sports', 
          'world news', 'writing', 'work', 'people']
topic = choice(topics)

prompt = "Write a short fable about " + topic + " under 200 words"
name = topic
content_identifier = "generated-image-slideshow" 
music = Music('/Users/ryanmcguire/Desktop/AI_Content/content_resources/motivating_uplifting.mp3', 'motivating_uplifting', 0)

content_parameters = ContentParameters(prompt, name, content_identifier)
fable_content = ContentGenerator(content_parameters, music)