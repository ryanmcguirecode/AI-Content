import google.cloud.texttospeech as tts
import os
from random import choice

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/key.json"

class Voice:
    def __init__(self, voice_name, pitch=0):
        self.voice_name = voice_name
        self.language_code = "-".join(voice_name.split("-")[:2])
        self.pitch = pitch
        
def text_to_wav(text: str, filepath: str, voice: Voice):
    text_input = tts.SynthesisInput(text=text)
    
    voice_params = tts.VoiceSelectionParams(
        language_code=voice.language_code, name=voice.voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16, pitch=voice.pitch)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    with open(filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filepath}"')
        
def generate(text: str, filepath: str):
    voices = [Voice("en-US-Wavenet-I"), Voice("en-US-Neural2-D"), 
              Voice("en-US-Neural2-H"), Voice("en-US-Neural2-I"), 
              Voice("en-US-Neural2-J")]
    voice = choice(voices)
    text_to_wav(text, filepath, voice)