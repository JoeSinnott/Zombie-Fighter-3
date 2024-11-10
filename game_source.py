import tkinter as tk
from PIL import Image, ImageTk

class View(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        # Character variables
        self.acceleration = 0.0007
        self.speed = {"x": 0, "y": 0}
        self.character_pos = {"x": 0.5, "y": 0.5}


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
        x = root.winfo_pointerx()
        y = root.winfo_pointery()
        print(x,y)
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
        pass


if __name__ == '__main__': # Runs if this file is ran directly
    root = tk.Tk()

    # Set window dimensions
    window_width = 1280
    window_height = 720
    root.geometry(f"{window_width}x{window_height}")

    # Create View instance
    view = View(root)
    view.pack(side="top", fill="both", expand=True)


    view.apply_character()

    root.mainloop()