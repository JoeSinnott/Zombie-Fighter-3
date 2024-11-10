import tkinter as tk
from PIL import Image, ImageTk

class View(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        # Load and scale the image using Pillow
        original_image = Image.open("comp16321-labs_y46354js/images/test.png")
        new_width = int(original_image.width * 4)
        new_height = int(original_image.height * 4)
        scaled_image = original_image.resize((new_width, new_height), Image.NEAREST)

        # Convert the scaled images to a format Tkinter can use
        self.photo = ImageTk.PhotoImage(scaled_image)

        # Create a label to hold the scaled image
        self.image_label = tk.Label(self, image=self.photo)
        self.image_label.pack()

if __name__ == '__main__':
    root = tk.Tk()

    # Set window dimensions
    window_width = 900
    window_height = 600
    root.geometry(f"{window_width}x{window_height}")

    # Create View instance
    view = View(root)
    view.pack(side="top", fill="both", expand=True)

    root.mainloop()