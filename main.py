from PIL import Image, ImageDraw, ImageFont
# from utils import generate_grid

WHITEBOARD_PATH = "assets/whiteboard.png"
FONT_PATH = "assets/font.ttf"
OUTPUT_PATH = "dist/"
GRID_SIZE = 50

COUNTER_PATH = "assets/counter.txt"

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
    for step in steps:
        while step:
            cut_step = cut_text_to_fit(step, 1000 - x_position, FONT_PATH, size)
            paint.text((x_position, y_position), cut_step, fill=(0, 0, 0), font=font)
            step = step[len(cut_step):]
            x_position = 390
            y_position += size 

    counter = str(count_one()).zfill(5)
    path = OUTPUT_PATH + f"croquis-{counter}.png"
    img.save(path)

    return path


generate_image(
    "Titulo de lo que sea",
    [
        "1. Que onda waxo",
        "2. Hello, im your friend :_d",
        "3. Oh la la, bonjour mon ami",
    ],
    (0, 0, 0),
    20
)