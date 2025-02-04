"""
Comic Panel Generator with Text Overlay
Maintains original functionality while improving code structure and readability
"""

import cv2
import math
import textwrap
from PIL import Image, ImageOps
from typing import List, Tuple

# Constants for maintainability
TEXT_WRAP_WIDTH = 54
DIALOG_HEIGHT_FACTOR = 0.06
FONT_SCALE_FACTOR = 0.4
BASE_WIDTH = 272
PADDING_FACTOR = 10/362
LINE_SPACING_FACTOR = 17.5/362
BORDER_THICKNESS_MULTIPLIER = 6
LINE_THICKNESS_MULTIPLIER = 3

COLORS = {
    'text_box': (239, 239, 239),
    'border': (0, 0, 0),
    'narrator_box': (140, 238, 255)
}

FONT_CONFIG = cv2.FONT_HERSHEY_SIMPLEX | cv2.FONT_ITALIC

def calculate_text_dimensions(text: str, image_width: int) -> Tuple[int, int]:
    """Calculate required dimensions for text container"""
    row_count = math.ceil(len(text) / TEXT_WRAP_WIDTH)
    text_height = math.ceil(image_width * DIALOG_HEIGHT_FACTOR * row_count)
    return row_count, text_height

def add_dialog_panel(image_path: str, dialog_text: str) -> int:
    """
    Add text panel to bottom of image
    Returns height of added text panel
    """
    # Image preparation
    pil_img = Image.open(image_path)
    width, height = pil_img.size
    
    # Calculate text dimensions
    _, dialog_height = calculate_text_dimensions(dialog_text, width)
    
    # Create expanded image with text space
    expanded_img = ImageOps.expand(
        pil_img, 
        border=(0, dialog_height, 0, 0), 
        fill=COLORS['border']
    )
    expanded_img.save('temp.png')
    
    # OpenCV processing
    cv_img = cv2.imread('temp.png')
    font_scale = FONT_SCALE_FACTOR * width / BASE_WIDTH * 2/3
    font_thickness = math.floor(width / BASE_WIDTH * 2/3)
    
    # Draw text container
    cv2.rectangle(
        cv_img, 
        (0, 0), 
        (width, dialog_height),
        COLORS['text_box'], 
        -1
    )
    
    # Add borders
    cv2.rectangle(
        cv_img,
        (0, 0),
        (cv_img.shape[1], cv_img.shape[0]),
        COLORS['border'],
        font_thickness * BORDER_THICKNESS_MULTIPLIER
    )
    
    # Add separator line
    cv2.line(
        cv_img,
        (0, dialog_height),
        (cv_img.shape[1], dialog_height),
        COLORS['border'],
        font_thickness * LINE_THICKNESS_MULTIPLIER
    )
    
    # Wrap and position text
    wrapped_text = textwrap.wrap(dialog_text, width=TEXT_WRAP_WIDTH)
    for i, line in enumerate(wrapped_text):
        text_size = cv2.getTextSize(line, FONT_CONFIG, font_scale, font_thickness)[0]
        y_position = int(width * LINE_SPACING_FACTOR + i * (text_size[1] + int(width * PADDING_FACTOR)))
        x_position = int(height * PADDING_FACTOR)
        
        cv2.putText(
            cv_img, line, 
            (x_position, y_position), 
            FONT_CONFIG, font_scale, 
            COLORS['border'], font_thickness, 
            lineType=cv2.LINE_AA
        )
    
    cv2.imwrite("dialog_panel.png", cv_img)
    return dialog_height

def prepare_narrator_section(image_path: str, text: str) -> Tuple[int, List[str], int]:
    """Prepare dimensions and wrapped text for narrator section"""
    pil_img = Image.open(image_path)
    width, height = pil_img.size
    
    _, text_height = calculate_text_dimensions(text, width)
    wrapped_text = textwrap.wrap(text, width=TEXT_WRAP_WIDTH)
    
    return height - text_height, wrapped_text, text_height

def create_composite_panel(panel_data: List[List[str]]):
    """Main function to create composite comic panel"""
    # Setup base image
    narrator_data = prepare_narrator_section("plain_sheet.png", panel_data[0][0])
    base_height, wrapped_text, text_height = narrator_data
    
    page = cv2.imread("plain_sheet.png")
    middle_y = base_height // 2
    panel_coordinates = [
        [middle_y - 585, 50],
        [middle_y - 585, 830],
        [middle_y + 5, 50],
        [middle_y + 5, 830]
    ]
    
    # Configure text parameters
    page_width = 1653
    font_scale = FONT_SCALE_FACTOR * page_width / BASE_WIDTH * 2/3
    font_thickness = math.floor(page_width / BASE_WIDTH * 2/3)
    
    # Draw narrator section
    cv2.rectangle(
        page,
        (50, 595 + middle_y),
        (page_width - 50, 595 + middle_y + text_height),
        COLORS['narrator_box'], 
        -1
    )
    
    # Add narrator text
    for i, line in enumerate(wrapped_text):
        text_size = cv2.getTextSize(line, FONT_CONFIG, font_scale, font_thickness)[0]
        y_pos = middle_y + 590 + int(page_width * LINE_SPACING_FACTOR + i * (
            text_size[1] + int(page_width * PADDING_FACTOR)))
        x_pos = int(base_height * PADDING_FACTOR)
        
        cv2.putText(
            page, line, 
            (x_pos, y_pos), 
            FONT_CONFIG, font_scale, 
            COLORS['border'], font_thickness, 
            lineType=cv2.LINE_AA
        )
    
    # Add comic panels
    for idx, (coord, panel_info) in enumerate(zip(panel_coordinates, panel_data[1:])):
        panel_img = cv2.imread(panel_info[0])
        processed_height = int(panel_img.shape[0] * 0.75)
        
        # Process individual panel
        cv2.imwrite("temp_panel.png", panel_img)
        panel_height = add_dialog_panel("temp_panel.png", panel_info[1])
        
        final_panel = cv2.imread("dialog_panel.png")
        final_panel = cv2.resize(final_panel[:processed_height, :], (773, 580))
        
        # Add panel to composite image
        page[
            coord[0]:coord[0] + final_panel.shape[0],
            coord[1]:coord[1] + final_panel.shape[1]
        ] = final_panel
    
    cv2.imwrite("sheet_output.png", page)

# Example usage
create_composite_panel([
    ["¡Hala Madrid!...y nada más is the popular anthem of Spanish football club Real Madrid..."],
    ["image_1.png", "CORNER TAKEN QUICKLY... ORIGI!"],
    ["image_2.png", "ROMA HAVE RISEN FROM THEIR RUINS! MANOLAS!"],
    ["image_3.png", "AND SOLSJKAER HAS WON IT!"],
    ["image_4.png", "LOVELY CUSHIONED HEADER FOR GERRARD! OH YOU BEAUTY! WHAT A HIT, SON!"]
])
