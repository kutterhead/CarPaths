from pathlib import Path

import cv2
import numpy as np


SOURCE = Path(__file__).with_name("Santiago_fondo_blanco.png")
TARGET = Path(__file__).with_name("Santiago_vectorizado.svg")

image = cv2.imread(str(SOURCE), cv2.IMREAD_GRAYSCALE)
if image is None:
    raise SystemExit(f"No se pudo leer {SOURCE}")

# Separate the solid black lettering from the near-white generated background.
mask = np.where(image < 128, 255, 0).astype(np.uint8)
points = cv2.findNonZero(mask)
if points is None:
    raise SystemExit("No se detectaron trazos negros")

x, y, w, h = cv2.boundingRect(points)
margin = max(24, round(max(w, h) * 0.025))
x0 = max(0, x - margin)
y0 = max(0, y - margin)
x1 = min(mask.shape[1], x + w + margin)
y1 = min(mask.shape[0], y + h + margin)
cropped = mask[y0:y1, x0:x1]

contours, hierarchy = cv2.findContours(
    cropped, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
)
if hierarchy is None:
    raise SystemExit("No se pudieron construir contornos")

paths = []
for contour in contours:
    if abs(cv2.contourArea(contour)) < 2.0:
        continue
    simplified = cv2.approxPolyDP(contour, 0.45, True).reshape(-1, 2)
    if len(simplified) < 3:
        continue
    commands = [f"M {simplified[0, 0]} {simplified[0, 1]}"]
    commands.extend(f"L {px} {py}" for px, py in simplified[1:])
    commands.append("Z")
    paths.append(" ".join(commands))

width = x1 - x0
height = y1 - y0
svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"
     viewBox="0 0 {width} {height}" role="img" aria-label="Santiago">
  <title>Santiago</title>
  <rect width="100%" height="100%" fill="#ffffff"/>
  <path d="{' '.join(paths)}" fill="#000000" fill-rule="evenodd"/>
</svg>
'''
TARGET.write_text(svg, encoding="utf-8")
print(f"{TARGET}\nLienzo: {width} x {height}\nContornos: {len(paths)}")
