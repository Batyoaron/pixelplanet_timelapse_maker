
import cv2
import os
import re

os.system("cls")




os.system("cls")
print(" \n \n \n \n \n")
print("If the window closed itself, your timelapse is ready, you can find it in, py files/")
print("wait until the program finishes")
print("dont close the window")
print("the video is now creating...")


def create_video_from_images(image_folder, output_path, fps):
    image_files = sorted(os.listdir(image_folder))
    image_files = [file for file in image_files if file.endswith('.png')]


    image_files = sorted(image_files, key=lambda x: int(re.findall('\d+', x)[0]))

    if len(image_files) == 0:
        print("No image files found in the specified folder.")
        return


    first_image_path = os.path.join(image_folder, image_files[0])
    first_image = cv2.imread(first_image_path)
    height, width, channels = first_image.shape


    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        image = cv2.imread(image_path)
        video_writer.write(image)

    video_writer.release()
    os.startfile("end.exe")
    cv2.destroyAllWindows()

image_folder = "images"

output_path = 'timelapse.mp4'
fps = 30

create_video_from_images(image_folder, output_path, fps)
