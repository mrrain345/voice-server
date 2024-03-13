FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /app

ARG RVC_BRANCH=v2.2

VOLUME [ "/data" ]
RUN mkdir -p /data/{models,tts_voices,rvc_voices}

# Main environment variables
ENV SECRET_KEY="secret"
ENV PORT=6600

# TorToiSe environment variables
ENV TORTOISE_MODELS_DIR="/data/models"
ENV USE_DEEPSPEED="false"
ENV PYTHONPATH="/app/src:/app/rvc:$PYTHONPATH"

# RVC environment variables
ENV OPENBLAS_NUM_THREADS="1"
ENV no_proxy="localhost, 127.0.0.1, ::1"

ENV weight_root="/data/voices"
ENV index_root="/data/voices"
ENV weight_uvr5_root="/data/models/uvr5_weights"
ENV outside_index_root="/data/models/indices"
ENV rmvpe_root="/data/models/rmvpe"


RUN apt update
RUN apt install -y wget git ffmpeg aria2

RUN mkdir -p /root/.cache/huggingface && ln -s "${TORTOISE_MODELS_DIR}" "/root/.cache/huggingface/hub"

ADD rvc /app/rvc
RUN pip install -r /app/rvc/requirements.txt

ADD tortoise_tts /app/tortoise_tts
RUN pip install -e /app/tortoise_tts

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD src /app/src

ENTRYPOINT ["python3", "/app/src/main.py"]