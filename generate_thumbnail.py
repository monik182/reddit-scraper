from PIL import Image, ImageDraw, ImageFont
import textwrap


def generate_thumbnail(text, image_path, output_path):
    image = Image.open(image_path).convert('RGBA')
    font_size = 60
    font = ImageFont.load_default(font_size) 

    text_overlay = Image.new('RGBA', image.size, (255, 255, 255, 0)) 

    draw = ImageDraw.Draw(text_overlay)

    bbox = draw.textbbox((0, 0), text, font=font)

    image_width, image_height = image.size

    wrapped_text = []
    for line in text.split('\n'):
        wrapped_text.extend(textwrap.fill(line, width=40).split('\n'))

    bbox1 = draw.textbbox((0,0),"Test", font=font)
    line_height = bbox1[3] - bbox1[1]
    line_spacing = line_height * 1.4

    total_text_height = line_height * len(wrapped_text)
    y_position = max((image_height - total_text_height) *3 / 5, 0)

    text_color = (0, 0, 0, 255) 
    for line in wrapped_text:
        bbox = draw.textbbox((0,0),line, font=font)
        line_width = bbox[2] - bbox[0]
        x_position = (image_width - line_width) / 2
        draw.text((x_position, y_position), line, font=font, fill=text_color)
        y_position += line_spacing

    combined = Image.alpha_composite(image, text_overlay)

    combined.save(output_path, format='PNG')
