import os
from moviepy.editor import VideoFileClip, CompositeAudioClip, CompositeVideoClip, \
    clips_array, concatenate_videoclips

from ImageSlideshowGenerator import ImageSlideshowGenerator
from ContentParameters import ContentParameters
from generate_video import generate_voiceover_audiofileclip, get_timestamps, \
    generate_music_audiofileclip, generate_image_imageclips, generate_subtitle_textclips, \
    save_video
from constants import FINAL_VIDEO_WIDTH as FVW, FINAL_VIDEO_HEIGHT as FVH

class ImageSlideshowBottomVideoGenerator(ImageSlideshowGenerator):
    def __init__(self, cp: ContentParameters) -> str:
        super().__init__(cp)
        
    def generate_video(self):
        """ Generate and save final video based on all content """
        
        print("Generating final video...")
        
        self.voiceover = generate_voiceover_audiofileclip(self, self.content_parameters)
        self.timestamps = get_timestamps(self, self.content_parameters)
        
        self.content_parameters.music.music_duration = self.voiceover.duration + self.content_parameters.end_time
        music_audio = generate_music_audiofileclip(self, self.content_parameters)
        full_audio = CompositeAudioClip([self.voiceover, music_audio])
        
        image_clips = generate_image_imageclips(self, self.content_parameters)
        image_clips = [clip.resize(height=1080) for clip in image_clips]
        image_clips[-1].duration += self.content_parameters.end_time
        text_clips = generate_subtitle_textclips(self, self.content_parameters)

        full_image_video = concatenate_videoclips(image_clips)
        
        bottom_video = self.content_parameters.video
        bottom_video_clip = VideoFileClip(bottom_video.filepath).without_audio()
        st = bottom_video.start_time
        bottom_video_clip = bottom_video_clip.subclip(st, st + full_image_video.duration)
        bottom_video_clip = bottom_video_clip.resize(height=(FVH - full_image_video.size[1]))
        offset = (bottom_video_clip.size[0] - 1080) // 2
        bottom_video_clip = bottom_video_clip.crop(
            x1=offset, y1=0, x2=(offset + FVW), y2=bottom_video_clip.size[1]
        )
        
        full_video = clips_array([[full_image_video], 
                                  [bottom_video_clip]])
        full_text_clips = concatenate_videoclips(text_clips).set_pos(("center", 800))
        
        self.final_video = CompositeVideoClip([full_video, full_text_clips]).set_audio(full_audio)
        self.video_outpath = os.path.join(self.destination, "final_video.mp4")
        save_video(self.final_video, self.video_outpath)
        
        print("Final video saved to " + self.video_outpath)
        
class ImageSlideshowBottomVideoGeneratorTest(ImageSlideshowBottomVideoGenerator):
    def __init__(self, cp: ContentParameters) -> str:
        super().__init__(cp)
        self.destination = "generated_content/test_video_01052023_1903"
        
    def initialize_text(self):
        pass
    
    def initialize_audio(self):
        pass
    
    def initialize_visuals(self):
        pass
    