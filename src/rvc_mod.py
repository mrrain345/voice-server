from vc.config import Config
from vc.modules import VC
from utils import singleton

from typing import Literal
import os

import logging
logger = logging.getLogger(__name__)

F0Method = Literal["pm", "harvest", "crepe", "rmvpe"]

class RVC_Instance:
    def __init__(self, config:Config, voice:str, model_name:str, index_path:str = None):
        self.voice = voice
        self.model_name = model_name
        self.index_path = index_path

        self.vc = VC(config)
        self.vc.get_vc(self.model_name)
        

    def infer(self, audio, f0method:F0Method = "harvest", f0up_key:int = 0, index_rate:float = 0.0, filter_radius:int = 3, resample_sr:int = 48000, rms_mix_rate:float = 0.25, protect:float = 0.33):
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

        sample_rate, audio = wav_opt

        return audio, sample_rate


@singleton
class RVC_Model:
    def __init__(self):
        logger.info("Initializing RVC_Model")
        self.config = Config()
        self.voices = {}
    
    def infer(self, voice:str, audio, f0method:F0Method = "rmvpe", f0up_key:int = 0, index_rate:float = 0.0, filter_radius:int = 3, resample_sr:int = 48000, rms_mix_rate:float = 0.25, protect:float = 0.33):
        rvc = self.get_voice(voice)
        
        return rvc.infer(audio, f0method, f0up_key, index_rate, filter_radius, resample_sr, rms_mix_rate, protect)
    
    def get_voice(self, voice):
        if not voice:
            logger.error("No voice specified")
            raise ValueError("No voice specified")

        if voice in self.voices:
            return self.voices[voice]
        
        logger.info(f"Loading RVC voice {voice}")

        if not os.path.exists(f"/data/voices/{voice}"):
            logger.error(f"Voice '{voice}' does not exist")
            raise ValueError(f"Voice '{voice}' does not exist")
        
        files = os.listdir(f"/data/voices/{voice}")

        for file in files:
            if file.endswith(".pth"):
                model_name = file
            if file.endswith(".index") and not "trained" in file:
                index_name = file
            
        if not model_name:
            logger.error(f"No RVC model found for voice '{voice}'")
            raise ValueError(f"No RVC model found for voice '{voice}'")
        else:
            logger.info(f"Using RVC model '/data/voices/{voice}/{model_name}' for voice '{voice}'")
        
        if index_name:
            index_path=f"/data/voices/{voice}/{index_name}"
            logger.info(f"Using RVC index '{index_path}' for voice '{voice}'")


        rvc = RVC_Instance(self.config, voice, model_name=f"{voice}/{model_name}", index_path=index_path)
        self.voices[voice] = rvc
        return rvc