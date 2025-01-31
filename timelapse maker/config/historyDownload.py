#!/usr/bin/python3

import sys
import io
import os
import datetime
import asyncio
import aiohttp
import json
import PIL.Image
import time

def generate_progress_bar(percentage, bar_length=20):
    filled_length = int(bar_length * percentage // 100)
    bar = "■" * filled_length + " " * (bar_length - filled_length)
    return f"[{bar}] {percentage:.2f}%"

semaphore = asyncio.Semaphore(500)


f = open("detectcrash_image_downloader.txt", "a")
f.close()

try:
    with open("name", 'r') as file:
        nametimelapse = file.read()
except FileNotFoundError:
    print("File 'name' not found.")
    sys.exit(1)

try:
    with open("days", 'r') as file:
        daysss = int(file.read().strip())
except FileNotFoundError:
    print("File 'days' not found.")
    sys.exit(1)

try:
    with open("date", 'r') as file:
        dateee = file.read()
except FileNotFoundError:
    print("File 'date' not found.")
    sys.exit(1)

frameskip = 1

canvases = [
    {
        "canvas_name": "earth",
        "canvas_size": 256 * 256,
        "canvas_id": 0,
        "bkg": (202, 227, 255),
    },
    {
        "canvas_name": "moon",
        "canvas_size": 16384,
        "canvas_id": 1,
        "bkg": (49, 46, 47),
        "historical_sizes": [
            ["20210417", 4096],
        ]
    },
    {},
    {
        "canvas_name": "corona",
        "canvas_size": 256,
        "canvas_id": 3,
        "bkg": (33, 28, 15),
    },
    {
        "canvas_name": "compass",
        "canvas_size": 1024,
        "canvas_id": 4,
        "bkg": (196, 196, 196),
    },
    {},
    {},
    {
        "canvas_name": "1bit",
        "canvas_size": 256 * 256,
        "canvas_id": 7,
        "bkg": (0, 0, 0),
    },
]

os.system("cls")
print(" [I] Program needs to prepare for long time, the time of the preparation will take like 2-7 minutes\n but its depending on the time distance you gave the program \n \n Ignore the error under this message \n \n")

async def fetch(session, url, offx, offy, image, bkg, needed=False):
    attempts = 0
    while True:
        try:
            async with session.get(url) as resp:
                if resp.status == 404:
                    if needed:
                        img = PIL.Image.new('RGB', (256, 256), color=bkg)
                        image.paste(img, (offx, offy))
                        img.close()
                    return
                if resp.status != 200:
                    if needed:
                        continue
                    return
                data = await resp.read()
                img = PIL.Image.open(io.BytesIO(data)).convert('RGBA')
                image.paste(img, (offx, offy), img)
                img.close()
                return
        except:
            if attempts > 3:
                raise
            attempts += 1
            pass

async def calculate_total_images(canvas, start_date, end_date):
    canvas_data = canvases[canvas]
    canvas_id = canvas_data["canvas_id"]
    delta = datetime.timedelta(days=1)
    total_images = 0
    temp_date = start_date

    while temp_date <= end_date:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://pixelplanet.fun/history?day=%s&id=%s' % (temp_date.strftime("%Y%m%d"), canvas_id)) as resp:
                try:
                    time_list = json.loads(await resp.text())
                    total_images += len(time_list)
                except:
                    print('Couldn\'t decode json for day %s, trying again' % (temp_date.strftime("%Y%m%d")))
        temp_date += delta

    if total_images == 0:
        total_images = 1  

    return total_images

async def get_area(canvas, x, y, w, h, start_date, end_date):
    canvas_data = canvases[canvas]
    canvas_id = canvas_data["canvas_id"]
    canvas_size = canvas_data["canvas_size"]
    bkg = canvas_data["bkg"]

    delta = datetime.timedelta(days=1)
    end_date_str = end_date.strftime("%Y%m%d")
    iter_date = None
    day = 0
    cnt = 0
    previous_day = PIL.Image.new('RGB', (w, h), color=bkg)
    
    total_images = await calculate_total_images(canvas, start_date, end_date)

    import time
    start_time = time.time()

    while iter_date != end_date_str:
        iter_date = start_date.strftime("%Y%m%d")
        start_date = start_date + delta

        fetch_canvas_size = canvas_size
        if 'historical_sizes' in canvas_data:
            for ts in canvas_data['historical_sizes']:
                date = ts[0]
                size = ts[1]
                if iter_date <= date:
                    fetch_canvas_size = size

        offset = int(-fetch_canvas_size / 2)
        xc = (x - offset) // 256
        wc = (x + w - offset) // 256
        yc = (y - offset) // 256
        hc = (y + h - offset) // 256

        tasks = []
        async with aiohttp.ClientSession() as session:
            image = PIL.Image.new('RGBA', (w, h))
            for iy in range(yc, hc + 1):
                for ix in range(xc, wc + 1):
                    url = 'https://storage.pixelplanet.fun/%s/%s/%s/%s/tiles/%s/%s.png' % (
                    iter_date[0:4], iter_date[4:6], iter_date[6:], canvas_id, ix, iy)
                    offx = ix * 256 + offset - x
                    offy = iy * 256 + offset - y
                    tasks.append(fetch(session, url, offx, offy, image, bkg, True))
            await asyncio.gather(*tasks)

            day += 1
            days_left = daysss - day

            clr = image.getcolors(1)
            if clr is not None:
                print("Got faulty full-backup frame, using last frame from previous day instead.")
                image = previous_day.copy()
            cnt += 1
            image.save('./images/t%s.png' % (cnt))
            while True:
                async with session.get('https://pixelplanet.fun/history?day=%s&id=%s' % (iter_date, canvas_id)) as resp:
                    try:
                        time_list = json.loads(await resp.text())
                        break
                    except:
                        print('Couldn\'t decode json for day %s, trying again' % (iter_date))
            i = 0
            for time in time_list:
                i += 1
                if (i % frameskip) != 0:
                    continue
                if time == '0000':
                    continue
                tasks = []
                image_rel = image.copy()
                for iy in range(yc, hc + 1):
                    for ix in range(xc, wc + 1):
                        url = 'https://storage.pixelplanet.fun/%s/%s/%s/%s/%s/%s/%s.png' % (
                        iter_date[0:4], iter_date[4:6], iter_date[6:], canvas_id, time, ix, iy)
                        offx = ix * 256 + offset - x
                        offy = iy * 256 + offset - y
                        tasks.append(fetch(session, url, offx, offy, image_rel, bkg))

                await asyncio.gather(*tasks)
                cnt += 1
                percentage = (cnt / total_images) * 100
                import time
                elapsed_time = time.time() - start_time
                
                if cnt > 0:
                    average_time_per_image = elapsed_time / cnt
                    estimated_remaining_time = average_time_per_image * (total_images - cnt)
                else:
                    estimated_remaining_time = 0


                hours = int(estimated_remaining_time // 3600)
                minutes = int((estimated_remaining_time % 3600) // 60)
                seconds = int(estimated_remaining_time % 60)
                



                os.system("cls")
                print(" [N] Project name: " , nametimelapse)
                print(" [I] Images downloading  |    Image: ", cnt, "/", total_images ," |   Day: ", day, "/", daysss, "   | Days left: ", days_left)
                print(" [P] Progress: ", generate_progress_bar(percentage))
                if percentage >= 10:
                    print(" [T] Estimated time remaining: %02d:%02d:%02d" % (hours, minutes, seconds))
                else:
                    print(" [T] Calculating estimated remaining time...")
                print(dateee)





                image_rel.save('./images/t%s.png' % (cnt))
                if time == time_list[-1]:
                    previous_day.close()
                    previous_day = image_rel.copy()
                image_rel.close()
            image.close()
    previous_day.close()

if __name__ == "__main__":
    if len(sys.argv) != 5 and len(sys.argv) != 6:
        print("Run the launcher.exe")
    else:
        canvas = int(sys.argv[1])
        start = sys.argv[2].split('_')
        end = sys.argv[3].split('_')
        start_date = datetime.date.fromisoformat(sys.argv[4])
        if len(sys.argv) == 6:
            end_date = datetime.date.fromisoformat(sys.argv[5])
        else:
            end_date = datetime.date.today()
        x = int(start[0])
        y = int(start[1])
        w = int(end[0]) - x + 1
        h = int(end[1]) - y + 1
        loop = asyncio.get_event_loop()
        if not os.path.exists('./images'):
            os.mkdir('./images')
        loop.run_until_complete(get_area(canvas, x, y, w, h, start_date, end_date))


os.remove("detectcrash_image_downloader.txt")
os.startfile("main.exe")
