import google.cloud.texttospeech_v1beta1 as tts
import os
import json
from random import choice

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/key.json"

class Voice:
    def __init__(self, voice_name, pitch=0):
        self.voice_name = voice_name
        self.language_code = "-".join(voice_name.split("-")[:2])
        self.pitch = pitch
        
def text_to_wav(text: str, outpath: str, voice: Voice):
    client = tts.TextToSpeechClient()
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=voice.language_code, name=voice.voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16, pitch=voice.pitch)
    
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    voiceover_outpath = os.path.join(outpath, "voiceover.wav")
    with open(voiceover_outpath, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{voiceover_outpath}"')
        
def ssml_to_wav(ssml_text: str, voiceover_outpath: str, timestamps_outpath: str, voice: Voice):
    client = tts.TextToSpeechClient()
    synthesis_input = tts.SynthesisInput(ssml=ssml_text)
    voice_params = tts.VoiceSelectionParams(
        language_code=voice.language_code, name=voice.voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16, pitch=voice.pitch)
    
    response = client.synthesize_speech(
        request=tts.SynthesizeSpeechRequest(
            input=synthesis_input, voice=voice_params, audio_config=audio_config, 
            enable_time_pointing=[tts.SynthesizeSpeechRequest.TimepointType.SSML_MARK]
        )
    )

    marks = {t.mark_name : t.time_seconds for t in response.timepoints}
    # print(response.timepoints)
    # print(marks)
    with open(timestamps_outpath, 'w') as out:
        json.dump(marks, out)
        print(f'Marks content written to file: {timestamps_outpath}')
    
    with open(voiceover_outpath, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{voiceover_outpath}"')
    
        
def select_voice():
    voices = [Voice("en-US-Wavenet-I")]
            #   Voice("en-US-Neural2-D")], 
            #   Voice("en-US-Neural2-H"), Voice("en-US-Neural2-I"), 
            #   Voice("en-US-Neural2-J")]
    return choice(voices)
    
def text_to_ssml(text: str):
    paragraphs = []
    i = 1
    for p in text.split("\n"):
        paragraphs.append([])
        for word in p.split():
            paragraphs[-1].append(word + " <mark name=\"{}\"/>".format((str(i))))
            i += 1
    paragraphs = [" ".join(p) for p in paragraphs]
    new_text = "<speak>" + "".join(paragraphs) + "</speak>"
    return new_text

def generate(text: str, voiceover_outpath: str, timestamps_outpath: str, voice: Voice):
    ssml_text = text_to_ssml(text)
    print(ssml_text)
    ssml_to_wav(ssml_text, voiceover_outpath, timestamps_outpath, voice)
    