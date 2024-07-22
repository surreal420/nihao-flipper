import os
from tkinter import Tk, Label, filedialog, Canvas, PhotoImage, StringVar, DoubleVar
from tkinter.ttk import Button, Frame, Combobox
from ttkthemes import ThemedTk
from PIL import Image, ImageTk

def flip_image(image_path, flip_position, flip_side):
    image = Image.open(image_path)

    flip_side = flip_side.lower()

    if flip_side.startswith('l'):
        flip_pos_px = int(image.width * flip_position)
        image_part = image.crop((0, 0, flip_pos_px, image.height))
        flipped_part = image_part.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        combined_image = Image.new('RGB', (flip_pos_px * 2, image.height))
        combined_image.paste(image_part, (0, 0))
        combined_image.paste(flipped_part, (flip_pos_px, 0))
    elif flip_side.startswith('r'):
        flip_pos_px = int(image.width * flip_position)
        image_part = image.crop((flip_pos_px, 0, image.width, image.height))
        flipped_part = image_part.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        combined_image = Image.new('RGB', ((image.width - flip_pos_px) * 2, image.height))
        combined_image.paste(flipped_part, (0, 0))
        combined_image.paste(image_part, (image.width - flip_pos_px, 0))
    elif flip_side.startswith('t'):
        flip_pos_px = int(image.height * flip_position)
        image_part = image.crop((0, 0, image.width, flip_pos_px))
        flipped_part = image_part.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        combined_image = Image.new('RGB', (image.width, flip_pos_px * 2))
        combined_image.paste(image_part, (0, 0))
        combined_image.paste(flipped_part, (0, flip_pos_px))
    elif flip_side.startswith('b'):
        flip_pos_px = int(image.height * flip_position)
        image_part = image.crop((0, flip_pos_px, image.width, image.height))
        flipped_part = image_part.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        combined_image = Image.new('RGB', (image.width, (image.height - flip_pos_px) * 2))
        combined_image.paste(flipped_part, (0, 0))
        combined_image.paste(image_part, (0, image.height - flip_pos_px))
    else:
        raise ValueError("Flip side must be 'left', 'right', 'top', or 'bottom'")

    return combined_image

def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        app.image = Image.open(file_path)
        w, h = app.image.size
        
        scale = min(500 / w, 500 / h)
        new_w, new_h = int(w * scale), int(h * scale)
        
        canvas.config(width=new_w, height=new_h)
        canvas_combined.config(width=new_w, height=new_h)
        
        app.image = app.image.resize((new_w, new_h), Image.ANTIALIAS)
        
        img_tk = ImageTk.PhotoImage(app.image)
        canvas.image = img_tk
        
        x_center = (new_w - img_tk.width()) // 2
        y_center = (new_h - img_tk.height()) // 2
        
        canvas.create_image(x_center, y_center, anchor='nw', image=img_tk)
        app.image_path = file_path

def save_image():
    if hasattr(app, 'image_path') and hasattr(app, 'combined_image'):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            app.combined_image.save(file_path)
            print(f"Output image saved at {file_path}")

def on_canvas_click(event):
    if flip_side.get().startswith(('l', 'r')):
        flip_position.set(event.x / app.image.width)
    else:
        flip_position.set(event.y / app.image.height)

    if hasattr(app, 'image_path'):
        combined_image = flip_image(app.image_path, flip_position.get(), flip_side.get())
        app.combined_image = combined_image
        combined_image.thumbnail((app.image.width, app.image.height))
        combined_img_tk = ImageTk.PhotoImage(combined_image)
        canvas_combined.image = combined_img_tk
        canvas_combined.create_image(0, 0, anchor='nw', image=combined_img_tk)

app = ThemedTk(theme="breeze")
app.title("nihao")

flip_side = StringVar(value='left')
flip_position = DoubleVar(value=0.5)

frame = Frame(app)
frame.pack(padx=10, pady=10)

canvas = Canvas(frame, width=500, height=500, bd=2, relief="sunken")
canvas.grid(row=0, column=0, padx=5, pady=5)

canvas_combined = Canvas(frame, width=500, height=500, bd=2, relief="sunken")
canvas_combined.grid(row=0, column=1, padx=5, pady=5)

controls_frame = Frame(app)
controls_frame.pack(padx=10, pady=10)

load_button = Button(controls_frame, text="Load Image", command=load_image)
load_button.grid(row=0, column=0, padx=5, pady=5)

save_button = Button(controls_frame, text="Save Image", command=save_image)
save_button.grid(row=0, column=1, padx=5, pady=5)

label = Label(controls_frame, text="Select flip side:")
label.grid(row=1, column=0, padx=5, pady=5)

flip_side_combo = Combobox(controls_frame, textvariable=flip_side, values=['left', 'right', 'top', 'bottom'], state='readonly')
flip_side_combo.grid(row=1, column=1, padx=5, pady=5)

canvas.bind("<Button-1>", on_canvas_click)

app.mainloop()