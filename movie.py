from moviepy.editor import *
from moviepy.audio.fx.volumex import volumex
from moviepy.video.fx.colorx import colorx
from moviepy.video.fx.crop import crop
import sys

FRAMES = 0

if len(sys.argv) > 1:
    FRAMES = int(sys.argv[1])

# Set up clips
print("Setting up clips, music and narrations...")
bgm = AudioFileClip("output\\bgm.mp3")
narrations = [AudioFileClip(f"output\\narration{i}.mp3") for i in range(1, FRAMES + 1)]
videos = [VideoFileClip(f"output\\video{i}.mp4") for i in range(1, FRAMES + 1)]

# Set up clips aspect ratio
print("Setting up clips aspect ratio...")
for i in range(len(videos)):
    videos[i] = videos[i].resize(height=1600)
    (w, h) = videos[i].size
    videos[i] = crop(videos[i], width=900, height=1600, x_center=w/2, y_center=h/2)
    videos[i].set_position(("center", "center"))
    videos[i] = colorx(videos[i], 0.7)

# Subclip narration clips to videos
print("Subclipping narration clips...")
for i in range(len(narrations)):
    video_duration = videos[i].duration
    narration_duration = narrations[i].duration
    if video_duration > narration_duration:
        videos[i] = videos[i].subclip(0, narration_duration + (2 if i == 0 else 0))

# Initiate loop at end
print("Subclipping for end-loop...")
videos[-1] = videos[-1].subclip(0, videos[-1].duration - 2)
videos.append(videos[0].subclip(0, 2))
videos[0] = videos[0].subclip(2, videos[0].duration)

# Add captions to videos
print("Adding captions to videos... [Cancelled]")
# total_txt = ""
# with open(f"output\\script.txt", "r", encoding="utf-8") as f:
#     total_txt = f.read()
# total_txt = total_txt.split("\n")
# total_txt = [x for x in total_txt if x != ""]
# for i in range(len(videos)):
#     current_txt = total_txt[i].split(" ")
#     current_txt = [x for x in current_txt if x != ""]
#     current_txt = [x for x in current_txt if x]
#     vtt = ""
#     with open(f"output\\narration{i+1}.mp3.vtt", "r", encoding="utf-8") as f:
#         vtt = f.read()
#     vtt = vtt.split("\n")
#     vtt = [x for x in vtt if x != ""]
#     words_done = 0
#     for j in range(len(vtt)):
#         if " --> " in vtt[j]:
#             timestamps = vtt[j].split(" --> ")
#             starttime = timestamps[0].split(":")
#             starttime_int = (int(starttime[0]) * 3600) + (int(starttime[1]) * 60) + float(starttime[2])
#             endtime = timestamps[1].split(":")
#             endtime_int = (int(endtime[0]) * 3600) + (int(endtime[1]) * 60) + float(endtime[2])
#             caption = (TextClip(current_txt[words_done], fontsize=100, color="white", font="Impact-Bold", stroke_color="black", stroke_width=5, align="center")
#                 .set_position(("center", 1000 if i == 0 else 750))
#                 .set_start(starttime_int)
#                 .set_duration(endtime_int - starttime_int))
#             videos[i] = CompositeVideoClip([videos[i], caption])
#             words_done += 1

# Add image clip to beginning of first video
print("Adding image clip to first video...")
icon = (ImageClip("output\\icon.png")
        .set_position(("center", "center"))
        .resize(height=300)
        .set_opacity(1)
        .set_duration(narrations[0].end)
        .set_start(0))
videos[0] = CompositeVideoClip([videos[0], icon])


# Concatenate videos into final clip
print("Concatenating videos...")
final_clip = concatenate_videoclips(videos)

# Set new resolution and crop to 9:16 aspect ratio
print("Setting new resolution and cropping to 9:16 aspect ratio...")
final_clip = final_clip.resize(height=1600)
final_clip = final_clip.crop(x1=0, y1=0, x2=900, y2=1600)

# Set background music
print("Setting background music...")
bgm = bgm.subclip(0, final_clip.end)
bgm = volumex(bgm, 0.08)

# Add outro text to last video
print("Adding outro text to last video...")
outro = (TextClip("CLICK THE LINK\nFOR MORE DETAILS", fontsize=50, color="yellow", font="Impact", stroke_color="black", stroke_width=3, align="center")
        .set_position(("center", 250))
        .set_start(final_clip.end - 3)
        .set_duration(3))
final_clip = CompositeVideoClip([final_clip, outro])

# Adding audio
print("Adding audio...")
narration = concatenate_audioclips([nar for nar in narrations])
plop_sound = AudioFileClip("output\\plop.wav")
confirm_sound = AudioFileClip("output\\confirm.wav")
whoosh_sound = AudioFileClip("output\\whoosh.wav")
final_audio = CompositeAudioClip([bgm.set_start(0), narration.set_start(0), whoosh_sound.set_start(narration.start), plop_sound.set_start(narration.start + whoosh_sound.duration), confirm_sound.set_start(narration.end - confirm_sound.duration)])

# Set final clip's audio
print("Setting final clip's audio...")
final_clip = final_clip.set_audio(final_audio)

# Adding tagline and logo
print("Adding tagline and logo...")
tagline = (ImageClip("output\\tagline.png")
        .set_position((50, 50))
        .resize(width=450)
        .set_opacity(1)
        .set_duration(final_clip.duration)
        .set_start(0))
final_clip = CompositeVideoClip([final_clip, tagline])
logo = (ImageClip("output\\logo.png")
        .set_position(("center", 1200))
        .resize(width=150)
        .set_opacity(0.65)
        .set_duration(final_clip.duration)
        .set_start(0))
final_clip = CompositeVideoClip([final_clip, logo])

final_clip = final_clip.resize(width=675, height=1200)

# Adding progress bar
print("Adding progress bar... [Cancelled]")
# duration = final_clip.duration
# screensize = (675, 1200)

# def resize_func(t):
#     data = (t / duration) * 675
#     if data <= 0: data = 1
#     if data >= 675: data = 674
#     return (data, 100)

# progress_bar = (
#     ImageClip("output\\progress-bar.png")
#     .resize(resize_func)
#     .set_position(0, 1100)
#     .set_duration(duration)
#     .set_fps(24)
# )

# final_clip = CompositeVideoClip(final_clip, progress_bar)

# Export video
print("Exporting video...")
final_clip.write_videofile("output\\video_out.mp4", threads=32, fps=24)
