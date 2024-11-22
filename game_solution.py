import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageFont
import json

from entities import zombie, demon, character, capybara

class View(tk.Canvas):
    def __init__(self, root, name, width=1920, height=1080):
        super().__init__(root, width=width, height=height)
        
        self.height = height
        self.width = width

        root.bind("<Button-1>", self.dash)
        root.bind("<Escape>", self.pause)

        self.paused = False

        self.score = 0
        self.time = 0

        self.speed = 20

        self.name = name


        # Zombie and demon lists
        self.zombies = []
        self.demons = []

        # Load and scale the game_over image
        game_over_image = Image.open("images/game_over.png")
        game_over_image = game_over_image.convert("RGBA")  # Ensure transparency is preserved
        new_width = int(game_over_image.width * 16)
        new_height = int(game_over_image.height * 16)
        game_over_image = game_over_image.resize((new_width, new_height), Image.NEAREST)
        self.game_over_tk_image = ImageTk.PhotoImage(game_over_image)

        # Load the background image and add it to the canvas
        bg_image = Image.open("images/bg_image.png")
        new_height = int(self.height)
        new_width = int(bg_image.width * (new_height/bg_image.height))
        bg_image = bg_image.resize((new_width,new_height), Image.NEAREST)
        self.bg_tk_image = ImageTk.PhotoImage(bg_image)
        self.create_image(0, 0, anchor="nw", image=self.bg_tk_image)

        # instantiate character and capybara class
        self.capy = capybara(self)
        self.character = character(self)

        # Super secret cheat codes shhh
        if self.name == "2X!":
            self.speed = 1
            self.character.acceleration = 0.000035
        elif self.name == "0G!":
            self.character.acceleration = 0

        self.timer_text = self.create_text(
            0.3 * self.width,
            0.05 * self.height,
            text=f"{self.time}s", font=("Courier New", 60, "bold"), fill="red"
        )

        self.score_text = self.create_text(
            0.5 * self.width,
            0.05 * self.height,
            text=str(self.score), font=("Courier New", 60, "bold"), fill="red"
        )


    def test(self):
        pass

    def timer(self):
        if not self.paused:
            self.time += 1
            root.after(1000, self.timer)

    def set_up(self):
        self.spawn_zombie()
        self.spawn_demon()

        self.timer()

        self.game_loop()

    def pause(self, event=None):
        self.paused = not self.paused
        if self.paused == True:
            root.unbind("<Button-1>")

            # Define button properties
            button_width, button_height = 200, 80
            button_x, button_y = round(self.width/2), round(self.height/2)

            # Bind the button area to the action
            self.tag_bind("save", "<Button-1>", lambda event: self.to_menu("progress"))

            self.save_button = []

            self.save_button.append(self.create_rectangle(
                button_x - button_width // 2, button_y - button_height // 2,
                button_x + button_width // 2, button_y + button_height // 2,
                tags="save",  # Assign a tag to group the button elements
                fill="red", outline="black", width=7
            ))

            # Add text
            self.save_button.append(self.create_text(
                button_x, button_y,
                tags="save", text="save", font=("Courier New", 40, "bold"), fill="white"
            ))

        elif self.paused == False:
            for part in self.save_button:
                self.delete(part)
            self.set_up()
            root.bind("<Button-1>", self.dash)

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

        if self.capy.health <= 0:
            self.game_over()

        self.itemconfig(self.timer_text, text=f"{self.time}s")
        self.itemconfig(self.score_text, text=str(self.score))

        # Call function every 20 ms
        if not self.paused:
            root.after(self.speed, self.game_loop)

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

        root.after(5000, lambda: self.to_menu("score"))
        
    def to_menu(self, option):
        if option == "score":
            self.save_score()
        elif option == "progress":
            self.save_progress()
        self.pack_forget()
        menu = Menu(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        menu.pack()
        menu.update_idletasks()
    
    def save_score(self):
        with open("leaderboard.json", "r") as file:
            try:
                leaderboard = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                leaderboard = []
            print(f"name: {self.name}")
            leaderboard.append({"name": self.name, "score": self.score})
            leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
        with open("leaderboard.json", "w") as file:
            json.dump(leaderboard, file)
        
        # Clear save upon death
        with open("save.json", "w") as file:
            json.dump({"name": "", "score": 0, "time": 0}, file)

    def save_progress(self):
        save = {"name": self.name, "score": self.score, "time": self.time}
        with open("save.json", "w") as file:
            json.dump(save, file)

    def gravity(self, event=None):
        # Apply gravity to character
        self.character.speed_y += self.character.acceleration
        self.character.y += self.character.speed_y
        self.character.x += self.character.speed_x
               
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

            freq = round(2000/(0.01*self.time+1))

            root.after(freq, self.spawn_zombie)

    def spawn_demon(self, event=None):
        # Add the demon object to the zombie list
        if not self.paused:
            self.demons.append(demon(self))

            freq = round(2000/(0.01*self.time+1))

            root.after(freq, self.spawn_demon)
    
    def mon_collision(self):

        char_bbox = self.bbox(self.character.image)

        for zombie in self.zombies:
            zom_bbox = self.bbox(zombie.image)
            if not (zom_bbox[2] < char_bbox[0] or   # zombie is to the left of character
                    zom_bbox[0] > char_bbox[2] or   # zombie is to the right of character
                    zom_bbox[3] < char_bbox[1] or   # zombie is above character
                    zom_bbox[1] > char_bbox[3]):    # zombie is below character
                self.zombies.remove(zombie)
                self.score += 10

        for demon in self.demons:
            dem_bbox = self.bbox(demon.image)
            if not (dem_bbox[2] < char_bbox[0] or   # demon is to the left of character
                    dem_bbox[0] > char_bbox[2] or   # demon is to the right of character
                    dem_bbox[3] < char_bbox[1] or   # demon is above character
                    dem_bbox[1] > char_bbox[3]):    # demon is below character
                self.demons.remove(demon)
                self.score += 10

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

        self.name = ""

        # Load the background image and add it to the canvas
        bg_image = Image.open("images/bg_image.png")
        new_height = int(self.height)
        new_width = int(bg_image.width * (new_height/bg_image.height))
        bg_image = bg_image.resize((new_width,new_height), Image.NEAREST)
        self.bg_tk_image = ImageTk.PhotoImage(bg_image)
        self.create_image(0, 0, anchor="nw", image=self.bg_tk_image)

        logo_image = Image.open("images/game_logo.png")
        new_height = int(logo_image.width * 6)
        new_width = int(logo_image.width * 6)
        logo_image = logo_image.resize((new_width,new_height), Image.NEAREST)
        self.logo_tk_image = ImageTk.PhotoImage(logo_image)
        self.create_image(self.width/4, 0, anchor=tk.N, image=self.logo_tk_image)
        
        self.create_button("PLAY", lambda: self.name_entry(), round(self.width/4), round(0.55*self.height))
        self.create_button("RESUME", lambda: self.play(load=True), round(self.width/4), round(0.65*self.height))
        self.create_button("CONTROLS", lambda: self.play(), round(self.width/4), round(0.75*self.height))
        
        self.display_leaderboard()

    def create_button(self, text, action, x, y):
        # Define button properties
        button_width, button_height = 200, 80
        button_x, button_y = x, y

        # Bind the button area to the action
        self.tag_bind(text, "<Button-1>", lambda event: action())

        self.create_rectangle(
            button_x - button_width // 2, button_y - button_height // 2,
            button_x + button_width // 2, button_y + button_height // 2,
            tags=text,  # Assign a tag to group the button elements
            fill="red", outline="black", width=7
        )

        # Add text
        self.create_text(
            button_x, button_y,
            tags=text, text=text, font=("Courier New", 40, "bold"), fill="white"
        )

    def display_leaderboard(self):
        self.create_text(
            round(0.55*self.width), round(0.35*self.height),
            text="Best scores:", font=("Courier New", 40, "bold"), fill="red", anchor=tk.W
        )

        with open("leaderboard.json", "r") as file:
            try:
                leaderboard = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                leaderboard = []
        
        leaderboard_text = []
        for place, entry in enumerate(leaderboard):
            leaderboard_text.append(self.create_text(
            round(0.55*self.width), round((0.43 + place*0.04)*self.height),
            text=(place+1, entry["name"]), font=("Courier New", 40, "bold"), fill="red", anchor=tk.W
            ))
            leaderboard_text.append(self.create_text(
            round(0.75*self.width), round((0.43 + place*0.04)*self.height),
            text=entry["score"], font=("Courier New", 40, "bold"), fill="red", anchor=tk.E
            ))

    def play(self, load=False, event=None):
        if load:
                with open("save.json", "r") as file:
                    try:
                        save = json.load(file)
                    except (json.JSONDecodeError, FileNotFoundError):
                        save = {}
        # Create the View instance
        if len(self.name) == 3 or (load and save.get("name", "???") != ""):
            root.unbind("<Key>")
            root.unbind("<BackSpace>")
            root.unbind("<Return>")
            view = View(root, self.name, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
            view.pack()
            if load:
                view.score = save.get("score", 0)
                view.time = save.get("time", 0)
                view.name = save.get("name", "???")
            print(view.name)
            view.set_up()
            self.pack_forget()

    def name_entry(self):
        self.create_rectangle(
            self.width*0.4, self.height*0.4,
            self.width*0.6, self.height*0.6,
            fill="grey", outline="black", width=7
        )
        self.create_text(
            0.5*self.width, 0.41*self.height,
            text="Input name:", font=("Courier New", 40, "bold"), fill="white", anchor=tk.N
        )
        # Bind the key events
        root.bind("<Key>", self.add_character)
        root.bind("<BackSpace>", self.delete_character)  # Handle Backspace
        root.bind("<Return>", lambda event: self.play())
        self.name_text = self.create_text(
            0.5*self.width, 0.48*self.height,
            text=self.name, font=("Courier New", 70, "bold"), fill="white", anchor=tk.N
        )
        
    def add_character(self, event):
        """Adds the pressed key's character to the name."""
        char = event.char  # Get the character from the key press
        if char.isprintable() and len(self.name) < 3:  # Only handle printable characters
            self.name += char.upper()
            self.update_text()

    def delete_character(self, event):
        """Deletes the last character when Backspace is pressed."""
        self.name = self.name[:-1]  # Remove the last character
        self.update_text()

    def update_text(self):
        """Updates the canvas to display the current text."""
        self.delete(self.name_text)  # Clear previous text
        self.name_text = self.create_text(
            0.5*self.width, 0.48*self.height,
            text=self.name, font=("Courier New", 70, "bold"), fill="white", anchor=tk.N
        )

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    root.attributes('-fullscreen', True)
    root.resizable(False, False)


    menu = Menu(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    menu.pack()

    root.mainloop()