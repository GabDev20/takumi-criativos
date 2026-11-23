#!/usr/bin/env bash
# Junta a narração do ElevenLabs (voz/<nome>.mp3) ao vídeo, com a trilha abaixada (-17 dB) por baixo.
# Uso: bash src/mux_voz.sh   (rodar dentro de contagem/, com out/videos/voz/v1-quiz.mp3 etc.)
cd "$(dirname "$0")/../out/videos"
for v in v1-quiz v2-calendario v3-dezembro; do
  [ -f "voz/$v.mp3" ] || { echo "falta voz/$v.mp3"; continue; }
  ffmpeg -y -loglevel error -i "$v-sem-voz.mp4" -i "voz/$v.mp3" -i "$v-trilha.wav" \
    -filter_complex "[1:a]adelay=250|250,volume=1.0[vz];[2:a]volume=0.14[tr];[vz][tr]amix=inputs=2:duration=longest:normalize=0[a]" \
    -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest "$v.mp4" && echo "ok $v.mp4"
done
