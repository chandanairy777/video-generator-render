import numpy as np
from moviepy.editor import *
from moviepy.video.fx.all import loop
import random, datetime

# Config
frequencies = [396, 417, 528, 639, 741, 852]
video_styles = ["gradient", "moving_circle", "solid"]
clip_duration = 3      # base loop
final_minutes = 1      # default video length
size = (1280, 720)     # resolution

def generate_video(minutes: int = final_minutes):
    # ---- Randomize ----
    frequency = random.choice(frequencies)
    style = random.choice(video_styles)
    color1 = tuple(np.random.randint(0,256,3))
    color2 = tuple(np.random.randint(0,256,3))

    # ---- Audio (sine wave) ----
    sr = 44100
    t = np.linspace(0, clip_duration, int(sr*clip_duration), endpoint=False)
    audio_data = 0.1 * np.sin(2*np.pi*frequency*t)
    audio_clip = AudioArrayClip(audio_data.reshape((-1,1)), fps=sr)

    # ---- Video ----
    if style == "gradient":
        def make_frame(t):
            return np.tile(
                np.linspace(color1, color2, size[0], dtype=int),
                (size[1],1,1)
            )
        clip = VideoClip(make_frame, duration=clip_duration)
    elif style == "moving_circle":
        def make_frame(t):
            frame = np.zeros((size[1], size[0], 3), dtype=np.uint8)
            x = int(size[0]/2 + np.sin(t*2*np.pi/clip_duration)*100)
            y = size[1]//2
            rr, cc = np.ogrid[:size[1], :size[0]]
            mask = (rr - y)**2 + (cc - x)**2 <= 100**2
            frame[mask] = color1
            return frame
        clip = VideoClip(make_frame, duration=clip_duration)
    else:
        clip = ColorClip(size=size, color=color1).set_duration(clip_duration)

    clip = clip.set_audio(audio_clip)

    # ---- Loop to final length ----
    final_clip = loop(clip, duration=minutes*60)

    # ---- Save file ----
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"meditation_{frequency}Hz_{style}_{timestamp}.mp4"
    final_clip.write_videofile(filename, fps=30)

    return filename, frequency, style
