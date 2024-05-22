import cv2
import os
import re
import time

import os

desktop = os.path.join(os.path.expanduser('~'), 'Desktop')


def create_video_from_images(image_folder, output_path, fps):
    image_files = sorted(os.listdir(image_folder))
    image_files = [file for file in image_files if file.endswith('.png')]

    image_files = sorted(image_files, key=lambda x: int(re.findall('\d+', x)[0]))

    if len(image_files) == 0:
        print("No image files found in the specified folder.")
        return

    first_image_path = os.path.join(image_folder, image_files[0])
    first_image = cv2.imread(first_image_path)
    if first_image is None:
        print(f"Error reading the first image from {first_image_path}")
        return
    height, width, channels = first_image.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))


    start_time = time.time()
    total_images = len(image_files)
    


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

try:
    with open("speed", 'r') as file:
        speed = float(file.read().strip())
except FileNotFoundError:
    print("Speed file not found. Using default speed value of 30.0 fps.")
    speed = 30.0
except ValueError:
    print("Invalid speed value in file. Using default speed value of 30.0 fps.")
    speed = 30.0

image_folder = "images"
output_path = os.path.join(desktop, 'timelapse.mp4')

create_video_from_images(image_folder, output_path, speed)

os.startfile("end.exe")
