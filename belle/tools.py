import cv2
import numpy as np
from PIL import Image
from cairosvg import svg2png
from io import BytesIO

def confirm(prompt, default=0, options=["y", "n"]):
    answer = None
    options = list(x.lower() for x in options)
    upperOptions = list(x.lower() for x in options)
    upperOptions[default] = upperOptions[default].upper()
    while not answer in options:
        answer = input(f"{prompt} ({'/'.join(upperOptions)}) ").lower()
        if answer == "":
            answer = options[default]

    return answer

cache = {}
size_cache = {}
def load_image(path, width, height, scale=None, interpolation=cv2.INTER_AREA):
    if path not in cache:
        assert width is not None or height is not None or scale is not None
        if path.endswith(".svg"):
            with open(path, "rb") as file:
                png = svg2png(bytestring=file.read())

            pil_img = Image.open(BytesIO(png)).convert('RGBA')
            img = np.array(pil_img)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        else:
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        cache[path] = img
        size_cache[path] = {}
    img = cache[path]
    im_height, im_width, _ = img.shape
    if scale is None:
        aspect = im_width/im_height
        if width is None:
            width = round(height * aspect)
        if height is None:
            height = round(width / aspect)

        scale = [height/im_height, width/im_width]
    else:
        width = round(im_width*scale[0])
        height = round(im_height*scale[1])
    size_cache_key = f"{width},{height}"
    if size_cache_key not in size_cache[path]:
        img = cv2.resize(img, (width, height), interpolation=interpolation)
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        size_cache[path][size_cache_key] = img

    return size_cache[path][size_cache_key]

def overlay_image(base, overlay, x, y):
    base_height, base_width, _ = base.shape
    height, width, channels = overlay.shape
    if channels == 3:
        overlay = cv2.cvtColor(overlay, cv2.COLOR_RGB2RGBA)

    y1, y2 = y, y+height
    x1, x2 = x, x+width

    if x1 >= base_width or x2 < 0 or y1 >= base_height or y2 < 0:
        return

    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(base_width, x2)
    y2 = min(base_height, y2)

    cropX1 = x1 - x
    cropY1 = y1 - y
    cropX2 = x2 - x
    cropY2 = y2 - y
    
    cropped = overlay[cropY1:cropY2, cropX1:cropX2]
    
    overlay_alpha = cropped[:, :, 3] / 255.0
    inverted_alpha = 1.0 - overlay_alpha

    for c in range(3):
        base[y1:y2, x1:x2, c] = (
            overlay_alpha * cropped[:, :, c] +
            inverted_alpha * base[y1:y2, x1:x2, c]
        )

mouth_types = {
    "openVowels": [
        "ah", "ih", "ey", "iy", "eh", "uh", "ay", "aa", "ae", "er"
    ],
    "y,l": [
        "l", "y"
    ],
    "oo,r": [
        "ao", "r", "ow", "uw", "aw", "oov", "oy"
    ],
    "m,p,b": [
        "b", "m", "p"
    ],
    "f,v": [
        "v", "f"
    ],
    "d,g,k,th": [
        "k", "d", "t", "ng", "n", "z", "sh", "dh", "w", "s", "g", "hh", "th", "jh", "ch", "zh"
    ]
}

def phone_to_mouth_type(phone):
    if phone is not None:
        p = phone.split("_")[0]
        for i in mouth_types:
            if p in mouth_types[i]:
                return i
        print(f"Warning. Phoneme not found: ${phone}")
        return "d,g,k,th"
    
    return "m,p,b"

def line_break(x, on, newline="\n"):
    return f"{on}{newline}".join(x.split(on))
