from rvc_config import Config
from vc.modules import VC

from typing import Literal
import os

class RVC_Instance:
    def __init__(self, config:Config, voice:str, model_name:str, index_path:str = None):
        self.voice = voice
        self.model_name = model_name
        self.index_path = index_path

        self.vc = VC(config)
        self.vc.get_vc(self.model_name)
        

    def infer(self, audio, f0method:Literal["pm", "harvest", "crepe", "rmvpe"] = "harvest", f0up_key:int = 0, index_rate:float = 0.0, filter_radius:int = 3, resample_sr:int = 48000, rms_mix_rate:float = 0.25, protect:float = 0.33):
        _, wav_opt = self.vc.vc_single(
            0,
            audio,
            f0up_key,
            None,
            f0method,
            self.index_path,
            None,
            index_rate,
            filter_radius,
            resample_sr,
            rms_mix_rate,
            protect,
        )

        return wav_opt[1]


class RVC_Model:
    def __init__(self):
        self.config = Config()
        self.voices = {}
    
    def infer(self, voice:str, audio, f0method:Literal["pm", "harvest", "crepe", "rmvpe"] = "harvest", f0up_key:int = 0, index_rate:float = 0.0, filter_radius:int = 3, resample_sr:int = 48000, rms_mix_rate:float = 0.25, protect:float = 0.33):
        rvc = self.get_voice(voice)
        
        return rvc.infer(audio, f0method, f0up_key, index_rate, filter_radius, resample_sr, rms_mix_rate, protect)
    
    def get_voice(self, voice):
        if voice in self.voices:
            return self.voices[voice]
        
        if not os.path.exists(f"/data/rvc_voices/{voice}"):
            raise ValueError(f"Voice '{voice}' does not exist")
        
        files = os.listdir(f"/data/rvc_voices/{voice}")

        for file in files:
            if file.endswith(".pth"):
                model_name = file
            if file.endswith(".index") and not "trained" in file:
                index_name = file
            
        if not model_name:
            raise ValueError(f"No model found for voice {voice}")
        
        if index_name:
            index_path=f"/data/rvc_voices/{voice}/{index_name}"

        rvc = RVC_Instance(self.config, voice, model_name=f"{voice}/{model_name}", index_path=index_path)
        self.voices[voice] = rvc
        return rvc