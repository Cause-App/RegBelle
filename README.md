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