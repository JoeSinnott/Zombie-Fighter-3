import tkinter as tk
from PIL import Image, ImageTk
from random import randint

class zombie():
    def __init__(self, canvas):

        # Load and scale the zombie image
        zombie_image = Image.open("comp16321-labs_y46354js/images/zombie_img.png")
        zombie_image = zombie_image.convert("RGBA")  # Ensure transparency is preserved
        new_width = int(zombie_image.width * 5)
        new_height = int(zombie_image.height * 5)
        zombie_image = zombie_image.resize((new_width, new_height), Image.NEAREST)
        self.zombie_tk_image = ImageTk.PhotoImage(zombie_image)

        self.speed = 0

        self.image = canvas.create_image(
            randint(0,100)/100 * canvas.width,
            -0.1 * canvas.height,
            image=self.zombie_tk_image,
            anchor="center"
        )
