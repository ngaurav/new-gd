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

# Font Variables
prominence_ranges = [0.75,0.5,0.3,0.2,0.15,0.1]
font_sizes = [1,0.6,0.35,0.2,0.15]
line_spacing = [40,20,10,6,4]
element_padding = [40,20,10,6,4]
font_factor = 48.0

class Grid(object):
    """ Helper class to encapsulate the grid properties of graphic
    """

    def __init__(self, cols, rows, width, height) -> None:
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.gutter_margin = round(height/40)
        vertical_padding = self.gutter_margin * 2
        horizontal_padding = round(width/cols/4)
        self.col_spacing = round((width-2*horizontal_padding)/cols)
        self.row_spacing = round((height-2*vertical_padding)/rows)
        self.vertical_padding = (height-self.row_spacing*rows)/2
        self.horizontal_padding = (width-self.col_spacing*cols)/2

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
                    if (len(buf) > 0):
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
        # print("font_size: ", font_size, " | max_size: ", max_size, " | min_size: ", min_size)
        font = font.font_variant(size=font_size)
        temp_image = Image.new('RGB', (int(max_size), int(canvas_height)), color='white')
        temp_draw = ImageDraw.Draw(temp_image)
        text_width = temp_draw.textlength(text, font=font)
        # print("text_width: ", text_width)
        if text_width >= max_size:
            # print ("condition 1")
            font_size = font_size * 0.8
        elif text_width <= min_size:
            # print ("condition 2")
            font_size = font_size * 1.25
        else:
            font_factor = font_size/font_sizes[priority-1]
            # print ("condition 3 ", font_factor)
            return font_size

def add_alignment(grid:Grid, groups):
    #TODO: Add 2 col, 1 row 
    #TODO: Add Long Posters (Insta Story), 4 corners and then large center block.
    if grid.rows == 1 and grid.cols == 1:
        for group in groups:
            col = group['col']
            row = group['row']
            for element in group['elements']:
                if col == 0 and row == 0:
                    element['alignment_x'] = 0
                    element['alignment_y'] = 0
    elif grid.rows == 2 and grid.cols == 2:
        for group in groups:
            col = group['col']
            row = group['row']
            for element in group['elements']:
                if col == 0 and row == 0:
                    element['alignment_x'] = 1
                    element['alignment_y'] = 1
                elif col == 0 and row == 1:
                    element['alignment_x'] = 1
                    element['alignment_y'] = -1
                elif col == 1 and row == 0:
                    element['alignment_x'] = -1
                    element['alignment_y'] = 1
                elif col == 1 and row == 1:
                    element['alignment_x'] = -1
                    element['alignment_y'] = -1
    elif grid.rows == 3 and grid.cols == 3:
        for group in groups:
            col = group['col']
            row = group['row']
            for element in group['elements']:
                if col == 0 and row == 0:
                    element['alignment_x'] = 1
                    element['alignment_y'] = 1
                elif col == 0 and row == 1:
                    element['alignment_x'] = 0
                    element['alignment_y'] = 1
                elif col == 0 and row == 2:
                    element['alignment_x'] = -1
                    element['alignment_y'] = 1
                elif col == 1 and row == 0:
                    element['alignment_x'] = 1
                    element['alignment_y'] = 0
                elif col == 1 and row == 1:
                    element['alignment_x'] = 0
                    element['alignment_y'] = 0
                elif col == 1 and row == 2:
                    element['alignment_x'] = -1
                    element['alignment_y'] = 0
                elif col == 2 and row == 0:
                    element['alignment_x'] = 1
                    element['alignment_y'] = -1
                elif col == 2 and row == 1:
                    element['alignment_x'] = 0
                    element['alignment_y'] = -1
                elif col == 2 and row == 2:
                    element['alignment_x'] = -1
                    element['alignment_y'] = -1
    else:
        for group in groups:
            for element in group['elements']:
                element['alignment_x'] = 1
                element['alignment_y'] = 1
    return groups


def draw(width, height, font:ImageFont, grid:Grid, groups):
    rows = grid.rows
    cols = grid.cols
    half_gutter_spacing = grid.gutter_margin/2
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    row_spacing = grid.row_spacing
    col_spacing = grid.col_spacing
    #TODO: Add space around logic (NOT NEEDED, DON'T DO)
    draw.line((0, height/2, width, height/2), fill="red", width=1)
    draw.line((width/2, 0, width/2, height), fill="red", width=1)
    for i in range(0, rows+1):
        draw.line((0, grid.vertical_padding + i * row_spacing - half_gutter_spacing, width, grid.vertical_padding + i * row_spacing - half_gutter_spacing), fill="black", width=2)
        draw.line((0, grid.vertical_padding + i * row_spacing + half_gutter_spacing, width, grid.vertical_padding + i * row_spacing + half_gutter_spacing), fill="black", width=2)

    for i in range(0, cols+1):
        draw.line((grid.horizontal_padding + i * col_spacing - half_gutter_spacing, 0, grid.horizontal_padding + i * col_spacing - half_gutter_spacing, height), fill="black", width=2)
        draw.line((grid.horizontal_padding + i * col_spacing + half_gutter_spacing, 0, grid.horizontal_padding + i * col_spacing + half_gutter_spacing, height), fill="black", width=2)

    for group in groups:
        elements = group['elements']
        for el in elements:
            update_font_factor(
                font=font,
                text=el['description'],
                priority=el['prominence'],
                canvas_height=height,
                canvas_width=width)
            
    groups = add_alignment(grid, groups)
    # TODO: Sort groups to put similar priority together in y-axis
    # TODO: Heirarchy (Rule of odds)
    # TODO: Hanging indent for bullets, quotes, etc.
    # TODO: Hanging indent for images.
    for group in groups:
        elements = group['elements']
        col = group['col']
        row = group['row']
        y_start = grid.vertical_padding + row * row_spacing + half_gutter_spacing
        y = y_start
        for i in range(len(elements)):
            prominence = elements[i]['prominence']
            text = elements[i]['description']
            ft = font.font_variant(size=font_sizes[prominence-1] * font_factor)
            ascent, descent = ft.getmetrics()
            (width, baseline), (offset_x, offset_y) = ft.font.getsize("A")
            line_height = ascent + descent
            y = y + element_padding[prominence-1]
            wrapper = TextWrapper(text, ft, col_spacing - 2 * half_gutter_spacing)
            wrapped_text = wrapper.wrapped_text()
            alignment_x = elements[i]['alignment_x']
            if alignment_x > 0:
                align = "left"
            elif alignment_x == 0:
                align = "center"
            else:
                align = "right"
            xy0, xy1, xy2, xy3 = draw.multiline_textbbox((0,0), wrapped_text, spacing=line_spacing[prominence-1], font=ft, align=align)
            if alignment_x > 0:
                x = grid.horizontal_padding + col * col_spacing + half_gutter_spacing
            elif alignment_x == 0:
                x = grid.horizontal_padding + (col + 0.5) * col_spacing - (xy2 - xy0)/2
            else:
                x = grid.horizontal_padding + (col+1) * col_spacing - half_gutter_spacing - (xy2 - xy0)
            elements[i]['x'] = x
            elements[i]['y'] = y
            elements[i]['text'] = wrapped_text
            elements[i]['align'] = align
            n_lines = wrapped_text.count("\n")+1
            # print(text, n_lines)
            new_y = y + n_lines*ascent + (n_lines-1)*line_spacing[prominence-1] + offset_y
            elements[i]['y_height'] = new_y - y
            y = new_y + element_padding[prominence-1]
            # y = y + xy3-xy1 +  0.5 * font_sizes[prominence-1] * font_factor
        for element in elements:
            prominence = element['prominence']
            ft = font.font_variant(size=font_sizes[prominence-1] * font_factor)
            alignment_y = element['alignment_y']
            if alignment_y > 0:
                y_delta = 0
            elif alignment_y == 0:
                y_delta = (row_spacing - 2*half_gutter_spacing - (y-y_start))/2
            elif alignment_y < 0:
                y_delta = row_spacing - 2*half_gutter_spacing - (y-y_start)
            draw.multiline_text(
                (element['x'], element['y']+y_delta),
                element['text'],
                spacing=line_spacing[prominence-1],
                fill="black",
                align=element['align'],
                font=ft)
            xy0, xy1, xy2, xy3 = draw.multiline_textbbox(
                (element['x'], element['y']+y_delta),
                element['text'],
                spacing=line_spacing[prominence-1],
                align=element['align'],
                font=ft)
            draw.rectangle((xy0, element['y']+y_delta, xy2, element['y']+y_delta+element['y_height']), outline='green')

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
        grid = Grid(
            height=step4_input['height'],
            width=step4_input['width'],
            cols=step4_input['grid']['cols'],
            rows=step4_input['grid']['rows']
        )
        img = draw(
            height=step4_input['height'],
            width=step4_input['width'],
            font=font,
            grid=grid,
            groups=step4_input['groups'])
        img.save(join(config['STEP4_OUTPUT_FOLDER'],f"{file}.png"))
        i = i + 1