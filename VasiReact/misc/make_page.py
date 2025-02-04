import cv2, math, textwrap, os
from PIL import Image, ImageOps

def add_text(image_path: str, dialog_text: str):
    img = Image.open(image_path)
    width, height = img.size
    dialog_rows = math.ceil(float(len(dialog_text) / 24))
    dialog_ht = math.ceil(float(width * 0.06 * dialog_rows))
    tl = 0, 0
    br = (int(width), dialog_ht)
    bordered = ImageOps.expand(img, border=(0,dialog_ht,0,0), fill=(0,0,0))
    bordered.save('temp.png')
    img = cv2.imread('temp.png')
    font_size = (0.4 * width / 272 * 2 / 3)
    font_thickness = math.floor(width / 272 * 2 / 3)
    cv2.rectangle(img, tl, br, (239, 239, 239), -1)
    cv2.rectangle(img, (0, 0), (img.shape[1], img.shape[0]), (0, 0, 0), font_thickness * 6)
    cv2.line(img, (0, int(dialog_ht)), (img.shape[1], int(dialog_ht)), (0, 0, 0), font_thickness * 3)
    wrapped_dialog = textwrap.wrap(dialog_text, width = 54)
    font =  cv2.FONT_HERSHEY_SIMPLEX | cv2.FONT_ITALIC
    for i, line in enumerate(wrapped_dialog):   
        textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]
        gap = textsize[1] + int(width * 10 / 362)
        y = int((width * 17.5 / 362) + i * (gap))
        x = int(int(height * 10 / 362))
        cv2.putText(img, line, (x, y), font, font_size, (0,0,0), font_thickness, lineType = cv2.LINE_AA)
    cv2.imwrite("dialog_panel.png", img)
    return dialog_ht

def add_narrator_text(image_path: str, dialog_text: str):
    img = Image.open(image_path)
    width, height = img.size
    dialog_rows = math.ceil(float(len(dialog_text) / 54))
    dialog_ht = math.ceil(float(width * 0.06 * dialog_rows))
    img = cv2.imread(image_path)
    wrapped_dialog = textwrap.wrap(dialog_text, width = 54)
    return int(height - dialog_ht), wrapped_dialog, dialog_ht

def make_panel(image_list: list[list[str]]):
    op = add_narrator_text("plain_sheet.png", image_list[0][0])
    height = op[0]
    page = cv2.imread("plain_sheet.png")
    middle = int(height / 2)
    crds = [[middle - 585, 50], [middle - 585, 830], [middle + 5, 50], [middle + 5, 830]]
    print(len(image_list))
    wrapped_dialog = op[1]
    width = 1653
    font_size = (0.4 * width / 272 * 2 / 3)
    font_thickness = math.floor(width / 272 * 2 / 3)
    font =  cv2.FONT_HERSHEY_SIMPLEX | cv2.FONT_ITALIC
    cv2.rectangle(page, (50, 595 + middle), (width - 50, 595 + middle + op[2]), (140, 238, 255), -1)
    cv2.rectangle(page, (50, 595 + middle), (width - 50, 595 + middle + op[2]), (0, 0, 0), font_thickness)
    for i, line in enumerate(wrapped_dialog):   
        textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]
        gap = textsize[1] + int(width * 10 / 362)
        y = middle + 590 + int((width * 17.5 / 362) + i * (gap))
        x = int(int(height * 10 / 362))
        cv2.putText(page, line, (x, y), font, font_size, (0,0,0), font_thickness, lineType = cv2.LINE_AA)
    for i in range(1, len(image_list)):
        panel = cv2.imread(image_list[i][0])
        ht = int(panel.shape[1] * 3 / 4)
        cv2.imwrite("temp_panel.png", panel)
        dialog_ht = add_text("temp_panel.png", image_list[i][1])
        panel = cv2.imread("dialog_panel.png")
        panel = panel[0: ht, 0: panel.shape[1]]
        print(panel.shape)
        panel = cv2.resize(panel, (773, 580))
        font_thickness = math.floor(580 / 272 * 2 / 3)
        cv2.line(panel, (0, 580), (773, 580), (0, 0, 0), font_thickness * 10)
        print(page.shape, panel.shape)
        print(crds[i - 1][0], crds[i - 1][1])
        page[crds[i - 1][0]: crds[i - 1][0] + panel.shape[0], crds[i - 1][1]: crds[i - 1][1] + panel.shape[1]] = panel
    cv2.imwrite("sheet_output.png", page)
    return

make_panel([
    ["THE DAWN AWAKENS THE EPIC TALE OF HEROISM AND MYSTERY, SETTING THE STAGE FOR UNFORGETTABLE BATTLES."],
    ["image_1.png", "THE SHADOW STRIKES SILENTLY, UNLEASHING A CASCADE OF CHAOS ON THE UNWARY. THE SHADOW STRIKES SILENTLY, UNLEASHING A CASCADE OF CHAOS ON THE UNWARY."],
    ["image_2.png", "WITH THE MIGHT OF THE STARS, THE HERO RISES TO DEFY THE ODDS."],
    ["image_3.png", "AN UNEXPECTED ALLIANCE IS FORMED UNDER THE SILVER GLEAM OF THE MOON."],
    ["image_4.png", "THE VILLAIN LAUGHS, NAIVELY THINKING DEFEAT IS UNAVOIDABLE."]])