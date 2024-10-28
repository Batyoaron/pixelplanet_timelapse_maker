import PIL.Image
import sys, os, io, math
import asyncio
import aiohttp
import subprocess
import threading
import msvcrt

try:
    with open("name", 'r') as file:
        nametimelapse = file.read()
except FileNotFoundError:
    print("File 'name' not found.")
    sys.exit(1)

try:
    with open("rate", 'r') as file:
        rate = file.read()
except FileNotFoundError:
    print("File 'rate' not found.")
    sys.exit(1)

rate_int = int(rate)
os.system("cls")

USER_AGENT = "ppfun areaDownload 1.0 " + ' '.join(sys.argv[1:])
PPFUN_URL = "https://pixelplanet.fun"

class Color(object):
    def __init__(self, index, rgb):
        self.rgb = rgb
        self.index = index

class EnumColorPixelplanet:
    ENUM = []

    def getColors(canvas):
        colors = canvas['colors']
        for i, color in enumerate(colors):
            EnumColorPixelplanet.ENUM.append(Color(i, tuple(color)))
    
    @staticmethod
    def index(i):
        for color in EnumColorPixelplanet.ENUM:
            if i == color.index:
                return color
        return EnumColorPixelplanet.ENUM[0]

class Matrix:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.width = None
        self.height = None
        self.matrix = {}

    def add_coords(self, x, y, w, h):
        if self.start_x is None or self.start_x > x:
            self.start_x = x
        if self.start_y is None or self.start_y > y:
            self.start_y = y
        end_x_a = x + w
        end_y_a = y + h
        if self.width is None or self.height is None:
            self.width = w
            self.height = h
        else:
            end_x_b = self.start_x + self.width
            end_y_b = self.start_y + self.height
            self.width = max(end_x_b, end_x_a) - self.start_x
            self.height = max(end_y_b, end_y_a) - self.start_y

    def create_image(self, filename=None):
        img = PIL.Image.new('RGBA', (self.width, self.height), (255, 0, 0, 0))
        pxls = img.load()
        for x in range(self.width):
            for y in range(self.height):
                try:
                    color = self.matrix[x + self.start_x][y + self.start_y].rgb
                    pxls[x, y] = color
                except (IndexError, KeyError, AttributeError):
                    pass
        if filename is not None:
            img.save(filename)
        else:
            img.show()
        img.close()

    def set_pixel(self, x, y, color):
        if x >= self.start_x and x < (self.start_x + self.width) and y >= self.start_y and y < (self.start_y + self.height):
            if x not in self.matrix:
                self.matrix[x] = {}
            self.matrix[x][y] = color

async def fetchMe():
    url = f"{PPFUN_URL}/api/me"
    headers = {
        'User-Agent': USER_AGENT
    }
    async with aiohttp.ClientSession() as session:
        attempts = 0
        while True:
            try:
                async with session.get(url, headers=headers) as resp:
                    data = await resp.json()
                    return data
            except:
                if attempts > 3:
                    print(f" [X] Could not get {url} in three tries, cancelling")
                    raise
                attempts += 1
                print(f" [X] Failed to load {url}, trying again in 5s ~ Bad server")
                await asyncio.sleep(5)
                pass

async def fetch(session, canvas_id, canvasoffset, ix, iy, target_matrix):
    url = f"{PPFUN_URL}/chunks/{canvas_id}/{ix}/{iy}.bmp"
    headers = {
        'User-Agent': USER_AGENT
    }
    attempts = 0
    while True:
        try:
            async with session.get(url, headers=headers) as resp:
                data = await resp.read()
                offset = int(-canvasoffset * canvasoffset / 2)
                off_x = ix * 256 + offset
                off_y = iy * 256 + offset
                if len(data) == 0:
                    clr = EnumColorPixelplanet.index(0)
                    for i in range(256*256):
                        tx = off_x + i % 256 
                        ty = off_y + i // 256
                        target_matrix.set_pixel(tx, ty, clr)
                else:
                    i = 0
                    for b in data:
                        tx = off_x + i % 256
                        ty = off_y + i // 256
                        bcl = b & 0x7F
                        target_matrix.set_pixel(tx, ty, EnumColorPixelplanet.index(bcl))
                        i += 1
                break
        except:
            if attempts > 3:
                print(f" [X] Could not get {url} in three tries, cancelling")
                raise
            attempts += 1
            print(f" [X] Failed to load {url}, trying again in 3s ~ Bad server")
            await asyncio.sleep(3)
            pass

async def get_area(canvas_id, canvas, x, y, w, h):
    target_matrix = Matrix()
    target_matrix.add_coords(x, y, w, h)
    canvasoffset = math.pow(canvas['size'], 0.5)
    offset = int(-canvasoffset * canvasoffset / 2)
    xc = (x - offset) // 256
    wc = (x + w - offset) // 256
    yc = (y - offset) // 256
    hc = (y + h - offset) // 256
    tasks = []
    async with aiohttp.ClientSession() as session:
        for iy in range(yc, hc + 1):
            for ix in range(xc, wc + 1):
                tasks.append(fetch(session, canvas_id, canvasoffset, ix, iy, target_matrix))
        await asyncio.gather(*tasks)
        return target_matrix

def validateCoorRange(ulcoor: str, brcoor: str, canvasSize: int):
    if not ulcoor or not brcoor:
        return "Not all coordinates defined"
    splitCoords = ulcoor.strip().split('_')
    if not len(splitCoords) == 2:
        return "Invalid Coordinate Format for top-left corner"
    
    x, y = map(lambda z: int(math.floor(float(z))), splitCoords)

    splitCoords = brcoor.strip().split('_')
    if not len(splitCoords) == 2:
        return "Invalid Coordinate Format for bottom-right corner"
    u, v = map(lambda z: int(math.floor(float(z))), splitCoords)
    
    if (u < x or v < y):
        return "Corner coordinates are aligned wrong"

    canvasMaxXY = canvasSize / 2
    canvasMinXY = -canvasMaxXY
    
    if (x < canvasMinXY or y < canvasMinXY or x >= canvasMaxXY or y >= canvasMaxXY):
        return "Coordinates of top-left corner are outside of canvas"
    if (u < canvasMinXY or v < canvasMinXY or u >= canvasMaxXY or v >= canvasMaxXY):
        return "Coordinates of bottom-right corner are outside of canvas"
    
    return (x, y, u, v)

def listen_for_escape(stop_flag):
    while not stop_flag.is_set():
        if msvcrt.kbhit() and ord(msvcrt.getch()) == 27:  # ESC key is pressed
            stop_flag.set()
            os.startfile("main.exe")
            sys.exit()
            exit()
            break

async def main():
    if len(sys.argv) != 4:
        return

    canvas_id = sys.argv[1]
    top_left = sys.argv[2]
    bottom_right = sys.argv[3]

    apime = await fetchMe()

    if canvas_id not in apime['canvases']:
        print("Invalid canvas selected")
        return

    canvas = apime['canvases'][canvas_id]

    if 'v' in canvas and canvas['v']:
        print("Can't get area for 3D canvas")
        return

    parseCoords = validateCoorRange(top_left, bottom_right, canvas['size'])

    if isinstance(parseCoords, str):
        print(parseCoords)
        sys.exit()
    else:
        x, y, w, h = parseCoords
        w = w - x + 1
        h = h - y + 1

    EnumColorPixelplanet.getColors(canvas)

    if not os.path.exists("images"):
        os.makedirs("images")

    stop_flag = threading.Event()
    listener_thread = threading.Thread(target=listen_for_escape, args=(stop_flag,))
    listener_thread.start()

    count = 1
    try:
        while not stop_flag.is_set():
            matrix = await get_area(canvas_id, canvas, x, y, w, h)
            filename = os.path.join("images", f"{count}.png")
            matrix.create_image(filename)
            os.system("cls")
            print("\n [N] Project name: ", nametimelapse)
            print(f" [C] Image {count} saved!")
            print(" [R] Images/seconds: ", rate)
            print(" \n [I] Stop by Pressing ESC")
            count += 1
            await asyncio.sleep(rate_int)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        stop_flag.set()
        listener_thread.join()
        print("\nCapture stopped by user")
        sys.exit()

if __name__ == "__main__":
    asyncio.run(main())
