import os
from time import time

from flask import Flask, request, Response, jsonify

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
        print(f"403 Forbidden | Invalid secret key", flush=True)
        return jsonify({'error': 'Invalid secret key'}), 403

    error = api_validate(voice, text, preset, seed)
    if error:
        print(f"400 Bad Request | {error['error']}", flush=True)
        return jsonify(error), 400
    

    mp3_data = infer(text, voice, preset, seed)

    end_time = time()
    print(f"200 OK | {end_time - start_time:.2f}s", flush=True)
    return Response(mp3_data, mimetype='audio/mp3')


PRESETS = ['ultra_fast', 'fast', 'standard', 'high_quality']

def api_validate(voice, text, preset, seed):
    errors = {}
    voice_dir = os.path.join(TORTOISE_VOICES_DIR, voice)
    
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