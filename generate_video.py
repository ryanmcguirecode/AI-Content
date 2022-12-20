from moviepy.editor import ImageSequenceClip, TextClip
import os

clip.set_position(lambda t: ('center', 500 + (1080-500)*(t/5)))

# Set the text and the language
text = "This is the voice over for the video. This text should appear on the first image. And this text should appear on the second image."
language = "en"

# Split the text into a list of sentences
sentences = text.split(". ")

# Convert the text to audio using gTTS
audio = gTTS(text, lang=language)

# Save the audio to a file
audio.save("voice_over.mp3")

# Create a list of image filenames
image_filenames = ["image1.jpg", "image2.jpg", "image3.jpg"]

# Create a list of text clips, one for each sentence
text_clips = []
for sentence in sentences:
    text_clip = TextClip(txt=sentence, fontsize=24, color='white')
    text_clips.append(text_clip)

# Create the video using MoviePy
clip = ImageSequenceClip(image_filenames, fps=1)
clip = clip.set_audio(audio)
clip = clip.set_duration(len(sentences))
clip = clip.set_pos((0, 30))

final_clip = clip.CompositeVideoClip([clip, text_clips])
final_clip.write_videofile("voice_over_video.mp4")

# Clean up the audio file
os.remove("voice_over.mp3")
