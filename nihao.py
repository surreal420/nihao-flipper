import os
from tkinter import Tk, Label, filedialog, Canvas, StringVar, DoubleVar, messagebox
from tkinter.ttk import Button, Frame, Combobox
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD
import io
import win32clipboard
from PIL import ImageWin


def flip_image(image_path, flip_position, flip_side):
    image = Image.open(image_path)
    
    original_mode = image.mode
    original_size = image.size
    
    flip_side = flip_side.lower()

    if flip_side.startswith('l'):
        flip_pos_px = int(image.width * flip_position)
        image_part = image.crop((0, 0, flip_pos_px, image.height))
        flipped_part = image_part.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        combined_image = Image.new(original_mode, (flip_pos_px * 2, image.height))
        combined_image.paste(image_part, (0, 0))
        combined_image.paste(flipped_part, (flip_pos_px, 0))
    elif flip_side.startswith('r'):
        flip_pos_px = int(image.width * flip_position)
        image_part = image.crop((flip_pos_px, 0, image.width, image.height))
        flipped_part = image_part.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        combined_image = Image.new(original_mode, ((image.width - flip_pos_px) * 2, image.height))
        combined_image.paste(flipped_part, (0, 0))
        combined_image.paste(image_part, (image.width - flip_pos_px, 0))
    elif flip_side.startswith('t'):
        flip_pos_px = int(image.height * flip_position)
        image_part = image.crop((0, 0, image.width, flip_pos_px))
        flipped_part = image_part.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        combined_image = Image.new(original_mode, (image.width, flip_pos_px * 2))
        combined_image.paste(image_part, (0, 0))
        combined_image.paste(flipped_part, (0, flip_pos_px))
    elif flip_side.startswith('b'):
        flip_pos_px = int(image.height * flip_position)
        image_part = image.crop((0, flip_pos_px, image.width, image.height))
        flipped_part = image_part.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        combined_image = Image.new(original_mode, (image.width, (image.height - flip_pos_px) * 2))
        combined_image.paste(flipped_part, (0, 0))
        combined_image.paste(image_part, (0, image.height - flip_pos_px))

    return combined_image


def load_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        open_image(file_path)


def save_image():
    if hasattr(app, 'combined_image'):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            app.combined_image.save(file_path)
            show_status(f"Output image saved at {file_path}")


def on_canvas_click(event):
    actual_x = int(event.x * app.scale_x)
    actual_y = int(event.y * app.scale_y)

    if flip_side.get().startswith(('l', 'r')):
        flip_position.set(actual_x / app.image.width)
    else:
        flip_position.set(actual_y / app.image.height)

    if hasattr(app, 'image_path'):
        combined_image = flip_image(app.image_path, flip_position.get(), flip_side.get())
        app.combined_image = combined_image
        
        combined_image_display = combined_image.copy()
        
        combined_image_display.thumbnail((500, 500))
        combined_img_tk = ImageTk.PhotoImage(combined_image_display)
        
        canvas_combined.image = combined_img_tk
        canvas_combined.create_image(0, 0, anchor='nw', image=combined_img_tk)


def open_image(image_path):
    app.image_path = image_path
    image = Image.open(image_path)
    app.image = image

    display_image = image.copy()
    display_image.thumbnail((500, 500))
    app.scale_x = image.width / display_image.width
    app.scale_y = image.height / display_image.height
    
    img_tk = ImageTk.PhotoImage(display_image)
    canvas.image = img_tk
    canvas.create_image(0, 0, anchor='nw', image=img_tk)
    show_status(f"Image loaded: {os.path.basename(image_path)}")


def drop(event):
    image_path = event.data
    if image_path.startswith('{') and image_path.endswith('}'):
        image_path = image_path[1:-1]
    open_image(image_path)


def copy_to_clipboard():
    if hasattr(app, 'combined_image'):
        output = io.BytesIO()
        app.combined_image.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

        show_status("Image copied to clipboard!")


def paste_from_clipboard():
    try:
        win32clipboard.OpenClipboard()
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
            clipboard_data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)

            image = Image.open(io.BytesIO(clipboard_data))
            image_path = "clipboard_image.png"
            image.save(image_path)
            open_image(image_path)
            show_status("Image pasted from clipboard!")
        else:
            show_status("No image found in clipboard!")
        win32clipboard.CloseClipboard()
    except Exception as e:
        show_status(f"Failed to paste image: {e}")


def show_status(message):
    status_label.config(text=message)


app = TkinterDnD.Tk()
app.title("nihao v0.3")

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

copy_button = Button(controls_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=0, column=2, padx=5, pady=5)

paste_button = Button(controls_frame, text="Paste from Clipboard", command=paste_from_clipboard)
paste_button.grid(row=0, column=3, padx=5, pady=5)

label = Label(controls_frame, text="Select flip side:")
label.grid(row=1, column=0, padx=5, pady=5)

flip_side_combo = Combobox(controls_frame, textvariable=flip_side, values=['left', 'right', 'top', 'bottom'], state='readonly')
flip_side_combo.grid(row=1, column=1, padx=5, pady=5)

status_label = Label(app, text="", relief="sunken", anchor='w')
status_label.pack(fill='x', padx=10, pady=5)

canvas.bind("<Button-1>", on_canvas_click)

canvas.drop_target_register(DND_FILES)
canvas.dnd_bind('<<Drop>>', drop)

app.bind("<Control-c>", lambda event: copy_to_clipboard())
app.bind("<Control-v>", lambda event: paste_from_clipboard())

app.mainloop()
