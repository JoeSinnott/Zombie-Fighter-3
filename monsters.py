import tkinter as tk
from PIL import Image, ImageTk
from random import randint
from math import sqrt

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
        self.x = randint(0,1)
        self.y = 0.905

        self.image = self.canvas.create_image(
            self.x * self.canvas.width,
            self.y * self.canvas.height,
            image=self.zombie_tk_image,
            anchor=tk.S
        )
    def movement(self):
        # Move zombie towards centre of screen
        if self.x >= 0.5:
            self.speed_x = -0.0004
        else:
            self.speed_x = 0.0004

        self.x += self.speed_x
        self.y += self.speed_y

        if self.y >= 0.905:
                self.y = 0.905


class demon:
    def __init__(self, canvas):
        self.canvas = canvas
        # Load and scale the demon image
        demon_image = Image.open("comp16321-labs_y46354js/images/demon.png")
        demon_image = demon_image.convert("RGBA")  # Ensure transparency is preserved
        new_width = int(demon_image.width * 4)
        new_height = int(demon_image.height * 4)
        demon_image = demon_image.resize((new_width, new_height), Image.NEAREST)
        self.demon_tk_image = ImageTk.PhotoImage(demon_image)

        self.speed_x = 0
        self.speed_y = 0

        self.y = randint(0,1)
        if self.y == 0:
            self.y -= 0.1
            self.x = randint(0,100)/100
        else:
            self.y = randint(0,50)/100
            self.x = randint(0,1)
            if self.x == 0:
                self.x -= 0.1
            else:
                self.x += 0.1

        # self.x = randint(0,100)/100
        # self.y = 0

        self.rel_x = 0.5 - self.x
        self.rel_y = 0.9 - self.y

        self.mult = 0.0035 / (sqrt(self.rel_x ** 2 + self.rel_y ** 2))

        self.image = self.canvas.create_image(
            self.x * self.canvas.width,
            self.y * self.canvas.height,
            image=self.demon_tk_image,
            anchor=tk.S
        )
    def movement(self):
        self.speed_y = self.rel_y * self.mult
        self.speed_x = self.rel_x * self.mult

        self.x += self.speed_x
        self.y += self.speed_y