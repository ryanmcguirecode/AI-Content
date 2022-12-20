import generate_voiceover
import generate_text
import generate_image

from random import choice
from traceback import print_exc, format_exc
from sys import exit
from datetime import datetime
import os


topics = ['celebrities', 'space', 'philosophy', 'photography', 'health', 'relationships', 
          'family', 'movies', 'business', 'politics', 'books', 'computers', 'fitness', 'food', 
          'home', 'robots', 'art', 'beauty', 'cowboys', 'science', 'fashion', 'aliens', 'pets', 
          'weather', 'nature', 'religion', 'travel', 'society', 'education', 'technology', 
          'music',  'places', 'cars', 'money', 'style', 'history', 'hobbies', 'sports', 
          'world news', 'writing', 'work', 'people']
topic = choice(topics)

print("Creating directory for files...")
try:
    directory = os.path.join("generated_content", "fable_" + topic + "_" +  datetime.now().strftime("%m%d%Y_%H%M"))
    os.mkdir(directory)
except:
    print("Error making directory:")
    print_exc()
    exit()

print("Generating fable about " + topic + "...")
try:
    filepath = os.path.join(directory, "generated_text.txt")
    text = generate_text.generate('write a short fable about ' + topic, filepath)
    print(text)
except:
    print("Error generating text:")
    print_exc()
    exit()

paragraphs = [par.strip() for par in text.split("\n") if par]

print("Generating images for each paragraph...")    
try:
    images_directory = os.path.join(directory, "images")
    os.mkdir(images_directory)
    for i, paragraph in enumerate(paragraphs):
        filepath = os.path.join(images_directory, "generated_image_" + str(i) + ".jpg")
        generate_image.generate(paragraph, filepath)
except:
    print("Error generating images:")
    print_exc()
    exit()

print("Generating voiceovers for each paragraph...")
try:
    voiceovers_directory = os.path.join(directory, "voiceovers")
    os.mkdir(voiceovers_directory)
    for i, paragraph in enumerate(paragraphs):
        filepath = os.path.join(voiceovers_directory, "generated_voiceover_" + str(i) + ".wav")
        generate_voiceover.generate(paragraph, filepath)
except:
    print("Error generating voiceovers:")
    print_exc()
    exit()
