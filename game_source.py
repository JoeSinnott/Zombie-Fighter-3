import tkinter as tk
from PIL import Image, ImageTk

class View(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.acceleration = 0.0007
        self.speed = 0
        self.character_x = 0.5
        self.character_y = 0.5


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

    def gravity(self, event=None): # Moves the character to simulate the effects of gravity
        
        # Apply the speed and acceleration variables
        self.speed += self.acceleration
        self.character_y += self.speed

        # Stop character falling if touching bottom of screen
        if self.character_y >= 0.88:
            self.character_y = 0.88
        self.character.place(relx=self.character_x, rely=self.character_y, anchor='center')


        # Call function every 10 ms
        root.after(10, self.gravity)

if __name__ == '__main__': # Runs if this file is ran directly
    root = tk.Tk()

    # Set window dimensions
    window_width = 900
    window_height = 600
    root.geometry(f"{window_width}x{window_height}")

    # Create View instance
    view = View(root)
    view.pack(side="top", fill="both", expand=True)

    view.gravity()

    root.mainloop()