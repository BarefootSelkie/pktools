#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont

fontSize = 32

symbol = Image.new(mode="RGB", size=(32, 32), color=(255,255,255))
drawing = ImageDraw.Draw(symbol)

fontEmoji = ImageFont.truetype("./ttf/Noto_Emoji/static/NotoEmoji-Medium.ttf", fontSize)

drawing.text((1, 1), "A", fill = "black")

symbol.show()