import io
import os
from time import time

from waitress import serve
import soundfile as sf

import torch
import torchaudio

from tortoise_tts.tortoise.api_fast import TextToSpeech, MODELS_DIR
from tortoise_tts.tortoise.utils.audio import load_voice
from tortoise_tts.tortoise.utils.text import split_and_recombine_text

SECRET_KEY = os.environ.get('SECRET_KEY', None)
TORTOISE_VOICES_DIR = os.environ.get('TORTOISE_VOICES_DIR', '/data/tts_voices')

class TTS_Model:
    def __init__(self):
        if not torch.cuda.is_available():
            print("!!! No CUDA device found, using CPU !!!")

        use_deepspeed = os.environ.get('USE_DEEPSPEED', 'false').lower() == 'true'
        if torch.backends.mps.is_available() and use_deepspeed:
            print("DeepSpeed is not compatible with MPS, disabling it.")
            use_deepspeed = False
        print(f"Using DeepSpeed: {use_deepspeed}", flush=True)
        
        self.tts = TextToSpeech(models_dir=MODELS_DIR, use_deepspeed=use_deepspeed, kv_cache=True, half=True)


    def infer(self, text, voice, preset='standard', seed=None):
        audio_stream = self._infer_stream(text, voice, preset, seed)
        return self._stream_to_np(audio_stream)


    def _infer_stream(self, text, voice, preset, seed):
        texts = split_and_recombine_text(text)
        seed = int(time()) if seed is None else seed
        voice_samples, conditioning_latents = load_voice(voice, [TORTOISE_VOICES_DIR])

        presets = {
            'ultra_fast': {'num_autoregressive_samples': 1, 'diffusion_iterations': 10},
            'fast': {'num_autoregressive_samples': 32, 'diffusion_iterations': 50},
            'standard': {'num_autoregressive_samples': 256, 'diffusion_iterations': 200},
            'high_quality': {'num_autoregressive_samples': 256, 'diffusion_iterations': 400},
        }

        preset_args = presets[preset]

        # Hardcoded preset args for testing purposes
        # preset_args = {'num_autoregressive_samples': 512, 'diffusion_iterations': 400}

        for j, text in enumerate(texts):
            audio_generator = self.tts.tts_stream(text, voice_samples=voice_samples, use_deterministic_seed=seed, temperature=0.2, **preset_args)
            for wav_chunk in audio_generator:
                yield wav_chunk



    def _stream_to_np(self, audio_stream):
        audio_tensor = torch.cat(list(audio_stream)).cpu()
        audio_np = audio_tensor.numpy()
        return audio_np
        # torchaudio.save('/data/results/output.mp3', audio_tensor.unsqueeze(0), 24000)

    def _np_to_mp3(self, audio_np):
        audio_data = io.BytesIO()
        sf.write(audio_data, audio_np, 24000, format='mp3')
        audio_data.seek(0)
        return audio_data


# if __name__ == '__main__':
#     port = os.environ.get('PORT', 6600)
#     print(f"Running TTS server on port {port}")
#     serve(app, host="0.0.0.0", port=port)