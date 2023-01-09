import os 
from traceback import print_exc
from moviepy.editor import CompositeAudioClip, CompositeVideoClip, concatenate_videoclips, VideoFileClip
from moviepy.video.fx.all import scroll

from ContentGenerator import ContentGenerator
from ContentParameters import ContentParameters
import generate_voiceover
import generate_text
from generate_video import generate_voiceover_audiofileclip, get_timestamps, \
    generate_music_audiofileclip, generate_subtitle_textclips, \
    save_video
from constants import FINAL_VIDEO_WIDTH as FVW, FINAL_VIDEO_HEIGHT as FVH

class TextVideoGenerator(ContentGenerator):
    def __init__(self, cp: ContentParameters) -> str:
        super().__init__(cp)
    
    def initialize_text(self):
        """ Generate ChatGPT response based on prompt """
        
        print("Generating ChatGPT response based on prompt...")
        try:
            filepath = os.path.join(self.destination, "generated_text.txt")
            self.text = generate_text.generate(self.content_parameters.story_prompt.text, filepath)
            self.text = self.text.strip().replace("\"", "")
        except:
            print("Error generating text:")
            print_exc()
            exit()
        
    def initialize_audio(self):
        """ Generate Google TTS voiceover and timestamps """
        
        self.voice = generate_voiceover.select_voice()
        print("Generating Google TTS voiceover and timestamps...")
        try:
            voiceover_outpath = os.path.join(self.audio_path, "generated_voiceover.wav")
            timestamps_outpath = os.path.join(self.audio_path, "timestamps.json")
            generate_voiceover.generate(self.text, voiceover_outpath, timestamps_outpath, self.voice,
                                        sentence_pause=2)
        except:
            print("Error generating voiceovers:")
            print_exc()
            exit()
    
    def initialize_visuals(self):
        """ Not implemented here """
        pass
    
    def generate_video(self):
        """ Generate and save final video based on all content """
        
        print("Generating final video...")
        
        self.voiceover = generate_voiceover_audiofileclip(self, self.content_parameters)
        self.timestamps = get_timestamps(self, self.content_parameters)
        print(self.timestamps)
        duration = self.voiceover.duration + self.content_parameters.end_time
        
        self.content_parameters.music.music_duration = duration
        music_audio = generate_music_audiofileclip(self, self.content_parameters)
        full_audio = CompositeAudioClip([self.voiceover, music_audio])
        
        text_clips = generate_subtitle_textclips(self, self.content_parameters)
        full_text_clips = concatenate_videoclips(text_clips).set_pos(("center", "center"))
        
        video = self.content_parameters.video
        video_clip = VideoFileClip(video.filepath).without_audio()
        st = video.start_time
        video_clip = video_clip.subclip(st, st + duration)
        video_clip = video_clip.resize(height=FVH)
        offset = (video_clip.size[0] - 1080) // 2
        video_clip = video_clip.crop(
            x1=offset, y1=0, x2=(offset + FVW), y2=video_clip.size[1]
        )
        
        self.final_video = CompositeVideoClip([video_clip, full_text_clips]).set_audio(full_audio)
        self.video_outpath = os.path.join(self.destination, "final_video.mp4")
        save_video(self.final_video, self.video_outpath)
        
        print("Final video saved to " + self.video_outpath)