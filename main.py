from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import subprocess
import threading

app = FastAPI()

#TEST
# Global subprocess and pipe
audio_pipe = None
audio_lock = threading.Lock()

def start_ffmpeg_loop():
    global audio_pipe
    if audio_pipe is None:
        ffmpeg_cmd = [
            "ffmpeg",
            "-stream_loop", "-1",  # 🔁 infinite loop dsds
            "-re",                 # simulate real-time
            "-i", "music.mp3",        # your audio file
            "-f", "mp3",
            "-"
        ]
        
        audio_pipe = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE)

def audio_generator():
    print("Playibg")
    global audio_pipe
    while True:
        with audio_lock:
            chunk = audio_pipe.stdout.read(1024)
        if not chunk:
            break
        yield chunk

@app.on_event("startup")
def startup_event():
    start_ffmpeg_loop()

@app.get("/live")
def stream_audio():
    return StreamingResponse(audio_generator(), media_type="audio/mpeg")
