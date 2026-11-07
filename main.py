from tkinter import *
import random

# Game constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3

SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

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

        # generate random coordinates for the food
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

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

    # place the button on the canvas
    canvas.create_window(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2 + 100,
        window=restart_button
    )

def restart_game():

    # declare global variables
    global snake, food, score, direction

    # restart game variables
    canvas.delete(ALL)
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))

    # clear the canvas
    canvas.delete(ALL)

    # recreate the snae and food
    snake = Snake()
    food = Food()

    # restart the game loop
    next_turn(snake, food)

# Create game window
window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

# Score label
label = Label(
    window,
    text="Score:{}".format(score),
    font=('consolas', 40)
)
label.pack()

# Game canvas
canvas = Canvas(
    window,
    bg=BACKGROUND_COLOR,
    height=GAME_HEIGHT,
    width=GAME_WIDTH
)
canvas.pack()

# Update the window to get its actual size
window.update()

# Center the window on the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# calculate the position to center the window
x = (screen_width/2) - (window_width/2)
y = (screen_height/2) - (window_height/2)

# set the window geometry to center it on the screen
window.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

# Bind keyboard controls
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))


snake = Snake()
food = Food()

next_turn(snake, food)

# Start window
window.mainloop()
