import tkinter as tk
from PIL import Image, ImageTk
from math import sqrt

class View(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=1920, height=1080)
        self.pack()
        
        self.height = self.winfo_screenheight()
        self.width = self.winfo_screenwidth()

        # Character variables
        self.acceleration = 0.0007
        self.character_speed = {"x": 0, "y": 0}
        self.character_pos = {"x": 0.5, "y": 0.5}
        self.dash_count = 0
        self.dash_cooldown = False

        # Load the background image and add it to the canvas
        bg_image = Image.open("comp16321-labs_y46354js/images/bg_image.jpg")
        new_height = int(self.height)
        new_width = int(bg_image.width * (new_height/bg_image.height))
        bg_image = bg_image.resize((new_width,new_height), Image.NEAREST)
        self.bg_tk_image = ImageTk.PhotoImage(bg_image)
        self.create_image(0, 0, anchor="nw", image=self.bg_tk_image)

        # Load and scale the character image
        character_image = Image.open("comp16321-labs_y46354js/images/test.png")
        character_image = character_image.convert("RGBA")  # Ensure transparency is preserved
        new_width = int(character_image.width * 4)
        new_height = int(character_image.height * 4)
        character_image = character_image.resize((new_width, new_height), Image.NEAREST)
        self.photo = ImageTk.PhotoImage(character_image)

        # Add the character image to the canvas
        self.character = self.create_image(
            self.character_pos["x"] * self.width,
            self.character_pos["y"] * self.height,
            image=self.photo,
            anchor="center"
        )

    def apply_character(self, event=None):
        # Update character position with gravity and wall constraints
        self.gravity()
        self.walls()

        # Update character position on canvas
        self.coords(
            self.character,
            self.character_pos["x"] * self.width,
            self.character_pos["y"] * self.height
        )

        # Call function every 20 ms (adjust if necessary)
        root.after(20, self.apply_character)

    def gravity(self, event=None):
        # Apply gravity
        self.character_speed["y"] += self.acceleration
        self.character_pos["y"] += self.character_speed["y"]
        self.character_pos["x"] += self.character_speed["x"]

    def walls(self, event=None):
        if self.character_pos["y"] >= 0.843:
            self.character_pos["y"] = 0.843
            self.character_speed["x"] = 0
        if self.character_pos["y"] <= 0:
            self.character_pos["y"] = 0
            self.character_speed["y"] = 0
        if self.character_pos["x"] >= 1:
            self.character_pos["x"] = 1
        if self.character_pos["x"] <= 0:
            self.character_pos["x"] = 0

    def dash(self, event=None):
        rel_x = root.winfo_pointerx() / root.winfo_screenwidth() - self.character_pos["x"]
        rel_y = root.winfo_pointery() / root.winfo_screenheight() - self.character_pos["y"]

        mult = 0.035 / (sqrt(rel_x ** 2 + rel_y ** 2))
        if self.dash_count == 0:
            self.dash_movement_x = mult * rel_x
            self.dash_movement_y = mult * rel_y

        if self.dash_cooldown == False:
            self.character_speed["y"] = 0
            if (self.dash_count < 12) and mult < 1:
                self.character_pos["x"] += self.dash_movement_x
                self.character_pos["y"] += self.dash_movement_y
                self.dash_count += 1
                root.after(10, self.dash)
            else:
                self.dash_count = 0
                self.character_speed["x"] = self.dash_movement_x * 0.3
                self.character_speed["y"] = self.dash_movement_y * 0.3
                self.dash_cooldown = True
                root.after(200, lambda: setattr(self, 'dash_cooldown', False))

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1920x1080")
    root.attributes('-fullscreen', True)
    root.resizable(False, False)

    # Create the View instance using Canvas
    view = View(root)

    root.bind("<Button-1>", view.dash)
    view.apply_character()

    root.mainloop()