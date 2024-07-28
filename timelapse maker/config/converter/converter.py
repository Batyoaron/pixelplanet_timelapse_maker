from moviepy.editor import VideoFileClip
import os

try:
    with open("convertercommand", 'r') as file:
        convertercommand = file.read()
except FileNotFoundError:
    print(f"File not found.")


try:
    with open("convertercommandsecond", 'r') as file: #this contains the _.mp4
        convertercommandsecond = file.read()
except FileNotFoundError:
    print(f"File not found.")




input_file = convertercommand
output_file = convertercommandsecond


clip = VideoFileClip(input_file)


clip.write_videofile(output_file, codec='libx264', preset='fast', ffmpeg_params=['-crf', '23'])
os.startfile("end.exe")

