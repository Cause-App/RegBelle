# RegBelle

A somewhat automated animation engine

## Gentle

Run gentle with
```bash
docker run -p 8765:8765 lowerquality/gentle
```

and then receive transcript with
```bash
curl -F "audio=@PATH_TO_AUDIO_FILE" -F "transcript=@PATH_TO_TRANSCRIPT" "http://localhost:8765/transcriptions?async=false"
```

## FFMpeg

Stitch:

```bash
ffmpeg -i PATH_TO_FRAMES/%07d.png -c:v libx264 -vf fps=FRAMERATE -pix_fmt yuv420p silent.mp4
```

Add audio:

```bash
ffmpeg -i silent.mp4 -i audio.wav -c:v copy -map 0:v:0 -map 1:a:0 -c:a aac -b:a 192k output.mp4
```

## JSONS

Dummy "pose change" character is `~`