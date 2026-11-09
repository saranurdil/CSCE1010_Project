from tkinter import *
from tkinter import colorchooser
import random

# Game constants
GAME_WIDTH = 600
GAME_HEIGHT = 600
BODY_PARTS = 3
BACKGROUND_COLOR = "#000000"

# get filled in from the menu settings when the game starts
SPEED = 100
SPACE_SIZE = 50
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"

# menu looks
MENU_BG = "#1E1E1E"
CHIP_BG = "#3A3A3A"

# menu options
SNAKE_COLORS = ["#00FF00", "#00BFFF", "#FFD700", "#FF69B4", "#FFFFFF"]
FOOD_COLORS = ["#FF0000", "#FF8800", "#0044FF", "#FF00FF", "#00FFFF"]
CELL_SIZES = [("Large", 70), ("Medium", 50), ("Small", 35), ("Tiny", 25)]

# default menu settings
settings = {
    "snake_color": SNAKE_COLOR,
    "food_color": FOOD_COLOR,
    "speed": 5, # medium speed
    "space_size": 50
}

# Snake class
class Snake:

    # initialize the snake
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # initialize the snake coordinates
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # create the snake squares
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

# Food class
class Food:

    # initialize the food
    def __init__(self):

        
        # generate random coordinates for the food and force it not to spawn on the snake
        occupied = [tuple(c) for c in snake.coordinates]
        while True:    
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            if (x, y) not in occupied:
                break

        # set the food coordinates
        self.coordinates = [x, y]

        # create the food circle
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Next turn function
def next_turn(snake, food):

    # get the coordinates of the snake's head
    x, y = snake.coordinates[0]

    # update the coordinates based on the direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # insert the new coordinates at the beginning of the snake's body
    snake.coordinates.insert(0, (x, y))

    # create a new square for the snake's head
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    # insert the new square at the beginning of the snake's body
    snake.squares.insert(0, square)

    # check if the snake has eaten the food
    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    
    # otherwise, remove the last body part
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # check for collisions
    if check_collisions(snake):
        game_over()
    else:   
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    # change the direction of the snake

    global direction

    # check if the new direction is valid
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):

    # get the coordinates of the snake's head
    x, y = snake.coordinates[0]

    # check if the snake has hit the wall
    if x < 0 or x >= GAME_WIDTH:         
        # game over
        return True
    elif y < 0 or y >= GAME_HEIGHT:  
        # game over
        return True

    # check if the snake has hit its body
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            # game over
            return True

    # no collision detected
    return False

def game_over():

    # display game over message
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=('consolas', 70),
        text="GAME OVER",
        fill="red",
        tag="gameover"
    )

    # display a try again button
    restart_button = Button(
        window,
        text="Try again",
        font=('consolas', 20),
        command=restart_game
    )

    # display main menu button
    menu_button = Button(
            window,
            text="Main Menu",
            font=('consolas', 20),
            command=show_menu
    )
    game_over_widgets.extend([restart_button, menu_button])

    # place the buttons on the canvas
    canvas.create_window(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2 + 100,
        window=restart_button
    )
    canvas.create_window(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2 + 200,
        window=menu_button
    )

def clean_game_over_widgets():

    # remove buttons left over from the game over screen
    for widget in game_over_widgets:
        widget.destroy()
    game_over_widgets.clear()

def restart_game():

    # declare global variables
    global snake, food, score, direction

    # restart game variables
    clean_game_over_widgets()
    canvas.delete(ALL)      # clear the canvas
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))


    # recreate the snae and food
    snake = Snake()
    food = Food()

    # restart the game loop
    next_turn(snake, food)

def start_game():
    global SPEED, SPACE_SIZE, SNAKE_COLOR, FOOD_COLOR

    # apply game settings
    SNAKE_COLOR = settings["snake_color"]
    FOOD_COLOR = settings["food_color"]
    SPACE_SIZE = settings["space_size"]
    SPEED = 200 - settings["speed"] * 17

    # switch to the game screen
    menu_frame.pack_forget()

    # display the game frame
    game_frame.pack()
    
    # center the window
    center_window()

    restart_game()

def show_menu():

    # remove buttons left over from the game over screen
    clean_game_over_widgets()
    
    # hide the game frame
    game_frame.pack_forget()

    # display the menu frame
    menu_frame.pack()

    # center the window
    center_window()

def center_window():

    # center the window on the screen
    window.geometry("")

    # update the window to get its current dimensions
    window.update_idletasks()

    # get the window and screen dimensions
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # calculate the window position
    x = (screen_width/2) - (window_width/2)
    y = (screen_height/2) - (window_height/2)

    # set the window position
    window.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

class ChoiceRow:

    
    # initialize the choice row
    def __init__(self, parent, key, options, color_mode=False):
        self.key = key
        self.chips = []
        self.custom_chip = None
    
        # create the choice row
        row = Frame(parent, bg=MENU_BG)
        row.pack(pady=(0, 18))

        # create the choice chips
        for text, value in options:

            # create the chip based on the color mode
            if color_mode:
                chip = Label(row, width=4, height=2, bg=value)
            else:
                chip = Label(row, text=text, font=('consolas', 14), fg="white", bg=CHIP_BG, padx=14, pady=8)
            self.add_chip(chip, value)
 
        # color rows also get a "+" chip for picking any custom color
        if color_mode:
            self.custom_chip = Label(row, text="+", font=('consolas', 16, 'bold'), fg="white",
                                     bg="#555555", width=3, height=1, pady=6)
            self.add_chip(self.custom_chip, None, command=self.pick_custom)
 
        self.refresh()
 
    # add a chip to the choice row
    def add_chip(self, chip, value, command=None):
        chip.value = value
        chip.config(highlightthickness=3, cursor="hand2")
        chip.pack(side=LEFT, padx=4)
        if command is None:
            chip.bind("<Button-1>", lambda event, c=chip: self.select(c.value))
        else:
            chip.bind("<Button-1>", lambda event: command())
        self.chips.append(chip)
 
    # select a choice
    def select(self, value):
        settings[self.key] = value
        self.refresh()
 
    # pick a custom color
    def pick_custom(self):
        color = colorchooser.askcolor(title="Pick a color")[1]
        if color:
            self.custom_chip.config(bg=color, text="")
            self.custom_chip.value = color
            self.select(color)
 
    # refresh the choice row
    def refresh(self):
        # highlight the chip that is currently selected
        for chip in self.chips:
            selected = chip.value is not None and chip.value == settings[self.key]
            chip.config(highlightbackground="white" if selected else MENU_BG)
 
def menu_heading(parent, text):
    Label(parent, text=text, font=('consolas', 16), fg="white", bg=MENU_BG).pack(pady=(0, 6))
    
# Create game window
window = Tk()
window.title("Snake game")
window.resizable(False, False)
window.config(bg=MENU_BG)

# Initialize game state
score = 0
direction = 'down'
snake = None
food = None
game_over_widgets = []
 
# menu screen
menu_frame = Frame(window, bg=MENU_BG, padx=60, pady=30)

# Menu title
Label(menu_frame, text="SNAKE", font=('consolas', 50, 'bold'), fg="#00FF00", bg=MENU_BG).pack(pady=(0, 20))

# Snake color selection
menu_heading(menu_frame, "Snake color")
ChoiceRow(menu_frame, "snake_color", [("", c) for c in SNAKE_COLORS], color_mode=True)
 
# Food color selection
menu_heading(menu_frame, "Food color")
ChoiceRow(menu_frame, "food_color", [("", c) for c in FOOD_COLORS], color_mode=True)
 
# Speed selection
menu_heading(menu_frame, "Speed  (1 = slow, 10 = fast)")
speed_slider = Scale(
    menu_frame,
    from_=1,
    to=10,
    orient=HORIZONTAL,
    length=320,
    font=('consolas', 12),
    bg=MENU_BG,
    fg="white",
    troughcolor=CHIP_BG,
    highlightthickness=0,
    command=lambda value: settings.update(speed=int(float(value)))
)
speed_slider.set(settings["speed"])
speed_slider.pack(pady=(0, 18))
 
# Board squares selection
menu_heading(menu_frame, "Board squares")
ChoiceRow(menu_frame, "space_size", CELL_SIZES)
 
# Start button
start_button = Button(
    menu_frame,
    text="START",
    font=('consolas', 24, 'bold'),
    width=10,
    command=start_game
)
start_button.pack(pady=(10, 0))
 
# game screen
game_frame = Frame(window)
 
# Score label
label = Label(
    game_frame,
    text="Score:{}".format(score),
    font=('consolas', 40)
)
label.pack()
 
# Game canvas
canvas = Canvas(
    game_frame,
    bg=BACKGROUND_COLOR,
    height=GAME_HEIGHT,
    width=GAME_WIDTH
)
canvas.pack()
 
# Bind keyboard controls
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
 
# Show the menu first (the game only starts when START is clicked)
show_menu()
 
# Start window
window.mainloop()