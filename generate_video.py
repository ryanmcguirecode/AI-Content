from ContentGenerator import ContentGenerator
from ContentParameters import ContentParameters
from constants import SUBTITLE_DIVISION as SD, FINAL_VIDEO_HEIGHT as FVH, FINAL_VIDEO_WIDTH as FVW, VIDEO_FPS as FPS

from moviepy.editor import *
# from moviepy.video.fx.all import scroll
import json

def get_subtitle_groups(words: list[str]) -> list[str]:
    """ Generate subtitle groups from list of words """
    
    subtitle_groups = [[]]
    punctuation_marker = False
    for word in words:
        if len(subtitle_groups[-1]) >= SD or punctuation_marker:
            subtitle_groups.append([])
        subtitle_groups[-1].append(word)
        punctuation_marker= "." in word or "?" in word or "!" in word or "," in word
    return [" ".join(sg) for sg in subtitle_groups]

def get_timestamps(cg: ContentGenerator, cp: ContentParameters) -> dict:
    """ Generate timestamps for video """
    
    timestamps_outpath = os.path.join(cg.audio_path, "timestamps.json")
    with open(timestamps_outpath, "r") as f:
        timestamps = json.load(f)
    return timestamps

def get_image_path_list(images_directory: str) -> list[str]:
    """ Return list of images in images directory """
    
    images = list(filter(lambda f: '.jpg' in f, os.listdir(images_directory)))
    images.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
    return images

def generate_voiceover_audiofileclip(cg: ContentGenerator, cp: ContentParameters) -> AudioFileClip:
    """ Generate voiceover for video """
    
    voiceover_outpath = os.path.join(cg.audio_path, "generated_voiceover.wav")
    voiceover = AudioFileClip(voiceover_outpath)
    return voiceover

def generate_music_audiofileclip(cg: ContentGenerator, cp: ContentParameters) -> AudioFileClip:
    """ Generate music for video """
    
    s = cp.music.music_start
    dur = cp.music.music_duration
    vol = cp.music.music_volume
    music_audio = AudioFileClip(cp.music.music_filepath).subclip(s, s + dur).volumex(vol)
    return music_audio

def generate_image_imageclips(cg: ContentGenerator, cp: ContentParameters) -> list[ImageClip]:
    """ Generate image clips for video """
    
    images = get_image_path_list(cg.images_directory)
    
    image_clips = []
    seen_words = 0
    prev_time = 0
    for i in range(len(images)):
        image_path = os.path.join(cg.images_directory, images[i])
        seen_words += cg.paragraph_lengths[i]
        image_duration = cg.timestamps[str(seen_words)] - prev_time
        image_clip = ImageClip(image_path).set_duration(image_duration)
        image_clips.append(image_clip)
    return image_clips

def generate_subtitle_textclips(cg: ContentGenerator, cp: ContentParameters) -> list[TextClip]:
    """ Generate subtitle text clips for video """
    
    text_clips = []
    words = cg.text.split()
    subtitle_groups = get_subtitle_groups(words)
    seen_words = 0
    prev_time = 0
    for sg in subtitle_groups:
        seen_words += len(sg.split())
        text_clip = TextClip(sg, font="content_resources/Fonts/Anton/Anton-Regular.ttf", 
                             method="caption", fontsize=75, color="white", 
                             stroke_color="black",stroke_width=4.5, size=(700, None)).set_duration(cg.timestamps[str(seen_words)] - prev_time)
        prev_time = cg.timestamps[str(seen_words)]
        text_clips.append(text_clip)
    return text_clips

def resize_video(video: VideoClip) -> VideoClip:
    """ Resize video to fit final video dimensions """
        
    return video.resize(newsize=(FVW,FVH))

def save_video(video: VideoClip, outpath: str):
    """ Save video to outpath """
    
    video.write_videofile(outpath, fps=FPS, codec='libx264', audio_codec='aac', threads=8)
    
# def generate(cg, cp):
    
#     images = list(filter(lambda f: '.jpg' in f, os.listdir(cg.images_directory)))
#     images.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
    
#     voiceover_path = os.path.join(cg.audio_path, "generated_voiceover.wav")
#     voiceover = AudioFileClip(voiceover_path)
#     timestamp_path = os.path.join(cg.audio_path, "timestamps.json")
#     with open(timestamp_path, "r") as f:
#         timestamps = json.load(f)
    
#     ms = cp.music.music_start
#     music = AudioFileClip(cp.music.music_filepath).subclip(ms, ms + voiceover.duration).volumex(.1)
#     full_audio = CompositeAudioClip([voiceover, music])
    
#     image_clips = []
#     seen_words = 0
#     prev_time = 0
    
#     for i in range(len(images)):
#         image_path = os.path.join(cg.images_directory, images[i])
#         seen_words += cg.paragraph_lengths[i]
#         image_duration = timestamps[str(seen_words)] - prev_time
#         image_clip = ImageClip(image_path).set_duration(image_duration)
#         image_clips.append(image_clip)
        
#     text_clips = []
#     words = cg.text.split()
#     subtitle_groups = get_subtitle_groups(words)
#     seen_words = 0
#     prev_time = 0
#     for sg in subtitle_groups:
#         seen_words += len(sg.split())
#         text_clip = TextClip(sg, font="content_resources/Fonts/Anton/Anton-Regular.ttf", 
#                              method="caption", fontsize=75, color="white", 
#                              stroke_color="black",stroke_width=4.5, size=(700, None)).set_duration(timestamps[str(seen_words)] - prev_time)
#         prev_time = timestamps[str(seen_words)]
#         text_clips.append(text_clip)
        
#     full_image_video = concatenate_videoclips(image_clips)
#     full_text_clips = concatenate_videoclips(text_clips).set_pos(("center", 1320))
    
#     full_image_text_video = CompositeVideoClip([full_image_video, full_text_clips]).set_audio(full_audio)
#     bottom_video = VideoFileClip(cp.bottom_video_path).without_audio()
    
#     final_video = clips_array([[full_image_text_video], 
#                                [bottom_video]])
    
#     final_video.write_videofile(os.path.join(cg.destination, "final_video.mp4"), codec='libx264', audio_codec='aac', fps=FPS, threads=4)