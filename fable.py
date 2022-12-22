from ContentGenerator import ContentGenerator, ContentGeneratorTest
import generate_video

from random import choice


topics = ['celebrities', 'space', 'philosophy', 'photography', 'health', 'relationships', 
          'family', 'movies', 'business', 'politics', 'books', 'computers', 'fitness', 'food', 
          'home', 'robots', 'art', 'beauty', 'cowboys', 'science', 'fashion', 'aliens', 'pets', 
          'weather', 'nature', 'religion', 'travel', 'society', 'education', 'technology', 
          'music',  'places', 'cars', 'money', 'style', 'history', 'hobbies', 'sports', 
          'world news', 'writing', 'work', 'people']
topic = choice(topics)

fable_content = ContentGenerator("Write a short fable about " + topic, "fable_" + topic)
generate_video.generate(fable_content, '/Users/ryanmcguire/Desktop/AI_Content/content_resources/motivating_uplifting.mp3')