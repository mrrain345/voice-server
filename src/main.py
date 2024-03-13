from tts_rest import infer, tts_infer_stream
from rvc_main import rvc_infer

import os
import torch
import soundfile as sf

def main():
    os.system("/app/src/download-models.sh")

    text = "Favorite anime character? Oh, someone who's a master of avoiding responsibilities - they're living my dream! Maybe one who can teleport out of awkward situations. I could use that skill during glitchy streams."
    voice = "nekora"
    preset = "standard"
    seed = None

    audio_stream = tts_infer_stream(text, voice, preset, seed)
    audio_tensor = torch.cat(list(audio_stream)).cpu()
    audio_np = audio_tensor.numpy()

    print(audio_np.shape)
    sf.write('/data/results/output-tts.mp3', audio_np, 24000, format='mp3')

    rvc_infer(audio_np)

if __name__ == "__main__":
    main()