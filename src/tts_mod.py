import os
from time import time

from utils import singleton

import torch
from typing import Literal

from tortoise_tts.tortoise.api_fast import TextToSpeech, MODELS_DIR
from tortoise_tts.tortoise.utils.audio import load_voice, load_audio
from tortoise_tts.tortoise.utils.text import split_and_recombine_text

import logging
logger = logging.getLogger(__name__)


Preset = Literal['ultra_fast', 'fast', 'standard', 'high_quality']

class TTS_Instance:
    def __init__(self, tts, voice):
        self.tts = tts
        self.voice = voice
        self.samples = []

        files = os.listdir(f"/data/voices/{voice}/samples")
        for file in files:
            audio = load_audio(f"/data/voices/{voice}/samples/{file}", 22050)
            self.samples.append(audio)

        if not self.samples:
            logger.error(f"No samples found for voice '{voice}'")
            raise ValueError(f"No samples found for voice '{voice}'")
        

    def infer(self, text:str, preset:Preset = 'standard', seed:int = None, temperature:float = 0.2):
        if not text:
            logger.error("No text specified")
            raise ValueError("No text specified")
        
        texts = split_and_recombine_text(text)
        seed = int(time()) if seed is None else seed

        presets = {
            'ultra_fast': {'num_autoregressive_samples': 1, 'diffusion_iterations': 10},
            'fast': {'num_autoregressive_samples': 32, 'diffusion_iterations': 50},
            'standard': {'num_autoregressive_samples': 256, 'diffusion_iterations': 200},
            'high_quality': {'num_autoregressive_samples': 256, 'diffusion_iterations': 400},
        }

        preset_args = presets[preset]

        def audio_stream():
            for _text in texts:
                audio_generator = self.tts.tts_stream(_text, voice_samples=self.samples, use_deterministic_seed=seed, temperature=temperature, **preset_args)
                for wav_chunk in audio_generator:
                    yield wav_chunk

        audio_tensor = torch.cat(list(audio_stream())).cpu()
        return audio_tensor.numpy(), 24000


@singleton
class TTS_Model:
    def __init__(self):
        logger.info("Initializing TTS_Model")
        if not torch.cuda.is_available():
            logger.error("No CUDA device found, using CPU")

        use_deepspeed = os.environ.get('USE_DEEPSPEED', 'false').lower() == 'true'
        if torch.backends.mps.is_available() and use_deepspeed:
            logger.warning("DeepSpeed is not compatible with MPS, disabling it.")
            use_deepspeed = False

        logger.info(f"Using DeepSpeed: {use_deepspeed}")

        self.tts = TextToSpeech(models_dir=MODELS_DIR, use_deepspeed=use_deepspeed, kv_cache=True, half=True)
        self.voices = {}


    def infer(self, voice:str, text:str, preset:Preset = 'standard', seed:int = None, temperature:float = 0.2):
        tts = self.get_voice(voice)
        return tts.infer(text, preset, seed, temperature)
    

    def get_voice(self, voice:str):
        if not voice:
            logger.error("No voice specified")
            raise ValueError("No voice specified")

        if voice in self.voices:
            return self.voices[voice]
        
        logger.info(f"Loading TTS voice '{voice}'")

        if not os.path.exists(f"/data/voices/{voice}"):
            logger.error(f"Voice '{voice}' does not exist")
            raise ValueError(f"Voice '{voice}' does not exist")
        
        tts = TTS_Instance(self.tts, voice)
        self.voices[voice] = tts
        return tts