from ContentGenerator import ContentGenerator
from ContentParameters import ContentParameters
from Music import Music
from random import choice
import generate_video
from youtube_upload import upload_video
from generate_prompt import get_content
import os


prompt = get_content()
content_identifier = "generated-image-slideshow" 
music = Music(os.path.abspath('./content_resources/motivating_uplifting.mp3'), 'motivating_uplifting', 2)

content_parameters = ContentParameters(prompt.story_subject, content_identifier)
fable_content = ContentGenerator(prompt, content_parameters, music)
upload_video('dylan_mcg', os.path.join(fable_content.destination, 'final_video.mp4'), "{0} in tha {1}?! \u1F92F \u1F92F".format(prompt.story_subject, prompt.story_setting),
 "#storytelling", "24", "", "public")