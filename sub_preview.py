from moviepy.editor import TextClip
import moviepy.editor as mp
from PIL import Image


def preview_subtitle_old(text, output_image_path):
    width = 1080
    height = 1920

    subtitle_clip = mp.TextClip(
        text,
        font='Impact',
        fontsize=70,
        color='white',
        stroke_color='black',
        stroke_width=4,
        size=(width, None),
        method='caption',
        align='center'
    )

    background = Image.new("RGB", (width, height), "black")

    subtitle_clip = subtitle_clip.set_position(('center', 'center')).set_duration(1)
    frame = subtitle_clip.get_frame(0)
    subtitle_image = Image.fromarray(frame)

    background.paste(subtitle_image, (0, (height - subtitle_clip.size[1]) // 2), subtitle_image)

    background.save(output_image_path)


def preview_subtitle(text, output_image_path):
    width = 1080
    height = 1920

    subtitle_clip = mp.TextClip(
        text,
        font='Helvetica-Bold',
        fontsize=70,
        color='white',
        stroke_color='black',
        stroke_width=4,
        align='center',
        kerning=2,
    )

    background = Image.new("RGB", (width, height), "red")

    subtitle_clip = subtitle_clip.set_position(('center', 'center')).set_duration(1)
    frame = subtitle_clip.get_frame(0)
    subtitle_image = Image.fromarray(frame)

    subtitle_rgb = subtitle_image.convert("RGB")
    subtitle_alpha = subtitle_image.split()[-1]

    background.paste(subtitle_rgb, (0, (height - subtitle_clip.size[1]) // 2), subtitle_alpha)

    background.save(output_image_path)


preview_subtitle("chat gpt saved my life and", "subtitle_preview.png")
