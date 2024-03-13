from tts_mod import TTS_Model
from rvc_mod import RVC_Model
from rest_api import start_server

import io
import os
import soundfile

def main():
    os.system("/app/src/download-models.sh")

    text = "Favorite anime character? Oh, someone who's a master of avoiding responsibilities - they're living my dream! Maybe one who can teleport out of awkward situations. I could use that skill during glitchy streams."
    voice = "nekora"
    preset = "standard"
    seed = None
    temperature = 0.2

    tts = TTS_Model()
    rvc = RVC_Model()

    tts_audio, tts_sample_rate = tts.infer(voice, text, preset, seed, temperature)
    soundfile.write('/data/results/output-tts.mp3', tts_audio, tts_sample_rate, format='mp3')

    rvc_audio, rvc_sample_rate = rvc.infer(voice, tts_audio, f0method="rmvpe")
    soundfile.write('/data/results/output-rvc.mp3', rvc_audio, rvc_sample_rate, format='mp3')

    start_server()

if __name__ == "__main__":
    main()