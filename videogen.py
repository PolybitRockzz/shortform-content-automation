import sys
import subprocess
import json
import random
import os
import shutil
import edge_tts
import asyncio
import datetime

TYPE = None
SUBTYPE = None
FRAMES = 0

def init():
    global TYPE
    global FRAMES
    TYPE = sys.argv[1] if len(sys.argv) > 1 else "finance"
    SUBTYPE = ""
    FRAMES = int(0)

def random_script():
    global SUBTYPE
    print("Fetching random script...")
    f = open(f"scripts\\{TYPE}.json", "r")
    data = json.load(f)
    hashtags = ""
    with open(f"scripts\\{TYPE}.hashtags.txt", "r", encoding="utf-8") as f:
        hashtags = f.read()
    lines = []
    intrnd1 = random.randint(0, len(data)-1)
    SUBTYPE = data[intrnd1]["type"]
    intrnd2 = random.randint(0, len(data[intrnd1]["content"]))-1
    script = data[intrnd1]["content"][intrnd2].replace(". ", ".\n").replace("? ", "?\n").replace("! ", "!\n").replace(": ", ":\n")
    lines.extend(script.split("\n"))
    lines = [x for x in lines if x != ""]
    with open("output\\script.txt", "w", encoding="utf-8") as f:
        f.write(script + "\n\n" + hashtags)
    print("Random script fetched. --> [", SUBTYPE, "]")
    data[intrnd1]["content"].pop(intrnd2)
    with open(f"scripts\\{TYPE}.json", "w") as f:
        json.dump(data, f, indent=2)
    return lines
    
async def generate_narration(text, file, number, total) -> None:
    if number == 1:
        print("Generating narrations...")
    narrator = ""
    if TYPE == "health":
        narrator = "en-GB-RyanNeural"
    elif TYPE == "finance":
        narrator = "en-US-ChristopherNeural"
    elif TYPE == "relationship":
        narrator = "en-GB-SoniaNeural"
    communicate = edge_tts.Communicate(text, narrator)
    submaker = edge_tts.SubMaker()
    with open(file, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
    with open(file + ".vtt", "w", encoding="utf-8") as f:
        f.write(submaker.generate_subs())
    print("Narration (" + str(number)  + "/" + str(total) + ") generated.")
    if number == total:
        print("All narrations generated.")

def random_b_roll():
    print("Fetching B-roll...")
    stock_vids = os.listdir("stock")
    stock_vids = [f for f in stock_vids if TYPE in f]
    stock_vids.sort()
    selected_vids = []
    selection_vids = [f for f in stock_vids if SUBTYPE in f]
    related = 3 if len(selection_vids) >= 3 else len(selection_vids)
    print("Related videos --> " + str(related))
    selected_vids.extend(random.sample(selection_vids, related))
    selection_vids = [f for f in stock_vids if f not in selected_vids]
    selected_vids.extend(random.sample(selection_vids, FRAMES - related))
    print("Random videos --> " + str(FRAMES - related))
    for i, file in enumerate(selected_vids):
        new_file_name = "video" + str(i+1) + ".mp4"
        shutil.copy(f"stock\\{file}", f"output\\{new_file_name}")
    print("B-roll fetched.")

def random_music():
    print("Fetching music...")
    music = os.listdir("music")
    music = [f for f in music if TYPE in f]
    music.sort()
    selected_music = random.sample(music, 1)
    for i, file in enumerate(selected_music):
        new_file_name = "bgm.mp3"
        shutil.copy(f"music\\{file}", f"output\\{new_file_name}")
    print("Music fetched.")

def copy_otherfiles():
    print("Copying accessory files files...")
    shutil.copy("fx\\plop.wav", "output\\plop.wav")
    shutil.copy("fx\\confirm.wav", "output\\confirm.wav")
    shutil.copy("fx\\whoosh.wav", "output\\whoosh.wav")
    shutil.copy(f"fx\\{TYPE}.png", "output\\tagline.png")
    shutil.copy(f"fx\\{TYPE}-logo.png", "output\\logo.png")
    shutil.copy(f"fx\\{TYPE}-progress-bar.png", "output\\progress-bar.png")
    shutil.copy(f"fx\\{SUBTYPE}.png", "output\\icon.png")

def generate_video(vidno):
    print("Generating video...")
    subprocess.run(["python", "movie.py", str(FRAMES)])
    print("Video generated.")
    shutil.copy(f"output\\video_out.mp4", f"videos\\{TYPE}_{str(vidno)}_{datetime.datetime.now().strftime('%d-%m-%y_%H-%M')}.mp4")
    shutil.copy(f"output\\script.txt", f"videos\\{TYPE}_{str(vidno)}_{datetime.datetime.now().strftime('%d-%m-%y_%H-%M')}.txt")
    for file_name in os.listdir("output"):
        os.remove(f"output\\{file_name}")

def main(vidno):
    global FRAMES
    for file_name in os.listdir("output"):
        os.remove(f"output\\{file_name}")
    lines = random_script()
    for line in lines:
        asyncio.get_event_loop().run_until_complete(generate_narration(line, f"output\\narration{FRAMES+1}.mp3", FRAMES+1, len(lines)))
        FRAMES += 1
    random_b_roll()
    random_music()
    copy_otherfiles()
    generate_video(vidno)

if __name__ == "__main__":
    x = 0
    if len(sys.argv) > 2:
        x = int(sys.argv[2])
    else:
        x = int(input("How many videos? "))
    for i in range(x):
        print("\n\nVideo (" + str(i+1) + ")\n\n")
        init()
        main(i+1)