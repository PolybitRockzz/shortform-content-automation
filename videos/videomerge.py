from moviepy.editor import *
import json
import os
import subprocess

if __name__ == "__main__":
    print("[1] Merge all videos in .\\videos directory to video_merged.mp4")
    print("[2] De-merge video_merged.mp4 to .\\videos directory")
    print("[3] Fix video files in .\\videos directory")
    print("[3] Exit")

    choice = int(input("Enter your choice: "))

    if choice == 4:
        exit()
    if choice == 1:
        videos = []
        txtFile = open("merge_data.txt", "w")
        for file in os.listdir("."):
            if file.endswith(".mp4"):
                txtFile.write("file '" + file + "'\n")
        #         videos.append(VideoFileClip(os.path.join("videos", file)))
        #         videos.append(VideoFileClip(os.path.join("videos", file)))
        # write a json file merge_data.json with filename, start time and end time with respect to total merged video
        with open("merge_data.json", "w") as f:
            json.dump([], f)
        with open("merge_data.json", "r") as f:
            data = json.load(f)
        total_time = 0
        for i in range(0, len(videos)):
            data.append({"filename": videos[i].filename, "start": int(total_time + videos[i].start), "end": int(total_time + videos[i].end)})
            total_time += videos[i].duration
        with open("merge_data.json", "w") as f:
            json.dump(data, f)
        # final_video = concatenate_videoclips(videos)
        # final_video.write_videofile("video_merged.mp4")
        result = subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "merge_data.txt", "-c", "copy", "mergedfile.mp4"], capture_output=True, text=True)
        print("Video merged successfully!")
    if choice == 2:
        video = VideoFileClip("video_merged.mp4")
        with open("merge_data.json", "r") as f:
            data = json.load(f)
        for i in range(0, len(data)):
            video.subclip(data[i]["start"], data[i]["end"]).write_videofile("NEW_" + data[i]["filename"])
        print("Video de-merged successfully!")
    if choice == 3:
        for file in os.listdir("."):
            if file.endswith(".mp4"):
                subprocess.run(["ffmpeg", "-i", file, file.substring[:len(file)-3 + "avi"]], capture_output=True, text=True)
                subprocess.run(["ffmpeg", "-i", file.substring[:len(file)-3 + "avi", file]], capture_output=True, text=True)
        print("Video files fixed successfully!")