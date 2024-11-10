import tkinter as tk
from PIL import Image, ImageTk
from math import sqrt

class View(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        # Character variables
        self.acceleration = 0.0007
        self.speed = {"x": 0, "y": 0}
        self.character_pos = {"x": 0.5, "y": 0.5}
        self.dash_count = 0
        self.dash_cooldown = False



        # Load and scale the image using Pillow
        original_image = Image.open("comp16321-labs_y46354js/images/test.png")
        new_width = int(original_image.width * 4)
        new_height = int(original_image.height * 4)
        scaled_image = original_image.resize((new_width, new_height), Image.NEAREST)

        # Convert the scaled images to a format Tkinter can use
        self.photo = ImageTk.PhotoImage(scaled_image)

        # Create a label to hold the scaled image
        self.character = tk.Label(self, image=self.photo)
        self.character.pack()

    def apply_character(self, event=None): # Applies all movement changes to the character

        self.gravity()
        self.walls()

        self.character.place(relx=self.character_pos["x"], rely=self.character_pos["y"], anchor='center')

        print(self.dash_cooldown)
        # Call function every 10 ms
        root.after(10, self.apply_character)

    def gravity(self, event=None): # Moves the character to simulate the effects of gravity
        
        # Apply the speed and acceleration variables
        self.speed["y"] += self.acceleration
        self.character_pos["y"] += self.speed["y"]

    def walls(self, event=None):
        # Stop character falling if touching bottom of screen
        if self.character_pos["y"] >= 0.9:
            self.character_pos["y"] = 0.9

        if self.character_pos["x"] >= 1:
            self.character_pos["x"] = 1

        if self.character_pos["x"] <= 0:
            self.character_pos["x"] = 0
        
    def dash(self, event=None):
        # Get distance and direction between character and mouse
        rel_x = root.winfo_pointerx()/root.winfo_screenwidth() - self.character_pos["x"]
        rel_y = root.winfo_pointery()/root.winfo_screenheight() - self.character_pos["y"]
        
        mult = 0.035/(sqrt(rel_x**2 + rel_y**2)) # movement scaler 
        
        
        if view.dash_cooldown == False:
            self.speed["y"] = 0
            if (self.dash_count < 12) and mult < 1: # Apply calculated movement if dash and dash cooldown has ended
                self.character_pos["x"] += mult*rel_x
                self.character_pos["y"] += mult*rel_y
                self.dash_count += 1
                root.after(10, self.dash)
            else: 
                self.dash_count = 0
                # start dash cooldown
                self.dash_cooldown = True
                root.after(200, lambda: setattr(self, 'dash_cooldown', False))

if __name__ == '__main__': # Runs if this file is ran directly
    root = tk.Tk()

    # Set window dimensions
    window_width = 1280
    window_height = 720
    root.geometry(f"{window_width}x{window_height}")
    root.attributes('-fullscreen', True)

    # Create View instance
    view = View(root)
    view.pack(side="top", fill="both", expand=True)

    root.bind("<Button-1>", view.dash)

    view.apply_character()

    root.mainloop()