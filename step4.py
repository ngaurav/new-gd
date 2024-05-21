import shutil
from utils import askgpt, getjson
from step2_prompts import step2_system_prompt
import json, os
import subprocess
from PIL import Image, ImageDraw, ImageFont
from os import listdir
from os.path import isfile, join

with open('config.json', 'r') as f:
    config = json.load(f)

prominence_ranges = [0.75,0.5,0.3,0.2,0.15,0.1]
font_sizes = [1,0.6,0.35,0.2,0.15]
spacing = [40,20,10,6,4]
font_factor = 48.0

from PIL import Image, ImageDraw

class TextWrapper(object):
    """ Helper class to wrap text in lines, based on given text, font
        and max allowed line width.
    """

    def __init__(self, text, font, max_width):
        self.text = text
        self.text_lines = [
            ' '.join([w.strip() for w in l.split(' ') if w])
            for l in text.split('\n')
            if l
        ]
        self.font = font
        self.max_width = max_width

        self.draw = ImageDraw.Draw(
            Image.new(
                mode='RGB',
                size=(100, 100)
            )
        )

        self.space_width = self.draw.textlength(
            text=' ',
            font=self.font
        )

    def get_text_width(self, text):
        return self.draw.textlength(
            text=text,
            font=self.font
        )

    def wrapped_text(self):
        wrapped_lines = []
        buf = []
        buf_width = 0

        for line in self.text_lines:
            for word in line.split(' '):
                word_width = self.get_text_width(word)

                expected_width = word_width if not buf else \
                    buf_width + self.space_width + word_width

                if expected_width <= self.max_width:
                    # word fits in line
                    buf_width = expected_width
                    buf.append(word)
                else:
                    # word doesn't fit in line
                    wrapped_lines.append(' '.join(buf))
                    buf = [word]
                    buf_width = word_width

            if buf:
                wrapped_lines.append(' '.join(buf))
                buf = []
                buf_width = 0

        return '\n'.join(wrapped_lines)

def update_font_factor(font, text, priority, canvas_width, canvas_height):
    global font_sizes, font_factor, prominence_ranges
    font_size = font_sizes[priority-1] * font_factor
    max_size = canvas_width * prominence_ranges[priority-1]
    min_size = canvas_width * prominence_ranges[priority]
    while min_size < max_size:
        print("font_size: ", font_size, " | max_size: ", max_size, " | min_size: ", min_size)
        font = font.font_variant(size=font_size)
        temp_image = Image.new('RGB', (int(max_size), int(canvas_height)), color='white')
        temp_draw = ImageDraw.Draw(temp_image)
        text_width = temp_draw.textlength(text, font=font)
        print("text_width: ", text_width)
        if text_width >= max_size:
            print ("condition 1")
            font_size = font_size * 0.8
        elif text_width <= min_size:
            print ("condition 2")
            font_size = font_size * 1.25
        else:
            font_factor = font_size/font_sizes[priority-1]
            print ("condition 3 ", font_factor)
            return font_size
        
def draw(width, height, elements, font):
    rows = 3
    cols = 3
    half_gutter_spacing = 10
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    row_spacing = height // rows
    col_spacing = width // cols
    for i in range(1, rows):
        draw.line((0, i * row_spacing - half_gutter_spacing, width, i * row_spacing - half_gutter_spacing), fill="black", width=2)
        draw.line((0, i * row_spacing + half_gutter_spacing, width, i * row_spacing + half_gutter_spacing), fill="black", width=2)

    for i in range(1, cols):
        draw.line((i * col_spacing - half_gutter_spacing, 0, i * col_spacing - half_gutter_spacing, height), fill="black", width=2)
        draw.line((i * col_spacing + half_gutter_spacing, 0, i * col_spacing + half_gutter_spacing, height), fill="black", width=2)

    cols = [0,0,0,1,1,1,2,2,2]
    rows = [0,1,2,0,1,2,0,1,2]
    for i in range(len(elements)):
        col = cols[i]
        row = rows[i]
        text = elements[i]['description']
        print(text)
        text_position = (col * col_spacing + half_gutter_spacing, row * row_spacing + half_gutter_spacing)
        priority = elements[i]['prominence']
        ft = font.font_variant(size=font_sizes[priority-1] * font_factor)
        # to test multiline support remove the comment in the following line 
        max_width = prominence_ranges[priority-1] * width # * 0.8
        wrapper = TextWrapper(text, ft, max_width)
        wrapped_text = wrapper.wrapped_text()
        draw.multiline_text(text_position, wrapped_text, spacing=spacing[priority-1], fill="black", font=ft)    
    return image


if __name__ == "__main__":
    output_folder = os.path.join(config['STEP4_OUTPUT_FOLDER'])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    font_path = "Arial.ttf"
    font = ImageFont.truetype(font_path, size=1)
    mypath = config['STEP4_INPUT_FOLDER']
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    i = 0
    for file in onlyfiles:
        with open(join(config['STEP4_INPUT_FOLDER'],file), 'r') as f:
            step4_input = json.load(f)
        for el in step4_input['elements']:
            update_font_factor(font=font, text=el['description'], priority=el['prominence'], canvas_height=step4_input['height'], canvas_width=step4_input['width'])
        img = draw(height=step4_input['height'], width=step4_input['width'], elements=step4_input['elements'],font=font)
        img.save(join(config['STEP4_OUTPUT_FOLDER'],f"{i}.png"))