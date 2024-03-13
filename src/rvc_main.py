import os
import sys

# now_dir = os.getcwd()
# sys.path.append(now_dir)

from scipy.io import wavfile

from rvc.configs.config import Config
from vc.modules import VC

def rvc_infer(audio):
    args = {
        "f0up_key": 0,
        # "input_path": "/data/results/input.wav",
        "index_path": "/data/rvc_voices/nekora/added_IVF310_Flat_nprobe_1_nekora_v2.index",
        "f0method": "harvest",
        "opt_path": "/data/results/output.wav",
        "model_name": "nekora/nekora.pth",
        "index_rate": 0.0,
        # "device": "cuda:0",
        # "is_half": True,
        "filter_radius": 3,
        "resample_sr": 48000,
        "rms_mix_rate": 0.25,
        "protect": 0.33,
    }

    config = Config()
    # config.device = args.device if args.device else config.device
    # config.is_half = args.is_half if args.is_half else config.is_half
    vc = VC(config)
    vc.get_vc(args['model_name'])

    print('RVC inference...')

    _, wav_opt = vc.vc_single(
        0,
        # args['input_path'],
        audio,
        args['f0up_key'],
        None,
        args['f0method'],
        args['index_path'],
        None,
        args['index_rate'],
        args['filter_radius'],
        args['resample_sr'],
        args['rms_mix_rate'],
        args['protect'],
    )

    print(wav_opt)
    wavfile.write(args['opt_path'], wav_opt[0], wav_opt[1])