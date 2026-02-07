import argparse
from PIL import Image, ImageDraw, ImageFont


def add_corners(im, rad=50, bg=True, bgCol=(255, 255, 255), bgPix=5):
    bg_im = Image.new("RGB", tuple(x + (bgPix * 2) for x in im.size), bgCol)
    ims = [im if not bg else im, bg_im]
    circle = Image.new("L", (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    for i in ims:
        alpha = Image.new("L", i.size, "white")
        w, h = i.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        i.putalpha(alpha)
    bg_im.paste(im, (bgPix, bgPix), im)
    return im if not bg else bg_im


def resize(image: Image.Image, base_width: int) -> Image.Image:
    wpercent = base_width / float(image.size[0])
    hsize = int((float(image.size[1]) * float(wpercent)))
    return image.resize((base_width, hsize), Image.Resampling.LANCZOS)


parser = argparse.ArgumentParser(description="Iphone Music Player Creator")

parser.add_argument("--title", type=str, help="track title")
parser.add_argument("--artist", type=str, help="track artist")
parser.add_argument("--start-time", type=str, help="start time for progress bar")
parser.add_argument("--remaining-time", type=str, help="remaining time for progress bar")
parser.add_argument("--cover", type=str, help="path to music cover image")

args = parser.parse_args()

template = Image.open("template.png")
cover = Image.open(args.cover)
title = args.title
artists = args.artist

start_time = args.start_time
remaining_time = '-' + args.remaining_time


template_cover_coords = ((34, 63), (592, 620))
template_width, template_height = template.size
cover_width, cover_height = cover.size

cover = add_corners(cover, rad=50, bg=False)

base_width = template_cover_coords[1][0] - template_cover_coords[0][0]

cover = resize(cover, base_width)

# (cover_width//2 - template_width//2, template_cover_coords[0][1])
template.paste(cover, template_cover_coords[0], mask=cover)


draw = ImageDraw.Draw(template)
# font = ImageFont.truetype(<font-file>, <font-size>)
song_title = ImageFont.truetype(
    font=r"C:\\Users\\Rohit\\AppData\\Local\\Microsoft\\Windows\\Fonts\\SFPRODISPLAYBOLD.OTF",
    size=35,
)
song_artist = ImageFont.truetype(
    font=r"C:\\Users\\Rohit\\AppData\\Local\\Microsoft\\Windows\\Fonts\\SFPRODISPLAYMEDIUM.OTF",
    size=24,
)
song_time = ImageFont.truetype(
    font=r"C:\\Users\\Rohit\\AppData\\Local\\Microsoft\\Windows\\Fonts\\SFPRODISPLAYREGULAR.OTF",
    size=21,
)

# placing song title text
draw.text((template_cover_coords[0][0], 650), title, (255, 255, 255), font=song_title)

draw.text((template_cover_coords[0][0], 700), artists, (104, 104, 104), font=song_artist)

# 36, 793 -> start time pos
# 535, 793 -> remaining time pos

draw.text((36, 790), start_time, (255, 255, 255), font=song_time)
draw.text((535, 790), remaining_time, (255, 255, 255), font=song_time)

template.save("output.png")