from pathlib import Path
import re
import xml.etree.ElementTree as ET

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
NAME_SVG = HERE / "Santiago_vectorizado.svg"
OUTPUT = HERE / "Espalda_Santiago_54_vectorizada.svg"


def contours_to_path(mask: np.ndarray, epsilon: float = 0.65) -> str:
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    parts = []
    for contour in contours:
        if abs(cv2.contourArea(contour)) < 4:
            continue
        polygon = cv2.approxPolyDP(contour, epsilon, True).reshape(-1, 2)
        if len(polygon) < 3:
            continue
        commands = [f"M {polygon[0, 0]} {polygon[0, 1]}"]
        commands.extend(f"L {x} {y}" for x, y in polygon[1:])
        commands.append("Z")
        parts.append(" ".join(commands))
    return " ".join(parts)


# Reuse the previously approved Santiago vector curves, omitting its background.
root = ET.parse(NAME_SVG).getroot()
name_path = next(el.attrib["d"] for el in root if el.tag.endswith("path"))
view_box = [float(v) for v in root.attrib["viewBox"].split()]
name_w, name_h = view_box[2], view_box[3]

# Render bold athletic numerals only as an intermediate mask, then trace them.
font_candidates = [
    Path(r"C:\Windows\Fonts\arialbd.ttf"),
    Path(r"C:\Windows\Fonts\ariblk.ttf"),
]
font_path = next((p for p in font_candidates if p.exists()), None)
if font_path is None:
    raise SystemExit("No se encontró una fuente negrita del sistema")

font = ImageFont.truetype(str(font_path), 1250)
canvas = Image.new("L", (1800, 1500), 0)
draw = ImageDraw.Draw(canvas)
bbox = draw.textbbox((0, 0), "54", font=font, stroke_width=5)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
draw.text(
    ((1800 - tw) / 2 - bbox[0], (1500 - th) / 2 - bbox[1]),
    "54",
    font=font,
    fill=255,
    stroke_width=5,
    stroke_fill=255,
)
number_mask = np.array(canvas)
number_points = cv2.findNonZero(number_mask)
nx, ny, nw, nh = cv2.boundingRect(number_points)
number_crop = number_mask[ny : ny + nh, nx : nx + nw]
number_path = contours_to_path(number_crop)

page_w, page_h = 1800, 2400
name_target_w = 1600
name_scale = name_target_w / name_w
name_x = (page_w - name_w * name_scale) / 2
name_y = 170

number_target_w = 1120
number_scale_x = number_target_w / nw
# The reference jersey uses tall, dominant numerals. Preserve the current width
# while extending the glyphs vertically to match that football-shirt proportion.
number_scale_y = number_scale_x * 1.38
number_x = (page_w - nw * number_scale_x) / 2
number_y = 780

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="2400"
     viewBox="0 0 {page_w} {page_h}" role="img" aria-label="Santiago 54">
  <title>Diseño de espalda: Santiago 54</title>
  <rect width="100%" height="100%" fill="#ffffff"/>
  <g id="nombre" transform="translate({name_x:.3f} {name_y}) scale({name_scale:.8f})">
    <path d="{name_path}" fill="#000000" fill-rule="evenodd"/>
  </g>
  <g id="numero" transform="translate({number_x:.3f} {number_y}) scale({number_scale_x:.8f} {number_scale_y:.8f})">
    <path d="{number_path}" fill="#000000" fill-rule="evenodd"/>
  </g>
</svg>
'''
OUTPUT.write_text(svg, encoding="utf-8")
print(f"{OUTPUT}\nLienzo: {page_w} x {page_h}\nNombre y número convertidos a curvas")
