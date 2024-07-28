import cv2
import os
import shutil
import re
import time

def read_file_content(file_path, default_value):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Using default value '{default_value}'.")
        return default_value

namess = read_file_content("name", "output")
opath = read_file_content("outputpath.txt", os.path.join(os.path.expanduser('~'), 'Desktop'))

try:
    speed = float(read_file_content("speed", "30.0"))
except ValueError:
    print("Invalid speed value in file. Using default speed value of 30.0 fps.")
    speed = 30.0

os.system("cls" if os.name == "nt" else "clear")

def create_video_from_images(image_folder, output_path, fps):
    image_files = sorted([file for file in os.listdir(image_folder) if file.endswith('.png')])
    image_files = sorted(image_files, key=lambda x: int(re.findall(r'\d+', x)[0]))

    if len(image_files) == 0:
        print("No image files found in the specified folder.")
        return

    first_image_path = os.path.join(image_folder, image_files[0])
    first_image = cv2.imread(first_image_path)
    if first_image is None:
        print(f"Error reading the first image from {first_image_path}")
        return
    height, width, _ = first_image.shape


    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    start_time = time.time()
    total_images = len(image_files)
    os.system("cls" if os.name == "nt" else "clear")

    for index, image_file in enumerate(image_files):
        image_path = os.path.join(image_folder, image_file)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error reading image {image_path}")
            continue
        video_writer.write(image)
        elapsed_time = time.time() - start_time
        avg_time_per_image = elapsed_time / (index + 1)
        remaining_time = avg_time_per_image * (total_images - index - 1)
        print(f"\rProcessing image {index + 1}/{total_images}, estimated remaining time: {int(remaining_time)} seconds", end='')

    video_writer.release()
    cv2.destroyAllWindows()

    total_time = time.time() - start_time
    print(f"\nTimelapse creation completed in {total_time:.2f} seconds.")

image_folder = "images"
file_extension = '.mp4'
output_path = os.path.join(opath, namess + file_extension)

create_video_from_images(image_folder, output_path, speed)



output_path_modified = os.path.join(opath, namess + "_" + file_extension)
converter_command = output_path

f = open("convertercommand", "a")
f.write(converter_command)
f.close()

f = open("convertercommandsecond", "a")
f.write(output_path_modified) # we need the _ to work before the .mp4
f.close()

time.sleep(1)

fromm = "convertercommand"
to = "converterpart/"
shutil.move(fromm, to)

fromm = "convertercommandsecond"
to = "converterpart/"
shutil.move(fromm, to)

if os.path.isfile("outputpath.txt"):
    fromm = "outputpath.txt"
    to = "converterpart/"
    shutil.move(fromm, to)

if os.path.isfile("convertercommand"):
    os.remove("convertercommand")
    os.remove("convertercommandsecond")

shutil.rmtree('images')
os.mkdir("images")

os.chdir("converterpart")
os.startfile("converter.exe")

