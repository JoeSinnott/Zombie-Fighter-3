import tkinter as tk
from PIL import Image, ImageTk
from random import randint

class zombie:
    def __init__(self, canvas):
        self.canvas = canvas
        # Load and scale the zombie image
        zombie_image = Image.open("comp16321-labs_y46354js/images/zombie_img.png")
        zombie_image = zombie_image.convert("RGBA")  # Ensure transparency is preserved
        new_width = int(zombie_image.width * 5)
        new_height = int(zombie_image.height * 5)
        zombie_image = zombie_image.resize((new_width, new_height), Image.NEAREST)
        self.zombie_tk_image = ImageTk.PhotoImage(zombie_image)

        self.speed_x = 0
        self.speed_y = 0
        self.x = randint(5,95)/100
        self.y = -0.1

        self.image = self.canvas.create_image(
            self.x * self.canvas.width,
            self.y * self.canvas.height,
            image=self.zombie_tk_image,
            anchor=tk.S
        )
    def movement(self):
        if self.x >= 0.5:
            self.speed_x = -0.001
        else:
            self.speed_x = 0.001
    
