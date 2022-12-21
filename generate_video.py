import ContentGenerator
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

def generate(cg : ContentGenerator):
    
    images = list(filter(lambda f: '.jpg' in f, os.listdir(cg.images_directory)))
    images.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
    voiceovers = list(filter(lambda f: '.wav' in f, os.listdir(cg.voiceovers_directory)))
    voiceovers.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
    
    composite_videos = []
    for i in range(len(voiceovers)):
        voiceover_path = os.path.join(cg.voiceovers_directory, voiceovers[i])
        voiceover = AudioFileClip(voiceover_path)
        image_path = os.path.join(cg.images_directory, images[i])
        image_clip = ImageClip(image_path).set_duration(voiceover.duration)
        image_clip = image_clip.set_audio(voiceover)
        text_clip = TextClip(cg.paragraphs[i], fontsize=50, color="white")
        text_clip = text_clip.set_pos('center').set_duration(voiceover.duration)
        
        composite_videos.append(CompositeVideoClip([image_clip, text_clip]))

    final_video = concatenate_videoclips(composite_videos)
    # music_path = os.path.join("content_resources", "minecraft_relaxing_fireplace.mp3")
    # music = AudioFileClip(music_path).subclip(0, final_video.duration)
    # final_video = CompositeVideoClip([final_video, music])

    #TODO: delete old directory
    final_video.write_videofile(os.path.join(cg.destination, "final_video.mp4"), codec='libx264', audio_codec='aac', fps=24)