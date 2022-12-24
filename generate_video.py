# from ContentGenerator import ContentGenerator
# from ContentParameters import ContentParameters
from constants import SUBTITLE_DIVISION as SD, FINAL_VIDEO_HEIGHT as FVH, FINAL_VIDEO_WIDTH as FVW, VIDEO_FPS as FPS

from moviepy.editor import *
from moviepy.video.fx.all import scroll
import json

def get_subtitle_groups(words: list[str]):
    subtitle_groups = [[]]
    punctuation_marker = False
    for word in words:
        if len(subtitle_groups[-1]) >= SD or punctuation_marker:
            subtitle_groups.append([])
        subtitle_groups[-1].append(word)
        punctuation_marker= "." in word or "?" in word or "!" in word or "," in word
    return [" ".join(sg) for sg in subtitle_groups]

def generate(cg, cp):
    images = list(filter(lambda f: '.jpg' in f, os.listdir(cg.images_directory)))
    images.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
    
    voiceover_path = os.path.join(cg.audio_path, "generated_voiceover.wav")
    voiceover = AudioFileClip(voiceover_path)
    timestamp_path = os.path.join(cg.audio_path, "timestamps.json")
    with open(timestamp_path, "r") as f:
        timestamps = json.load(f)
    
    ms = cg.music.music_start
    music = AudioFileClip(cg.music.music_filepath).subclip(ms, ms + voiceover.duration).volumex(.1)
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
        image_clip = scroll(image_clip, w=608, h=1080, x_speed=((1080 - 608) / image_duration))
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

    full_image_video = concatenate_videoclips(image_clips).resize(newsize=(FVW,FVH))
    full_text_clips = concatenate_videoclips(text_clips).set_pos(("center", 1320))
    
    final_video = CompositeVideoClip([full_image_video, full_text_clips]).set_audio(full_audio)
    final_video.write_videofile(os.path.join(cg.destination, "final_video.mp4"), codec='libx264', audio_codec='aac', fps=FPS, threads=4)
    
    