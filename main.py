from tkinter import Tk
from tkinter.filedialog import askopenfilename

def choose_file():
    Tk().withdraw()
    filename = askopenfilename(title="Choose your main MP4 clip", filetypes=[("Video files", "*.mp4"), ("All files", "*.*")])
    return filename

if __name__ == '__main__':
    mainclip = choose_file()
    if mainclip == "": exit()
    