import io
import os
from time import time

from flask import Flask, request, Response, jsonify
from waitress import serve
import soundfile as sf

import torch
import torchaudio

from tortoise_tts.tortoise.api_fast import TextToSpeech, MODELS_DIR
from tortoise_tts.tortoise.utils.audio import load_voice, BUILTIN_VOICES_DIR
from tortoise_tts.tortoise.utils.text import split_and_recombine_text

app = Flask(__name__)

SECRET_KEY = os.environ.get('SECRET_KEY', None)
TORTOISE_VOICES_DIR = os.environ.get('TORTOISE_VOICES_DIR', '/data/tts_voices')

@app.route('/tts/stream', methods=['POST'])
def api_tts_stream():
    start_time = time()

    data = request.get_json()
    voice = data.get('voice')
    text = data.get('text')
    preset = data.get('preset', 'standard')
    seed = data.get('seed', None)

    print(f"POST /tts/stream voice={voice}, preset={preset}, seed={seed}")

    secret = request.headers.get('Authorization', None)
    if SECRET_KEY and secret != f'Bearer {SECRET_KEY}':
        print(f"403 Forbidden | Invalid secret key")
        return jsonify({'error': 'Invalid secret key'}), 403

    error = api_validate(voice, text, preset, seed)
    if error:
        print(f"400 Bad Request | {error['error']}")
        return jsonify(error), 400
    

    mp3_data = infer(text, voice, preset, seed)

    end_time = time()
    print(f"200 OK | {end_time - start_time:.2f}s")
    return Response(mp3_data, mimetype='audio/mp3')


def infer(text, voice, preset, seed):
    audio_stream = tts_infer_stream(text, voice, preset, seed)
    mp3_data = audio_stream_to_mp3(audio_stream)
    return mp3_data


PRESETS = ['ultra_fast', 'fast', 'standard', 'high_quality']

def api_validate(voice, text, preset, seed):
    errors = {}
    voice_dir = os.path.join(BUILTIN_VOICES_DIR, voice)
    
    if not voice:
        errors['voice'] = 'Field is required'
    elif not os.path.exists(voice_dir):
        errors['voice'] = f'Voice "{voice}" does not exist'
    if text is None:
        errors['text'] = 'Field is required'
    if preset not in PRESETS:
        errors['preset'] = f'Invalid preset value. Allowed values are: {", ".join(PRESETS)}'
    if seed is not None and not isinstance(seed, int):
        errors['seed'] = 'Seed must be an integer'
    
    if errors:
        return {'error': 'Invalid request body', 'fields': errors}
    
    return None



def tts_infer_stream(text, voice, preset, seed):
    texts = split_and_recombine_text(text)
    
    seed = int(time()) if seed is None else seed

    voice_samples, conditioning_latents = load_voice(voice, [TORTOISE_VOICES_DIR])

    presets = {
        'ultra_fast': {'num_autoregressive_samples': 1, 'diffusion_iterations': 10},
        'fast': {'num_autoregressive_samples': 32, 'diffusion_iterations': 50},
        'standard': {'num_autoregressive_samples': 256, 'diffusion_iterations': 200},
        'high_quality': {'num_autoregressive_samples': 256, 'diffusion_iterations': 400},
    }

    # preset_args = presets[preset]

    # Hardcoded preset args for testing purposes
    preset_args = {'num_autoregressive_samples': 512, 'diffusion_iterations': 400}

    for j, text in enumerate(texts):
        audio_generator = tts.tts_stream(text, voice_samples=voice_samples, use_deterministic_seed=seed, temperature=0.2, **preset_args)
        # audio_generator = tts.tts_with_preset(text, preset=preset, voice_samples=voice_samples, use_deterministic_seed=seed)
        for wav_chunk in audio_generator:
            yield wav_chunk



def audio_stream_to_mp3(audio_stream):
    audio_tensor = torch.cat(list(audio_stream)).cpu()
    audio_np = audio_tensor.numpy()

    # torchaudio.save('/data/results/output.mp3', audio_tensor.unsqueeze(0), 24000)

    audio_data = io.BytesIO()
    sf.write(audio_data, audio_np, 24000, format='mp3')
    audio_data.seek(0)

    return audio_data



if not torch.cuda.is_available():
    print("!!! No CUDA device found, using CPU !!!")

use_deepspeed = os.environ.get('USE_DEEPSPEED', 'false').lower() == 'true'

if torch.backends.mps.is_available() and use_deepspeed:
    print("DeepSpeed is not compatible with MPS, disabling it.")
    use_deepspeed = False

print(f"Using DeepSpeed: {use_deepspeed}")

tts = TextToSpeech(models_dir=MODELS_DIR, use_deepspeed=use_deepspeed, kv_cache=True, half=True)


if __name__ == '__main__':
    port = os.environ.get('PORT', 6600)
    print(f"Running TTS server on port {port}")
    serve(app, host="0.0.0.0", port=port)