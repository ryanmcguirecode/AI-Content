import ContentGenerator
from constants import SUBTITLE_DIVISION

from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import json

def get_subtitle_groups(words: list[str]):
    subtitle_groups = [[]]
    punctuation_marker = False
    for word in words:
        if len(subtitle_groups[-1]) >= SUBTITLE_DIVISION or punctuation_marker:
            subtitle_groups.append([])
        subtitle_groups[-1].append(word)
        punctuation_marker= "." in word or "?" in word or "!" in word or "," in word
    return [" ".join(sg) for sg in subtitle_groups]

def generate(cg : ContentGenerator, music_filepath : str):
    
    images = list(filter(lambda f: '.jpg' in f, os.listdir(cg.images_directory)))
    images.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
    
    voiceover_path = os.path.join(cg.destination, "generated_voiceover.wav")
    voiceover = AudioFileClip(voiceover_path)
    timestamp_path = os.path.join(cg.destination, "timestamps.json")
    with open(timestamp_path, "r") as f:
        timestamps = json.load(f)
    
    music = AudioFileClip(music_filepath).subclip(0, voiceover.duration).volumex(0.5)
    full_audio = CompositeAudioClip([voiceover, music])
    
    image_clips = []
    seen_words = 0
    prev_time = 0
    
    
    for i in range(len(images)):
        image_path = os.path.join(cg.images_directory, images[i])
        seen_words += cg.paragraph_lengths[i]
        image_duration = timestamps[str(seen_words)] - prev_time
        prev_time = timestamps[str(seen_words)]
        image_clip = ImageClip(image_path).set_duration(image_duration)
        image_clips.append(image_clip)
        
    text_clips = []
    words = cg.text.split()
    subtitle_groups = get_subtitle_groups(words)
    seen_words = 0
    prev_time = 0
    for sg in subtitle_groups:
        seen_words += len(sg.split())
        text_clip = TextClip(sg, font="content_resources/Fonts/Anton/Anton-Regular.ttf", 
                             method="caption", fontsize=75, color="white", 
                             stroke_color="black",stroke_width=4.5, size=(700, None)).set_duration(timestamps[str(seen_words)] - prev_time)
        prev_time = timestamps[str(seen_words)]
        text_clips.append(text_clip)

    full_image_video = concatenate_videoclips(image_clips).crop(x_center=540 , y_center=540,
                    width=607.5, height=1080).resize(newsize=(1080,1920))
    full_text_clips = concatenate_videoclips(text_clips).set_pos(("center", 1320))
    # TODO: Make video 1080x1920 pixels
    final_video = CompositeVideoClip([full_image_video, full_text_clips]).set_audio(full_audio)

    final_video.write_videofile(os.path.join(cg.destination, "final_video.mp4"), codec='libx264', audio_codec='aac', fps=6, threads=4, logger=None)
    
