import tkinter as tk
from PIL import Image, ImageTk
from math import sqrt
from monsters import zombie, demon

class View(tk.Canvas):
    def __init__(self, root, width=1920, height=1080):
        super().__init__(root, width=width, height=height)
        self.pack()
        
        self.height = height
        self.width = width

        self.paused = False

        # Character variables
        self.acceleration = 0.0007
        self.character_speed = {"x": 0, "y": 0}
        self.character_pos = {"x": 0.5, "y": 0.5}
        self.dash_count = 0
        self.dash_cooldown = False
        self.dashing = False
        self.rebound = 1

        # Zombie and demon lists
        self.zombies = []
        self.demons = []

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
        self.character_tk_image = ImageTk.PhotoImage(character_image)

        # Add the character image to the canvas
        self.character = self.create_image(
            self.character_pos["x"] * self.width,
            self.character_pos["y"] * self.height,
            image=self.character_tk_image,
            anchor=tk.S
        )

    def test(self):
        # print()
        pass

    def pause(self, event=None):
        self.paused = not self.paused
        if not self.paused:
            set_up()

    def game_loop(self, event=None):
        # Update character position on canvas
        self.coords(
            self.character,
            self.character_pos["x"] * self.width,
            self.character_pos["y"] * self.height
        )

        # Update the monsters' position on the canvas
        for monster in self.zombies + self.demons:
            monster.movement()
            self.coords(
                monster.image,
                monster.x * self.width,
                monster.y * self.height
            )


        # Update character position with gravity and wall constraints
        self.gravity()
        self.walls()

        # Test Function (prints stuff to check if working)
        self.test()

        if self.dashing: # Check for zombie collisions only if dashing
            self.mon_collision()

        # Call function every 20 ms
        if not self.paused:
            root.after(20, self.game_loop)

    def gravity(self, event=None):
        # Apply gravity to character
        self.character_speed["y"] += self.acceleration
        self.character_pos["y"] += self.character_speed["y"]
        self.character_pos["x"] += self.character_speed["x"]

        # Apply gravity to zombies
        for zombie in self.zombies:
            zombie.speed_y += self.acceleration
            zombie.x += zombie.speed_x
            zombie.y += zombie.speed_y
               

    def walls(self, event=None):
        if self.character_pos["y"] >= 0.907: # If character touches the ground
            self.character_pos["y"] = 0.907
            self.character_speed["x"] = 0
        if self.character_pos["y"] <= 0:     # If character touches the ceiling
            self.character_pos["y"] = 0
            self.character_speed["y"] = 0
        if self.character_pos["x"] >= 1:     # If character touches the right wall
            self.character_pos["x"] = 1
        if self.character_pos["x"] <= 0:     # If character touches the left wall
            self.character_pos["x"] = 0
            

    

    def dash(self, event=None):
        rel_x = root.winfo_pointerx() / root.winfo_screenwidth() - self.character_pos["x"]
        rel_y = root.winfo_pointery() / root.winfo_screenheight() - self.character_pos["y"]

        mult = 0.035 / (sqrt(rel_x ** 2 + rel_y ** 2))
        if self.dash_count == 0:
            self.dash_movement_x = mult * rel_x
            self.dash_movement_y = mult * rel_y

        if self.dash_cooldown == False:
            self.dashing = True
            self.character_speed["y"] = 0
            if (self.dash_count < 12) and mult < 1:
                self.character_pos["x"] += self.dash_movement_x
                self.character_pos["y"] += self.dash_movement_y
                self.dash_count += 1
                if not self.paused:
                    root.after(10, self.dash)
            else:
                self.dashing = False
                self.dash_count = 0
                self.character_speed["x"] = self.dash_movement_x * 0.3
                self.character_speed["y"] = self.dash_movement_y * 0.3
                self.dash_cooldown = True
                root.after(250, lambda: setattr(self, 'dash_cooldown', False))

    def spawn_zombie(self, event=None):
        # Add the zombie object to the zombie list
        if not self.paused:
            self.zombies.append(zombie(self))
            root.after(1500, self.spawn_zombie)

    def spawn_demon(self,event=None):
        # Add the demon object to the zombie list
        if not self.paused:
            self.demons.append(demon(self))
            root.after(2500, self.spawn_demon)
    
    def mon_collision(self):

        char_bbox = self.bbox(self.character)

        for zombie in self.zombies:
            zom_bbox = self.bbox(zombie.image)
            if not (zom_bbox[2] < char_bbox[0] or   # zombie is to the left of character
                    zom_bbox[0] > char_bbox[2] or   # zombie is to the right of character
                    zom_bbox[3] < char_bbox[1] or   # zombie is above character
                    zom_bbox[1] > char_bbox[3]):    # zombie is below character
                self.zombies.remove(zombie)

        for demon in self.demons:
            dem_bbox = self.bbox(demon.image)
            if not (dem_bbox[2] < char_bbox[0] or   # demon is to the left of character
                    dem_bbox[0] > char_bbox[2] or   # demon is to the right of character
                    dem_bbox[3] < char_bbox[1] or   # demon is above character
                    dem_bbox[1] > char_bbox[3]):    # demon is below character
                self.demons.remove(demon)


def set_up():
    view.spawn_zombie()
    view.spawn_demon()

    view.game_loop()

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    root.attributes('-fullscreen', True)
    root.resizable(False, False)

    # Create the View instance using Canvas
    view = View(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())

    root.bind("<Button-1>", view.dash)
    root.bind("<Escape>", view.pause)

    set_up()

    root.mainloop()