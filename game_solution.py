import tkinter as tk
from PIL import Image, ImageTk

from entities import zombie, demon, character, capybara

class View(tk.Canvas):
    def __init__(self, root, width=1920, height=1080):
        super().__init__(root, width=width, height=height)
        
        self.height = height
        self.width = width

        root.bind("<Button-1>", self.dash)
        root.bind("<Escape>", self.pause)

        self.paused = False

        # Zombie and demon lists
        self.zombies = []
        self.demons = []

        # Load and scale the game_over image
        game_over_image = Image.open("comp16321-labs_y46354js/images/game_over.png")
        game_over_image = game_over_image.convert("RGBA")  # Ensure transparency is preserved
        new_width = int(game_over_image.width * 16)
        new_height = int(game_over_image.height * 16)
        game_over_image = game_over_image.resize((new_width, new_height), Image.NEAREST)
        self.game_over_tk_image = ImageTk.PhotoImage(game_over_image)

        # Load the background image and add it to the canvas
        bg_image = Image.open("comp16321-labs_y46354js/images/bg_image.png")
        new_height = int(self.height)
        new_width = int(bg_image.width * (new_height/bg_image.height))
        bg_image = bg_image.resize((new_width,new_height), Image.NEAREST)
        self.bg_tk_image = ImageTk.PhotoImage(bg_image)
        self.create_image(0, 0, anchor="nw", image=self.bg_tk_image)

        # instantiate character and capybara class
        self.capy = capybara(self)
        self.character = character(self)


    def test(self):
        pass

    def set_up(self):
        self.spawn_zombie()
        self.spawn_demon()

        self.game_loop()

    def pause(self, event=None):
        self.paused = not self.paused
        if not self.paused:
            self.set_up()

    def game_loop(self, event=None):
        # Update character position on canvas
        self.coords(
            self.character.image,
            self.character.x * self.width,
            self.character.y * self.height
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

        if self.character.dashing: # Check for zombie collisions only if dashing
            self.mon_collision()
        
        self.capy_collision()

        if self.capy.health == 0 :
            self.game_over()

        # Call function every 20 ms
        if not self.paused:
            root.after(20, self.game_loop)

    def game_over(self):
        self.paused = True
        root.unbind("<Button-1>")
        root.unbind("<Escape>")

        self.game_over_image = self.create_image(
            0.5 * self.width,
            0.5 * self.height,
            image=self.game_over_tk_image,
            anchor=tk.CENTER
        )

        root.after(5000, self.to_menu)
        
    def to_menu(self):
        self.pack_forget()
        menu.pack()
        menu.update_idletasks()

    def gravity(self, event=None):
        # Apply gravity to character
        self.character.speed_y += self.character.acceleration
        self.character.y += self.character.speed_y
        self.character.x += self.character.speed_x

        # Apply gravity to zombies
        for zombie in self.zombies:
            zombie.speed_y += self.character.acceleration
            zombie.x += zombie.speed_x
            zombie.y += zombie.speed_y
               
    def walls(self, event=None):
        if self.character.y >= 0.907: # If character touches the ground
            self.character.y = 0.907
            self.character.speed_x = 0
        if self.character.y <= 0:     # If character touches the ceiling
            self.character.y = 0
            self.character.speed_y = 0
        if self.character.x >= 1:     # If character touches the right wall
            self.character.x = 1
        if self.character.x <= 0:     # If character touches the left wall
            self.character.x = 0

    def dash(self, event=None):
        self.character.dash()

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

        char_bbox = self.bbox(self.character.image)

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

    def capy_collision(self):

        capy_bbox = self.bbox(self.capy.image)

        for zombie in self.zombies:
            zom_bbox = self.bbox(zombie.image)
            if not (zom_bbox[2] < capy_bbox[0] or   # zombie is to the left of capybara
                    zom_bbox[0] > capy_bbox[2] or   # zombie is to the right of capybara
                    zom_bbox[3] < capy_bbox[1] or   # zombie is above capybara
                    zom_bbox[1] > capy_bbox[3]):    # zombie is below capybara
                self.zombies.remove(zombie)
                self.capy.health -= 1

        for demon in self.demons:
            dem_bbox = self.bbox(demon.image)
            if not (dem_bbox[2] < capy_bbox[0] or   # demon is to the left of capybara
                    dem_bbox[0] > capy_bbox[2] or   # demon is to the right of capybara
                    dem_bbox[3] < capy_bbox[1] or   # demon is above capybara
                    dem_bbox[1] > capy_bbox[3]):    # demon is below capybara
                self.demons.remove(demon)
                self.capy.health -= 1


class Menu(tk.Canvas):
    def __init__(self, root, width=1920, height=1080):
        super().__init__(root, width=width, height=height)
        
        self.height = height
        self.width = width

        # Load the background image and add it to the canvas
        bg_image = Image.open("comp16321-labs_y46354js/images/bg_image.png")
        new_height = int(self.height)
        new_width = int(bg_image.width * (new_height/bg_image.height))
        bg_image = bg_image.resize((new_width,new_height), Image.NEAREST)
        self.bg_tk_image = ImageTk.PhotoImage(bg_image)
        self.create_image(0, 0, anchor="nw", image=self.bg_tk_image)

        logo_image = Image.open("comp16321-labs_y46354js/images/game_logo.png")
        new_height = int(logo_image.width * 6)
        new_width = int(logo_image.width * 6)
        logo_image = logo_image.resize((new_width,new_height), Image.NEAREST)
        self.logo_tk_image = ImageTk.PhotoImage(logo_image)
        self.create_image(self.width*0.5, 0, anchor=tk.N, image=self.logo_tk_image)

        self.create_buttons()

    def create_buttons(self):
        # Define button properties
        button_width, button_height = 200, 80
        button_x, button_y = self.width // 2, round(0.6*self.height)

        # Bind the button area to the action
        self.tag_bind("button", "<Button-1>", lambda event: self.play())

        # Mark the rectangle and text as part of the button
        self.create_rectangle(
            button_x - button_width // 2, button_y - button_height // 2,
            button_x + button_width // 2, button_y + button_height // 2,
            tags="button",  # Assign a tag to group the button elements
            fill="red", outline="black", width=7
        )

        # Add pixelated text
        self.create_text(
            button_x, button_y,
            text="PLAY", font=("Terminal", 20, "bold"), fill="white"
        )

    def play(self):
        # Create the View instance
        global view
        view = View(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        view.pack()
        view.set_up()
        self.pack_forget()


if __name__ == '__main__':
    view = None

    root = tk.Tk()
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    root.attributes('-fullscreen', True)
    root.resizable(False, False)
    
    menu = Menu(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    menu.pack()

    root.mainloop()