from src.tts_mod import TTS_Model
from src.rvc_mod import RVC_Model

import io
import os
import soundfile as sf

def main():
    os.system("/app/src/download-models.sh")

    text = "Favorite anime character? Oh, someone who's a master of avoiding responsibilities - they're living my dream! Maybe one who can teleport out of awkward situations. I could use that skill during glitchy streams."
    voice = "nekora"
    preset = "standard"
    seed = None

    tts = TTS_Model()
    rvc = RVC_Model()

    tts_audio = tts.infer(text, voice, preset, seed)
    sf.write('/data/results/output-tts.mp3', tts_audio, 24000, format='mp3')

    rvc_audio = rvc.infer(voice, tts_audio, f0method="rmvpe")
    sf.write('/data/results/output-rvc.mp3', rvc_audio, 48000, format='mp3')


def audio_to_mp3_stream(audio_stream, sample_rate):
    audio_data = io.BytesIO()
    sf.write(audio_data, audio_stream, sample_rate, format='mp3')
    audio_data.seek(0)
    return audio_data

if __name__ == "__main__":
    main()