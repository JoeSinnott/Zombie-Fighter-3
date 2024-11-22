import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageFont
import json

from entities import zombie, demon, character, capybara

class Game(tk.Canvas):
    """Canvas-based game class."""

    def __init__(self, root, name, dash_b, pause_b, boss_b, width=1920, height=1080):
        super().__init__(root, width=width, height=height)

        # Initialize canvas dimensions
        self.height = height
        self.width = width

        # Bind keys for dash, pause, and boss actions
        root.bind(dash_b, self.dash)
        root.bind(pause_b, self.pause)
        root.bind(boss_b, self.boss)

        self.boss_screen = None
        self.paused = False
        self.score = 0
        self.time = 0
        self.speed = 20
        self.name = name

        # Monster lists
        self.zombies = []
        self.demons = []

        # Load and scale game over image
        game_over_image = Image.open("images/game_over.png").convert("RGBA")
        new_width = int(game_over_image.width * 16)
        new_height = int(game_over_image.height * 16)
        game_over_image = game_over_image.resize((new_width, new_height), Image.NEAREST)
        self.game_over_tk_image = ImageTk.PhotoImage(game_over_image)

        # Load and scale background image
        bg_image = Image.open("images/bg_image.png")
        new_height = self.height
        new_width = int(bg_image.width * (new_height / bg_image.height))
        bg_image = bg_image.resize((new_width, new_height), Image.NEAREST)
        self.bg_tk_image = ImageTk.PhotoImage(bg_image)
        self.create_image(0, 0, anchor="nw", image=self.bg_tk_image)

        # Initialize character and capybara
        self.capy = capybara(self)
        self.character = character(self)

        # Secret cheat codes
        if self.name == "2X!":
            self.speed = 1
            self.character.acceleration = 0.000035
        elif self.name == "0G!":
            self.character.acceleration = 0

        # Timer, score  and capy health display
        self.timer_text = self.create_text(
            0.3 * self.width,
            0.05 * self.height,
            text=f"Time: {self.time}s", font=("Courier New", 60, "bold"), fill="red"
        )
        self.score_text = self.create_text(
            0.5 * self.width,
            0.05 * self.height,
            text=f"Score: {self.score}", font=("Courier New", 60, "bold"), fill="red"
        )
        self.health_text = self.create_text(
            0.5 * self.width,
            0.95 * self.height,
            text=f"Health: {self.capy.health}", font=("Courier New", 60, "bold"), fill="red"
        )


    def test(self):
        """Placeholder for testing functionality."""
        pass

    def boss(self, event=None):
        """Toggle boss screen overlay."""
        if self.boss_screen == None:
            self.pause()
            boss_image = Image.open("images/boss_screen.png")
            boss_image = boss_image.resize((self.width, self.height), Image.NEAREST)
            self.boss_tk_image = ImageTk.PhotoImage(boss_image) 

            # Add the boss screen to the canvas
            self.boss_screen = self.create_image(0, 0,  image=self.boss_tk_image, anchor=tk.NW)
        else:
            self.delete(self.boss_screen)
            self.boss_screen = None



    def timer(self):
        """Update game timer."""
        if not self.paused:
            self.time += 1
            root.after(1000, self.timer)

    def set_up(self):
        """Set up the game environment."""
        self.spawn_zombie()
        self.spawn_demon()

        self.timer()

        self.game_loop()

    def pause(self, event=None):
        """Toggle game pause state."""
        self.paused = not self.paused
        if self.paused == True:
            root.unbind("<Button-1>")

            # Define button properties
            button_width, button_height = 200, 80
            button_x, button_y = round(self.width/2), round(self.height/2)

            # Bind the button area to the action
            self.tag_bind("save", "<Button-1>", lambda event: self.to_menu("progress"))

            self.save_button = []
            # Create button rectangle
            self.save_button.append(self.create_rectangle(
                button_x - button_width // 2, button_y - button_height // 2,
                button_x + button_width // 2, button_y + button_height // 2,
                tags="save", fill="red", outline="black", width=7
            ))

            # Add text
            self.save_button.append(self.create_text(
                button_x, button_y,
                tags="save", text="save", font=("Courier New", 40, "bold"), fill="white"
            ))

        elif self.paused == False:
            # Remove button and restart game
            for part in self.save_button:
                self.delete(part)
            self.set_up()
            root.bind("<Button-1>", self.dash)

    def game_loop(self, event=None):
        """Main game loop for updating game elements."""
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
        
        # Check for capy collision
        self.capy_collision()


        if self.capy.health <= 0: # End game when capy runs out of health
            self.game_over()

        self.itemconfig(self.timer_text, text=f"Time: {self.time}")
        self.itemconfig(self.score_text, text=f"Score: {self.score}")

        # Call function every 20 ms or 1ms if cheat code enabled
        if not self.paused:
            root.after(self.speed, self.game_loop)

    def game_over(self):
        """Handle game over state."""
        # Stop game and stop player from moving or pausing
        self.paused = True
        root.unbind("<Button-1>")
        root.unbind("<Escape>")

        # Display game over message
        self.game_over_image = self.create_image(
            0.5 * self.width,
            0.5 * self.height,
            image=self.game_over_tk_image,
            anchor=tk.CENTER
        )

        root.after(5000, lambda: self.to_menu("score"))
        
    def to_menu(self, option):
        """Return to the main menu."""
        # Save score or Save progress depending on circumstance
        if option == "score":
            self.save_score()
        elif option == "progress":
            self.save_progress()

        # Unpack game and pack menu
        self.pack_forget()
        menu = Menu(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        menu.pack()
        menu.update_idletasks()
    
    def save_score(self):
        """Save player score to leaderboard."""
        # Open leaderboard file and get contents
        with open("leaderboard.json", "r") as file:
            try:
                leaderboard = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                # If file missing or empty, use empty list
                leaderboard = []
            
            # Add name and score to leaderboard and sort it
            leaderboard.append({"name": self.name, "score": self.score})
            leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]

        with open("leaderboard.json", "w") as file:
            json.dump(leaderboard, file)
        
        # Clear save upon death
        with open("save.json", "w") as file:
            json.dump({"name": "", "score": 0, "time": 0}, file)

    def save_progress(self):
        """Save game progress."""
        # Save the name, score and time to a dictionary in the json
        save = {"name": self.name, "score": self.score, "time": self.time}
        with open("save.json", "w") as file:
            json.dump(save, file)

    def gravity(self, event=None):
        """Apply gravity and update character position."""
        # Apply gravity to character
        self.character.speed_y += self.character.acceleration
        self.character.y += self.character.speed_y
        self.character.x += self.character.speed_x
               
    def walls(self, event=None):
        """Constrain character within walls."""
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
        """Perform a dash action."""
        self.character.dash()

    def spawn_zombie(self, event=None):
        """Spawn a zombie."""
        # Add the zombie object to the zombie list
        if not self.paused:
            self.zombies.append(zombie(self))

            freq = round(2000/(0.01*self.time+1))

            root.after(freq, self.spawn_zombie)

    def spawn_demon(self, event=None):
        """Spawn a demon."""
        # Add the demon object to the zombie list
        if not self.paused:
            self.demons.append(demon(self))

            freq = round(2000/(0.01*self.time+1))

            root.after(freq, self.spawn_demon)
    
    def mon_collision(self):
        """Handle character-monster collisions."""
        char_bbox = self.bbox(self.character.image)
        for monster_list, score_increment in [(self.zombies, 10), (self.demons, 10)]:
            for monster in monster_list[:]:
                if self.check_collision(self.bbox(monster.image), char_bbox):
                    monster_list.remove(monster)
                    self.score += score_increment

    def capy_collision(self):
        """Handle capybara-monster collisions."""
        capy_bbox = self.bbox(self.capy.image)
        for monster_list in [self.zombies, self.demons]:
            for monster in monster_list[:]:
                if self.check_collision(self.bbox(monster.image), capy_bbox):
                    monster_list.remove(monster)
                    self.capy.health -= 1
                    self.itemconfig(self.health_text, text=f"Health: {self.capy.health}")

    @staticmethod
    def check_collision(bbox1, bbox2):
        """Check if two bounding boxes overlap."""
        return not (
            bbox1[2] < bbox2[0]     # Entity 1 is to the left of Entity 2
            or bbox1[0] > bbox2[2]  # Entity 1 is to the right of Entity 2
            or bbox1[3] < bbox2[1]  # Entity 1 is above Entity 2
            or bbox1[1] > bbox2[3]  # Entity 1 is below Entity 2
        )



class Menu(tk.Canvas):
    """Canvas-based menu class."""
    def __init__(self, root, width=1920, height=1080):
        super().__init__(root, width=width, height=height)
        
        # Store canvas dimensions
        self.height = height
        self.width = width

        # Initialize player name and control bindings
        self.name = ""
        self.controls_menu = None
        self.dash = "<Button-1>"  # Default dash control
        self.pause = "<Escape>"   # Default pause control
        self.boss = "b"           # Default boss screen toggle

        # Load and display the background image
        bg_image = Image.open("images/bg_image.png")
        new_height = int(self.height)
        new_width = int(bg_image.width * (new_height / bg_image.height))
        bg_image = bg_image.resize((new_width, new_height), Image.NEAREST)
        self.bg_tk_image = ImageTk.PhotoImage(bg_image)
        self.create_image(0, 0, anchor="nw", image=self.bg_tk_image)

        # Load and display the game logo
        logo_image = Image.open("images/game_logo.png")
        new_height = int(logo_image.height * 6)
        new_width = int(logo_image.width * 6)
        logo_image = logo_image.resize((new_width, new_height), Image.NEAREST)
        self.logo_tk_image = ImageTk.PhotoImage(logo_image)
        self.create_image(self.width / 4, 0, anchor=tk.N, image=self.logo_tk_image)

        # Add buttons to the menu
        self.create_button("PLAY", lambda: self.name_entry(), round(self.width / 4), round(0.55 * self.height))
        self.create_button("RESUME", lambda: self.play(load=True), round(self.width / 4), round(0.65 * self.height))
        self.create_button("CONTROLS", lambda: self.change_controls(), round(self.width / 4), round(0.75 * self.height))
        
        # Display the leaderboard
        self.display_leaderboard()

    def create_button(self, text, action, x, y):
        """Create a clickable button on the menu."""
        button_width, button_height = 200, 80

        # Define the button area
        self.create_rectangle(
            x - button_width // 2, y - button_height // 2,
            x + button_width // 2, y + button_height // 2,
            tags=text,  # Assign a tag for interaction
            fill="red", outline="black", width=7
        )

        # Add the button text
        self.create_text(
            x, y,
            tags=text, text=text, font=("Courier New", 40, "bold"), fill="white"
        )

        # Bind the button to an action
        self.tag_bind(text, "<Button-1>", lambda event: action())

    def display_leaderboard(self):
        """Display the top scores from the leaderboard."""
        self.create_text(
            round(0.55 * self.width), round(0.35 * self.height),
            text="Best scores:", font=("Courier New", 40, "bold"), fill="red", anchor=tk.W
        )

        try:
            with open("leaderboard.json", "r") as file:
                leaderboard = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            leaderboard = []

        # Display each leaderboard entry
        for place, entry in enumerate(leaderboard):
            self.create_text(
                round(0.55 * self.width), round((0.43 + place * 0.04) * self.height),
                text=(place + 1, entry["name"]), font=("Courier New", 40, "bold"), fill="red", anchor=tk.W
            )
            self.create_text(
                round(0.75 * self.width), round((0.43 + place * 0.04) * self.height),
                text=entry["score"], font=("Courier New", 40, "bold"), fill="red", anchor=tk.E
            )

    def play(self, load=False, event=None):
        """Start or resume the game."""
        save = {}
        if load:
            try:
                with open("save.json", "r") as file:
                    save = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        # Ensure name is valid before starting
        if len(self.name) == 3 or (load and save.get("name", "???") != ""):
            root.unbind("<Key>")
            root.unbind("<BackSpace>")
            root.unbind("<Return>")
            
            # Create a new game
            game = Game(root, self.name, self.dash, self.pause, self.boss,
                        width=root.winfo_screenwidth(), height=root.winfo_screenheight())
            game.pack()

            # Load progress if resuming
            if load:
                game.score = save.get("score", 0)
                game.time = save.get("time", 0)
                game.name = save.get("name", "???")
            game.set_up()
            self.pack_forget()

    def name_entry(self):
        """Prompt the user to enter their name."""
        # Create the name entry box
        self.create_rectangle(
            self.width * 0.4, self.height * 0.4,
            self.width * 0.6, self.height * 0.6,
            fill="grey", outline="black", width=7
        )
        self.create_text(
            0.5 * self.width, 0.41 * self.height,
            text="Input name:", font=("Courier New", 40, "bold"), fill="white", anchor=tk.N
        )

        # Bind key events for name input
        root.bind("<Key>", self.add_character)
        root.bind("<BackSpace>", self.delete_character)
        root.bind("<Return>", lambda event: self.play())

        # Display the entered name
        self.name_text = self.create_text(
            0.5 * self.width, 0.48 * self.height,
            text=self.name, font=("Courier New", 70, "bold"), fill="white", anchor=tk.N
        )

    def add_character(self, event):
        """Add a character to the player's name."""
        if event.char.isprintable() and len(self.name) < 3:
            self.name += event.char.upper()
            self.update_text()

    def delete_character(self, event):
        """Delete the last character of the player's name."""
        self.name = self.name[:-1]
        self.update_text()

    def update_text(self):
        """Update the name display."""
        self.delete(self.name_text)
        self.name_text = self.create_text(
            0.5 * self.width, 0.48 * self.height,
            text=self.name, font=("Courier New", 70, "bold"), fill="white", anchor=tk.N
        )

    def change_controls(self):
        """Allow the player to customize controls."""
        if self.controls_menu is None:
            # Create the controls customization menu
            self.controls_menu = [
                self.create_rectangle(
                    self.width * 0.35, self.height * 0.3,
                    self.width * 0.65, self.height * 0.7,
                    fill="grey", outline="black", width=7
                ),
                self.create_text(
                    0.5 * self.width, 0.31 * self.height,
                    text="Change controls:", font=("Courier New", 40, "bold"), fill="white", anchor=tk.N
                ),
                self.create_text(
                    0.36 * self.width, 0.4 * self.height,
                    text="Dash:", font=("Courier New", 40, "bold"), fill="white", anchor=tk.W
                ),
                self.create_text(
                    0.36 * self.width, 0.5 * self.height,
                    text="Pause:", font=("Courier New", 40, "bold"), fill="white", anchor=tk.W
                ),
                self.create_text(
                    0.36 * self.width, 0.6 * self.height,
                    text="Boss Screen:", font=("Courier New", 40, "bold"), fill="white", anchor=tk.W
                ),
                self.create_text(
                    0.64 * self.width, 0.4 * self.height,
                    tag="dash", text=self.dash, font=("Courier New", 40, "bold"), fill="white", anchor=tk.E
                ),
                self.create_text(
                    0.64 * self.width, 0.5 * self.height,
                    tag="pause", text=self.pause, font=("Courier New", 40, "bold"), fill="white", anchor=tk.E
                ),
                self.create_text(
                    0.64 * self.width, 0.6 * self.height,
                    tag="boss", text=self.boss, font=("Courier New", 40, "bold"), fill="white", anchor=tk.E
                )
            ]

            # Bind control change interaction
            self.tag_bind("dash", "<Button-1>", lambda event: root.bind("<Key>", lambda event: self.control_input(event, "dash")))
            self.tag_bind("pause", "<Button-1>", lambda event: root.bind("<Key>", lambda event: self.control_input(event, "pause")))
            self.tag_bind("boss", "<Button-1>", lambda event: root.bind("<Key>", lambda event: self.control_input(event, "boss")))


        else: 
            # Delete control menu
            for part in self.controls_menu:
                self.delete(part)
            self.controls_menu = None
        
    def control_input(self, event, action):
        """Handles key inputs for control change."""
        key = event.keysym
        if len(key) > 1:
            setattr(self, action, f"<{key}>")
        else:
            setattr(self, action, key)
        root.unbind("<Key>")
        self.change_controls()
        self.change_controls()
    

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

    # Force full screen
    root.attributes('-fullscreen', True)
    root.resizable(False, False)

    # Start game menu
    menu = Menu(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    menu.pack()

    root.mainloop()