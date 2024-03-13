# Voice Server

This is a simple TTS server that combines [TorToiSe](https://github.com/neonbjb/tortoise-tts) with [RVC](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI).



## Installation

```bash
git clone https://github.com/mrrain345/voice-server.git
cd voice-server
git submodule update --init --recursive
./run.sh build
./run.sh run
```



## API Endpoints

### POST `/tts`

#### Request

```ts
{
  // TTS options
  voice: string,
  text: string,
  preset?: 'ultra_fast' | 'fast' | 'standard' | 'high_quality' = 'standard',
  seed?: number | null = null,
  temperature?: number = 0.2,

  // RVC options
  use_rvc?: boolean = true,
  method?: "pm" | "harvest" | "crepe" | "rmvpe" = "rmvpe",
  f0up_key?: number = 0,
  index_rate?: number = 0.0,
  filter_radius?: number = 3,
  resample?: number = 48000,
  rms_mix_rate?: number = 0.25,
  protect?: number = 0.33
}
```

#### Response

`audio/mp3 stream`



### POST `/convert`

#### Request

```ts
{
  voice: string,
  audio: string, // base64 encoded
  method?: "pm" | "harvest" | "crepe" | "rmvpe" = "harvest",
  f0up_key?: number = 0,
  index_rate?: number = 0.0,
  filter_radius?: number = 3,
  resample?: number = 48000,
  rms_mix_rate?: number = 0.25,
  protect?: number = 0.33
}
```

#### Response

`audio/mp3 stream`