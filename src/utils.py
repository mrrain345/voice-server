import io
import soundfile
import base64
import numpy as np

def singleton(func):
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = func(*args, **kwargs)
        return wrapper.instance

    wrapper.instance = None
    return wrapper

def audio_to_mp3_stream(audio_stream, sample_rate):
    audio_data = io.BytesIO()
    soundfile.write(audio_data, audio_stream, sample_rate, format='mp3')
    audio_data.seek(0)
    return audio_data

def base64_url_to_audio(base64_url):
    mime, base64_str = base64_url.split(",")
    audio_data = io.BytesIO(base64.b64decode(base64_str))
    audio, sample_rate = soundfile.read(audio_data)
    return audio, sample_rate