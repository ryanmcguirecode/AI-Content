from moviepy.editor import *
from moviepy.config import change_settings
from moviepy.video.tools.subtitles import SubtitlesClip

# change_settings({"IMAGEMAGICK_BINARY": "/Users/dylanmcguire/Desktop/AI Social Media/movie/ImageMagick-7.0.10/bin/convert"})

# Load a video file

images = []
for image in os.listdir('images'):
    if not 'DS_Store' in image:
        images.append('images/' + image)
# print(TextClip.list('font'))
video = ImageSequenceClip(images, fps=.3)

# Load an audio file
audio = AudioFileClip('music/minecraft_w_fire.m4a').subclip(0,15)
audio2 = AudioFileClip('music/minecraft_w_fire.m4a').subclip(15,35)
audio = CompositeAudioClip([audio, audio2])

# Replace the audio of the video with the audio loaded above
clip = video.set_audio(audio)

#write subtitles to video
# for i in range(new_video.duration * 2):
words = ['house', 'mouse', 'douse', 'spouse', 'clause']
text = 'Once upon a time in a jungle green, There lived a troop of monkeys, so serene. They swung from vine to vine, And had a great time, Living in harmony, as if in a dream.'
text= text.split(" ")
num_words = 4
text = [" ".join(text[i:i+ num_words]) for i in range(0, len(text), num_words)]
start = 0
word_length = 4
text_clips = []
for i in range(len(text)):
    text_clips.append(TextClip(text[i], fontsize=40, color='green').set_duration(word_length).set_position('bottom', 'center'))
    start += word_length
clips = concatenate_videoclips(text_clips)
# generator = TextClip(text, font='Systemskrift-Condensed-Ultralight-G1', fontsize=40, color='green', method='pango',size=[1000,None]).set_duration(13)
#.set_position(lambda t: (-100*t, 980))
subs = [((0, 1), 'm&m'),
        ((1, 4), 'gus')]
# subtitles = SubtitlesClip(subs, generator)

clip = CompositeVideoClip([clip, clips])

# Save the modified video to a file
clip.write_videofile('modified_video.mp4', codec='libx264', audio_codec='aac', fps=30)

