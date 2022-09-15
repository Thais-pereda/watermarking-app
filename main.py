"""A desktop application with a Graphical User Interface (GUI)
where you can upload an image and use Python to add a watermark logo/text."""

import os
import tkinter as tk
from tkinter import *
from tkinter import ttk, font, filedialog, Tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from functools import partial

def choose_file(frame):
    image_list.clear()
    basewidth = 300
    filename = filedialog.askopenfilename()
    image_list.append(filename)
    myimg = Image.open(filename)
    wpercent = (basewidth / float(myimg.size[0]))
    hsize = int((float(myimg.size[1]) * float(wpercent)))
    if len(image_list) > 0:
        resized_image = myimg.resize((basewidth, hsize))
        new_image = ImageTk.PhotoImage(resized_image)
        root.new_image = new_image
        image_frame = frame.create_image(30, 30, image=new_image, anchor='nw')
        watermark_button = ttk.Button(mainframe, text="Watermark my image",
                                      command=partial(place_watermark, watermark_text, image_frame, frame))
        watermark_button.grid(column=0, row=9, columnspan=3)



def place_watermark(watermark, image_frame, frame):
    global fonts
    global sizes
    global colors
    if len(image_list) > 0:
        with Image.open(image_list[0]).convert("RGBA") as base:
            # Text to drawing
            watermark_entry = watermark.get()
            watermark_image = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
            draw = ImageDraw.Draw(watermark_image)
            watermark_font = ImageFont.truetype(f'{fonts.get().lower()}.ttf', size=int(sizes.get()))
            xcord = horz_scale.get()
            ycord = vert_scale.get()
            draw.text((xcord, ycord), font=watermark_font, text=watermark_entry, fill=(colors.get()))
            watermark_image = watermark_image.resize(base.size)
            # Merge image with text drawing
            merged_image = Image.alpha_composite(base, watermark_image)
            wpercent = (300 / float(merged_image.size[0]))
            hsize = int((float(merged_image.size[1]) * float(wpercent)))
            # Resize image to display
            resized_merged = merged_image.resize((300, hsize))
            display_merged = ImageTk.PhotoImage(resized_merged)
            root.display_merged = display_merged
            frame.itemconfig(image_frame, image=display_merged)
            save_button = ttk.Button(mainframe, text="Save image", command=partial(save_image, merged_image))
            save_button.grid(column=4, row=9, columnspan=4)

def save_image(watermarked_image):
    dirname, filename = os.path.split(image_list[0])
    new_filename = f"watermarked_{filename}"
    watermark_path = os.path.join(dirname, new_filename)
    save_path = os.path.normcase(watermark_path)
    rgb_image = watermarked_image.convert("RGB")
    rgb_image.save(save_path)
    top = Toplevel(root)
    top.geometry("200x100")
    top.title("File saved")
    Label(top, text=f"File saved successfully as \n{new_filename}.", padx=20, pady=10).grid(row=0, column=0)



image_list = []

root = Tk()
root.title("Watermark App")
root.geometry("750x600")
highlightFont = font.Font(family='Helvetica', name='appHighlightFont', size=12, weight='bold')

mainframe = ttk.Frame(root, padding=(3,3,12,12))

image_canvas = tk.Canvas(mainframe, borderwidth=5, relief="ridge", width=350, height=450, background='gray75')
title = ttk.Label(mainframe, text="Choose an image to place the watermark.", font=highlightFont, justify='center',padding=(3,3,12,12))
button = ttk.Button(mainframe, text="Choose file", command=partial(choose_file, image_canvas))
watermark = ttk.Label(mainframe, text="Text:", font=highlightFont, justify='center', padding=(3,3,12,12))
watermark_text = ttk.Entry(mainframe)

font_label = ttk.Label(mainframe, text="Font:", font=highlightFont, justify='center', padding=(3,3,12,12))
fontvar = tk.StringVar()
fonts = ttk.Combobox(mainframe, textvariable=fontvar)
fonts['values'] = ("Arial", "Calibri", "Ebrima", "Georgia", "Impact", "Tahoma", "Verdana")
fonts.state(['readonly'])
fonts.current(0)

size_label = ttk.Label(mainframe, text="Size:", font=highlightFont, justify='center', padding=(3,3,12,12))
sizevar = tk.StringVar()
sizes = ttk.Combobox(mainframe, textvariable=sizevar)
sizes['values'] = tuple([i for i in range(50) if i % 2 == 0])
sizes.state(['readonly'])
sizes.current(12)

color_label = ttk.Label(mainframe, text="Color:", font=highlightFont, justify='center', padding=(3,3,12,12))
colorvar = tk.StringVar()
colors = ttk.Combobox(mainframe, textvariable=colorvar)
colors['values'] = ("green", "blue", "red", "yellow", "purple", "black", "white")
colors.state(['readonly'])
colors.current(0)

place_text_label = ttk.Label(mainframe, text="Move text:", font=highlightFont, justify='center', padding=(3,3,12,12))
up_label = ttk.Label(mainframe, text="Up", font=highlightFont, justify='center', padding=(3,3,12,12))
down_label = ttk.Label(mainframe, text="Down", font=highlightFont, justify='center', padding=(3,3,12,12))
vert_scale = ttk.Scale(mainframe, orient='horizontal', length=200, from_=1.0, to=200.0)
right_label = ttk.Label(mainframe, text="Right", font=highlightFont, justify='center', padding=(3,3,12,12))
left_label = ttk.Label(mainframe, text="Left", font=highlightFont, justify='center', padding=(3,3,12,12))
horz_scale = ttk.Scale(mainframe, orient='horizontal', length=200, from_=1.0, to=200.0)


mainframe.grid(column=0, row=0)
image_canvas.grid(column=4, row=0, columnspan=4, rowspan=8)
title.grid(column=0, row=0, columnspan=3)
button.grid(column=0, row=1, columnspan=3)
watermark.grid(column=0, row=2)
watermark_text.grid(column=1, row=2, columnspan=2)
font_label.grid(column=0, row=3)
fonts.grid(column=1, row=3, columnspan=2)
size_label.grid(column=0, row=4)
sizes.grid(column=1, row=4, columnspan=2)
color_label.grid(column=0, row=5)
colors.grid(column=1, row=5, columnspan=2)
place_text_label.grid(column=0, row=6, columnspan=2)
up_label.grid(column=0, row=7)
vert_scale.grid(column=1, row=7)
down_label.grid(column=2, row=7)
right_label.grid(column=2, row=8)
horz_scale.grid(column=1, row=8)
left_label.grid(column=0, row=8)

#TODO: add popup to feedback save image

root.mainloop()

