from sense_hat import SenseHat
import time
import random
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause

Y = (255, 255, 0)
O = (0, 0, 0)
T = (0, 180, 220)

Spielfeld = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O
]

x = 0
y = 7

sense = SenseHat()


class Hindernis():
    def __init__(self):
        self.y = 0
        self.Loch = random.randint(1, 7)  # creates random loch

    def move(self):
        self.y += 1  # not allowed more than 1 for each pixel


# Controls start ---------------------------------------------------------------------------------------
def pushed_up(event):
    global y
    if event.action != ACTION_RELEASED:
        y -= 1
        if y < 0:
            y = 0


def pushed_down(event):
    global y
    if event.action != ACTION_RELEASED:
        y += 1
        if y > 7:
            y = 7


def pushed_left(event):
    global x
    if event.action != ACTION_RELEASED:
        x -= 1
        if x < 0:
            x = 0


def pushed_right(event):
    global x
    if event.action != ACTION_RELEASED:
        x += 1
        if x > 7:
            x = 7


# Controls end-----------------------------------------------------------------------------------------

# Drawing starts-------------------------------------------------------------------------------------
def draw_player():
    sense.clear()
    sense.set_pixel(x, y, 255, 255, 255)


def draw_Hindernis(Objekt):
    for i in range(8):
        if i == Objekt.Loch - 1 or i == Objekt.Loch or i == Objekt.Loch + 1:
            pass
        else:
            if 0 <= Objekt.y < 8:  # Check if Y position is within valid range
                sense.set_pixel(i, Objekt.y, T)


# Drawing ends------------------------------------------------------------------------------------------

def refresh():
    sense.clear()
    sense.set_pixel(clamp(x), clamp(y), 255, 255, 255)


# Adjusted clamp function to include bounday values
def clamp(value, min_value=0, max_value=7):
    return min(max_value, max(min_value, value))


sense.stick.direction_up = pushed_up
sense.stick.direction_down = pushed_down
sense.stick.direction_left = pushed_left
sense.stick.direction_right = pushed_right


def gameloop():
    Hindernis1 = Hindernis()
    score = 0
    while True:
        Hindernis1.move()
        sense.clear()
        draw_player()

        draw_Hindernis(Hindernis1)

        if y == Hindernis1.y:
            if not (x == Hindernis1.Loch - 1 or x == Hindernis1.Loch or x == Hindernis1.Loch + 1):
                # Check collision with player
                sense.show_message("Game Over!", text_colour=(255, 0, 0))
                break

        else:
            score += 1
            sense.show_message(str(score))
            break

        if Hindernis1.y >= 7:
            Hindernis1 = Hindernis()

        time.sleep(0.3)


gameloop()
