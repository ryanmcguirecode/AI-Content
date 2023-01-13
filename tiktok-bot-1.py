from pytube import Playlist, YouTube
import json
from moviepy.editor import *
import os
from random import randrange, choice

from generate_video import save_video
from constants import FINAL_VIDEO_HEIGHT as FVH, FINAL_VIDEO_WIDTH as FVW
from tiktok_upload import upload

def generate_new_videos(playlist_url, used_videos, bottom_video_path, videos_outpath):
    
    video_urls = list(Playlist(playlist_url).video_urls)
    video_urls = [video for video in video_urls if video not in used_videos]
    if not video_urls:
        raise Exception("No videos left to generate")
    video = YouTube(choice(video_urls))
    
    highresvid = video.streams.get_highest_resolution()
    highresvid.download("content_resources", filename="temp_video.mp4")
    
    clip1 = VideoFileClip(os.path.join("content_resources", "temp_video.mp4"))
    clip2 = VideoFileClip(os.path.join("content_resources", bottom_video_path)).without_audio()

    clip2_start = randrange(0, int(clip2.duration - clip1.duration - 1))
    clip2 = clip2.subclip(clip2_start, clip2_start + clip1.duration)

    clip1 = clip1.resize(height=(FVH // 2))
    clip2 = clip2.resize(height=(FVH - clip1.size[1]))

    offset1 = (clip1.size[0] - FVW) // 2
    clip1 = clip1.crop(
        x1=offset1, y1=0, x2=(offset1 + FVW), y2=clip1.size[1]
    )

    offset2 = (clip2.size[0] - FVW) // 2
    clip2 = clip2.crop(
        x1=offset2, y1=0, x2=(offset2 + FVW), y2=clip2.size[1]
    )

    final_video = clips_array([[clip1], 
                                [clip2]])

    final_video_length = int(final_video.duration)
    print("Final video length:", final_video_length)
    
    if final_video_length % 60 != 0:
        num_videos = (final_video_length // 60) + 1
    else:
        num_videos = final_video_length // 60
    print("Number of videos:", num_videos)
        
    videos = []
    vid_length = final_video_length // num_videos
    last_time = 0
    for i in range(num_videos):
        if i == num_videos - 1:
            videos.append(final_video.subclip(last_time, final_video_length))
            continue
        videos.append(final_video.subclip(last_time, min(last_time + vid_length, final_video_length)))
        last_time += vid_length
        
    if not os.path.exists(os.path.join("generated_content", "videos")):
        os.makedirs("generated_content", "videos")
    for i, video in enumerate(videos):
        save_video(video, os.path.join("generated_content", "videos", "video{0}.mp4".format(i + 1)))
    
    os.remove(os.path.join("content_resources", "temp_video.mp4"))
    print("Done generating videos")
    
def get_video_queue():
    vids = os.listdir(os.path.join("generated_content", "videos"))
    vids = [vid for vid in vids if vid.endswith(".mp4")]
    vids = sorted(vids, key= lambda s: int("".join(list(filter(str.isdigit, s)))))
    return vids

def get_video(playlist_url, used_videos, bottom_video_path, videos_outpath):
    if (not os.path.exists(os.path.join("generated_content", "videos"))
        or not get_video_queue()):
        generate_new_videos(playlist_url, used_videos, bottom_video_path, videos_outpath)
    
    return os.path.join("generated_content", "videos", get_video_queue()[0])

if __name__ == "__main__":
    with open("settings.json", "r") as f:
        settings = json.loads(f.read())
    username = settings["username"]
    password = settings["password"]
    playlist_url = settings["playlist_url"]
    used_videos = settings["used_videos"]
    vid = get_video(playlist_url, used_videos, "magnet_balls.mp4", "generated_content/videos")
    with open("settings.json", "w") as f:
        f.write(json.dumps(settings))
    
    caption = "Part {0} #msa #mystoryanimated #storytime #storyanimated".format(
        int("".join(list(filter(str.isdigit, vid))))
    )
    upload(username, vid, caption)
    os.remove(vid)