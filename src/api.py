from tts_mod import TTS_Model, Preset
from rvc_mod import RVC_Model, F0Method
from utils import base64_url_to_audio

tts_model = TTS_Model
rvc_model = RVC_Model

def tts(voice:str, text:str, preset:Preset = 'standard', seed:int = None, temperature:float = 0.2,
        use_rvc:bool = True, method:F0Method = "rmvpe", f0up_key:int = 0, index_rate:float = 0.0,
        filter_radius:int = 3, resample_sr:int = 48000, rms_mix_rate:float = 0.25,
        protect:float = 0.33):
    
    tts_audio, tts_sample_rate = tts_model.infer(voice, text, preset, seed, temperature)

    if not use_rvc:
        return tts_audio, tts_sample_rate
    
    rvc_audio, rvc_sample_rate = rvc_model.infer(voice, tts_audio, method, f0up_key, index_rate, filter_radius, resample_sr, rms_mix_rate, protect)
    return rvc_audio, rvc_sample_rate


def convert(voice:str, audio:str, method:F0Method = "rmvpe", f0up_key:int = 0,
            index_rate:float = 0.0, filter_radius:int = 3, resample_sr:int = 48000,
            rms_mix_rate:float = 0.25, protect:float = 0.33):
    
    # TODO: Check if decoding works
    audio_np, sample_rate = base64_url_to_audio(audio)
    
    return rvc_model.infer(voice, audio_np, method, f0up_key, index_rate, filter_radius, resample_sr, rms_mix_rate, protect)