import os
from time import time

from flask import Flask, request, Response, jsonify
from waitress import serve

from api import tts, convert
from utils import audio_to_mp3_stream

import logging
logger = logging.getLogger(__name__)

app = Flask(__name__)

SECRET_KEY = os.environ.get('SECRET_KEY', None)

def validate_secret():
    secret = request.headers.get('Authorization', None)
    if SECRET_KEY and secret != f'Bearer {SECRET_KEY}':
        return False
    return True

@app.route('/tts', methods=['POST'])
def api_tts():
    start_time = time()

    json = request.get_json()

    args = {
        'voice':            json.get('voice'),
        'text':             json.get('text'),
        'preset':           json.get('preset', 'standard'),
        'seed':             json.get('seed', None),
        'temperature':      json.get('temperature', 0.2),

        'use_rvc':          json.get('use_rvc', True),
        'method':           json.get('method', 'rmvpe'),
        'f0up_key':         json.get('f0up_key', 0),
        'index_rate':       json.get('index_rate', 0.0),
        'filter_radius':    json.get('filter_radius', 3),
        'resample':         json.get('resample', 48000),
        'rms_mix_rate':     json.get('rms_mix_rate', 0.25),
        'protect':          json.get('protect', 0.33),
    }
    
    logger.info(f"POST /tts voice={args.voice}, preset={args.preset}, seed={args.seed}")

    if not validate_secret():
        logger.error(f"403 Forbidden | Invalid secret key")
        return jsonify({'error': 'Invalid secret key'}), 403
    

    audio, sample_rate = tts(**args)
    mp3 = audio_to_mp3_stream(audio, sample_rate)

    end_time = time()
    logger.info(f"200 OK | {end_time - start_time:.2f}s")
    return Response(mp3, mimetype='audio/mp3')


@app.route('/convert', methods=['POST'])
def api_convert():
    start_time = time()

    json = request.get_json()

    args = {
        'voice':            json.get('voice'),
        'audio':            json.get('audio'),
        'method':           json.get('method', 'rmvpe'),
        'f0up_key':         json.get('f0up_key', 0),
        'index_rate':       json.get('index_rate', 0.0),
        'filter_radius':    json.get('filter_radius', 3),
        'resample':         json.get('resample', 48000),
        'rms_mix_rate':     json.get('rms_mix_rate', 0.25),
        'protect':          json.get('protect', 0.33),
    }
    
    logger.info(f"POST /convert voice={args.voice}, method={args.method}")

    if not validate_secret():
        logger.error(f"403 Forbidden | Invalid secret key")
        return jsonify({'error': 'Invalid secret key'}), 403

    audio, sample_rate = convert(**args)
    mp3 = audio_to_mp3_stream(audio, sample_rate)

    end_time = time()
    logger.info(f"200 OK | {end_time - start_time:.2f}s")
    return Response(mp3, mimetype='audio/mp3')


def start_server():
    port = os.environ.get('PORT', 6600)
    serve(app, host="0.0.0.0", port=port)