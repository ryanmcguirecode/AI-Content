import ContentGenerator
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

def generate_video(cg : ContentGenerator):
    voiceovers = []
    images = list(filter(sorted(os.listdir(cg.images_directory), key=lambda f: int(filter(str.isdigit, f))), lambda f: '.jpg' in f)) #list of images
    voiceovers = list(filter(sorted(os.listdir(cg.voiceovers_directory), key=lambda f: int("".join(filter(str.isdigit, f)))), lambda f: '.wav' in f)) #list of voiceovers
    composite_videos = []

    for i in range(len(voiceovers)):
        voiceover = (AudioFileClip(voiceovers[i]))
        video = ImageClip(images[i]).set_duration(voiceover.duration).set_audio(voiceover)
        text_clip = TextClip(cg.paragraphs[i], fontsize=50, color="white")
        text_clip = text_clip.set_pos('center').set_duration(voiceover.duration)
        
        composite_videos.append(CompositeVideoClip([video, text_clip]))

    final_video = concatenate_videoclips(composite_videos)
    music = AudioFileClip('music/minecraft_w_fire.m4a').subclip(0, final_video.duration)
    final_video = CompositeVideoClip([final_video, music])

    #TODO: delete old directory
    final_video.write_videofile(cg.destination, codec='libx264', audio_codec='aac')