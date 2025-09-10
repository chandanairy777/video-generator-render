from fastapi import FastAPI
import generate_video

app = FastAPI()

@app.get("/")
def root():
    return {"status": "running", "message": "Meditation Video Generator API"}

@app.get("/generate")
def generate(minutes: int = 1):
    filename, freq, style = generate_video.generate_video(minutes)
    return {
        "status": "success",
        "file": filename,
        "frequency": freq,
        "style": style
    }
