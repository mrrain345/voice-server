#!/bin/sh

# [ -f /data/models/pretrained_v2/D40k.pth ] || aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained_v2/D40k.pth -d /data/models/pretrained_v2/ -o D40k.pth
# [ -f /data/models/pretrained_v2/G40k.pth ] || aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained_v2/G40k.pth -d /data/models/pretrained_v2/ -o G40k.pth
# [ -f /data/models/pretrained_v2/f0D40k.pth ] || aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained_v2/f0D40k.pth -d /data/models/pretrained_v2/ -o f0D40k.pth
# [ -f /data/models/pretrained_v2/f0G40k.pth ] || aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained_v2/f0G40k.pth -d /data/models/pretrained_v2/ -o f0G40k.pth

# [ -f /data/models/uvr5_weights/HP2-人声vocals+非人声instrumentals.pth ] || aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/uvr5_weights/HP2-人声vocals+非人声instrumentals.pth -d /data/models/uvr5_weights/ -o HP2-人声vocals+非人声instrumentals.pth
# [ -f /data/models/uvr5_weights/HP5-主旋律人声vocals+其他instrumentals.pth ] || aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/uvr5_weights/HP5-主旋律人声vocals+其他instrumentals.pth -d /data/models/uvr5_weights/ -o HP5-主旋律人声vocals+其他instrumentals.pth

[ -f /data/models/hubert/hubert_base.pt ] || aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/hubert_base.pt -d /data/models/hubert -o hubert_base.pt

[ -f /data/models/rmvpe/rmvpe.pt ] || aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/rmvpe.pt -d /data/models/rmvpe -o rmvpe.pt