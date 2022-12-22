import ContentGenerator
from constants import SUBTITLE_DIVISION

from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import json

def generate(cg : ContentGenerator, music_filepath : str):
    
    images = list(filter(lambda f: '.jpg' in f, os.listdir(cg.images_directory)))
    images.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
    
    voiceover_path = os.path.join(cg.destination, "generated_voiceover.wav")
    voiceover = AudioFileClip(voiceover_path)
    timestamp_path = os.path.join(cg.destination, "timestamps.json")
    with open(timestamp_path, "r") as f:
        timestamps = json.load(f)
    
    music = AudioFileClip(music_filepath).subclip(0, voiceover.duration)
    full_audio = CompositeAudioClip([voiceover, music])
    
    
    image_clips = []
    seen_words = 0
    prev_time = 0
    
    # print(cg.paragraph_lengths)
    
    for i in range(len(images)):
        image_path = os.path.join(cg.images_directory, images[i])
        seen_words += cg.paragraph_lengths[i]
        # print(i, seen_words)
        image_duration = timestamps[str(seen_words)] - prev_time
        prev_time = timestamps[str(seen_words)]
        image_clip = ImageClip(image_path).set_duration(image_duration)
        image_clips.append(image_clip)
        
    text_clips = []
    words = cg.text.split(" ")
    subtitle_groups = [" ".join(words[i:i+SUBTITLE_DIVISION]) for i in range(0, len(words), SUBTITLE_DIVISION)]
    seen_words = 0
    prev_time = 0
    for sg in subtitle_groups:
        # print(sg)
        seen_words += len(sg.split())
        text_clip = TextClip(sg, fontsize=50, color="black", bg_color="white").set_duration(timestamps[str(seen_words)] - prev_time)
        prev_time = timestamps[str(seen_words)]
        text_clips.append(text_clip)

    full_image_video = concatenate_videoclips(image_clips)
    full_text_clips = concatenate_videoclips(text_clips).set_pos(("center", "bottom"))
    final_video = CompositeVideoClip([full_image_video, full_text_clips]).set_audio(full_audio)

    final_video.write_videofile(os.path.join(cg.destination, "final_video.mp4"), codec='libx264', audio_codec='aac', fps=24)
    
