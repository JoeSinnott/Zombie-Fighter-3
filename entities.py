"""Contains the classes for all of the entities within the game."""

import tkinter as tk
from PIL import Image, ImageTk
from random import randint
from math import sqrt


class zombie:
    def __init__(self, canvas):
        self.canvas = canvas
        # Load and scale the zombie image
        zombie_image = Image.open("images/zombie.png")
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

        if self.y >= 0.907:
                self.y = 0.907


class demon:
    def __init__(self, canvas):
        self.canvas = canvas
        # Load and scale the demon image
        demon_image = Image.open("images/demon.png")
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


class character:
    def __init__(self, canvas):
        self.canvas = canvas
        # create character variables
        self.acceleration = 0.0007
        self.speed_x = 0
        self.speed_y = 0
        self.x = 0.5
        self.y = -0.4
        self.dash_count = 0
        self.dash_cooldown = False
        self.dashing = False

        # Load and scale the character image
        character_image = Image.open("images/character.png")
        character_image = character_image.convert("RGBA")  # Ensure transparency is preserved
        new_width = int(character_image.width * 4)
        new_height = int(character_image.height * 4)
        character_image = character_image.resize((new_width, new_height), Image.NEAREST)
        self.character_tk_image = ImageTk.PhotoImage(character_image) 

        # Add the character image to the canvas
        self.image = self.canvas.create_image(
            self.x * self.canvas.width,
            self.y * self.canvas.height,
            image=self.character_tk_image,
            anchor=tk.S
        )

    def dash(self):
        """Moves the character towards the mouse with a dashing motion."""
        # Get relative mouse position
        rel_x = self.canvas.winfo_pointerx() / self.canvas.winfo_screenwidth() - self.x
        rel_y = self.canvas.winfo_pointery() / self.canvas.winfo_screenheight() - self.y

        mult = 0.035 / (sqrt(rel_x ** 2 + rel_y ** 2))

        if self.dash_count == 0:
            self.dash_movement_x = mult * rel_x
            self.dash_movement_y = mult * rel_y

        if not self.dash_cooldown:
            self.dashing = True
            self.speed_y = 0
            if self.dash_count < 12 and mult < 1:
                self.x += self.dash_movement_x
                self.y += self.dash_movement_y
                self.dash_count += 1
                self.canvas.after(10, self.dash)
            else:
                self.dashing = False
                self.dash_count = 0
                self.speed_x = self.dash_movement_x * 0.3
                self.speed_y = self.dash_movement_y * 0.3
                self.dash_cooldown = True
                self.canvas.after(250, lambda: setattr(self, 'dash_cooldown', False))


class capybara:
    def __init__(self, canvas):
        self.canvas = canvas
        # Load and scale the capybara image
        capy_image = Image.open("images/capy.png")
        capy_image = capy_image.convert("RGBA")  # Ensure transparency is preserved
        new_width = int(capy_image.width * 4)
        new_height = int(capy_image.height * 4)
        capy_image = capy_image.resize((new_width, new_height), Image.NEAREST)
        self.capy_tk_image = ImageTk.PhotoImage(capy_image)

        self.image = self.canvas.create_image(
            0.5 * self.canvas.width,
            0.907 * self.canvas.height,
            image=self.capy_tk_image,
            anchor=tk.S
        )

        self.health = 10

    