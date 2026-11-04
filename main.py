print("test")
print("Hello")

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


class Snake:
    pass


class Food:
    pass


def next_turn():
    pass


def change_direction(new_direction):
    pass


def check_collisions():
    pass


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

# Start window
window.mainloop()
