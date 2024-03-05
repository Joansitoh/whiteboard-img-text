from PIL import Image, ImageDraw, ImageFont
import os
# from utils import generate_grid

WHITEBOARD_PATH = "assets/whiteboard.png"
FONT_PATH = "assets/font.ttf"
OUTPUT_PATH = "dist/"
GRID_SIZE = 50

COUNTER_PATH = "assets/counter.txt"


class Step:

    def __init__(self, title, image=None):
        self.title = title
        self.image = image

    def get_title(self):
        return self.title
    
    def get_image(self):
        return self.image

def get_font(size):
    if FONT_PATH:
        font = ImageFont.truetype(FONT_PATH, size)
    else:
        font = ImageFont.load_default()

    return font

def generate_grid(path, size):
    img = Image.open(path)
    draw = ImageDraw.Draw(img)
    
    for i in range(0, img.size[0], size):
        for j in range(0, img.size[1], size):
            draw.line([(i, 0), (i, img.size[1])], fill=(255, 255, 255))
            draw.line([(0, j), (img.size[0], j)], fill=(255, 255, 255))
            draw.text((i, j), f'({i}, {j})', fill=(0, 0, 0))
    
    img.save("grid.png")

def count_one():
    with open(COUNTER_PATH, "r") as file:
        counter = int(file.read())

    with open(COUNTER_PATH, "w") as file:
        file.write(str(counter + 1))

    return counter

def get_text_length(text, size):
    font = get_font(size)
    return font.getlength(text)

def cut_text_to_fit(text, max_width, font_path, font_size):
    font = ImageFont.truetype(font_path, font_size)
    cut_text = ""
    for char in text:
        if font.getlength(cut_text + char) > max_width:
            break
        cut_text += char
    return cut_text

def generate_image(message, steps, color=(0, 0, 0), size=20):
    img = Image.open(WHITEBOARD_PATH)
    paint = ImageDraw.Draw(img)
    font = get_font(size)

    x_position = 390
    
    if isinstance(message, list):
        y_position = 80
        for line in message:
            paint.text((x_position, y_position), line, fill=color, font=font)
            y_position += size
    else:
        paint.text((x_position, 75), message, fill=color, font=font)
    
    y_position = 150

    x_image_pos = 460
    y_image_pos = 300
    image_pos_up = False
    for step in steps:
        while step.get_title():
            cut_step = cut_text_to_fit(step.get_title(), 1000 - x_position, FONT_PATH, size)
            paint.text((x_position, y_position), cut_step, fill=(0, 0, 0), font=font)
            step_title = step.get_title()[len(cut_step):]
            step = Step(step_title, step.get_image())
            x_position = 390
            y_position += size 

        if step.get_image():
            print(step.get_image())
            step_img = Image.open(step.get_image())

            if step_img.size[0] > 200:
                step_img = step_img.resize((200, int(step_img.size[1] * (200 / step_img.size[0]))))

            img.paste(step_img, (x_image_pos, y_image_pos)) 

            image_pos_up = not image_pos_up
            x_image_pos += step_img.size[0] - 40
            if image_pos_up:
                y_image_pos += step_img.size[1] + 20
            else:
                y_image_pos -= step_img.size[1] + 20

    counter = str(count_one()).zfill(5)
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    path = OUTPUT_PATH + f"croquis-{counter}.png"
    img.save(path)

    return path

generate_image(
    "Titulo de lo que sea",
    [
        Step("1. Que onda waxo", "assets/1.png"),
        Step("2. Hello, im your friend :_d", "assets/1.png"),
        Step("3. Oh la la, bonjour mon ami", "assets/1.png"),
    ],
    (0, 0, 0),
    20
)