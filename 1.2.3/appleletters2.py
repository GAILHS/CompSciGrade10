import turtle as trtl
import tkinter as tk
import random

#-----setup-----

apple_image = "1.2.3/apple.gif"
background_image = "1.2.3/background.gif"
letters = list("abcdef")  # Letters to use
number_of_apples = len(letters)

# Positions on the tree for apples (x, y)
apple_positions = [(-180, 90), (-90, 110), (0, 130), (90, 110), (180, 90), (-45, 150)]

# Get screen size dynamically
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

wn = trtl.Screen()
wn.setup(width=screen_width, height=screen_height)
wn.addshape(apple_image)
wn.bgpic(background_image)

gravity_speed = 5
floor_y = -screen_height // 2 + 50

#-----globals-----

apples = []
letters_on_screen = {}  # Maps each apple to its letter_writer turtle

#-----functions-----

# 1. Reset apple to a new random location on the tree if letters list not empty
def reset_apple(apple):
    if letters:
        pos = random.choice(apple_positions)
        apple.goto(pos)
        apple.showturtle()
        return True
    return False

# 2. Draw a new letter from the letters list at given position (used for letter_writer)
def draw_letter(letter_writer, letter, position):
    letter_writer.clear()
    letter_writer.goto(position[0], position[1] + 10)  # Slightly above apple center
    letter_writer.color("white")
    letter_writer.write(letter.upper(), align="center", font=("Arial", 28, "bold"))

# 3. Set turtle shape, draw letter, update screen
def draw_apple(apple, letter_writer, letter):
    wn.tracer(0)
    apple.shape(apple_image)
    draw_letter(letter_writer, letter, apple.position())
    wn.update()
    wn.tracer(1)

# 4. Create apples, reset their positions, add to apples list
for i in range(number_of_apples):
    apple = trtl.Turtle()
    apple.penup()
    apple.speed(0)
    reset_apple(apple)
    apples.append(apple)
    letter_writer = trtl.Turtle()
    letter_writer.hideturtle()
    letter_writer.penup()
    letters_on_screen[apple] = letter_writer

# Assign letters randomly to apples and draw them
def assign_letters_and_draw():
    # Shuffle letters so they assign randomly
    shuffled_letters = letters[:]
    random.shuffle(shuffled_letters)
    for apple, letter in zip(apples, shuffled_letters):
        draw_apple(apple, letters_on_screen[apple], letter)
        apple.assigned_letter = letter

assign_letters_and_draw()

# 5. Drop a random apple and letter with given letter parameter, then reset apple
def drop_apple(letter):
    # Find all apples assigned this letter that are currently visible
    candidates = [a for a in apples if getattr(a, 'assigned_letter', None) == letter and a.isvisible()]
    if not candidates:
        return
    apple = random.choice(candidates)

    falling = True
    def fall():
        nonlocal falling
        if not falling:
            return
        x, y = apple.position()
        if y > floor_y:
            wn.tracer(0)
            apple.sety(y - gravity_speed)
            # Move letter_writer with apple but clear letter to simulate disappearance
            letters_on_screen[apple].clear()
            wn.update()
            wn.tracer(1)
            wn.ontimer(fall, 30)
        else:
            falling = False
            apple.hideturtle()
            letters_on_screen[apple].clear()
            # Reset apple position and redraw letter
            reset_apple(apple)
            draw_apple(apple, letters_on_screen[apple], letter)

    fall()

# 6. Define one function per letter that drops a random apple with that letter
def drop_a():
    if "a" in letters:
        drop_apple("a")

def drop_b():
    if "b" in letters:
        drop_apple("b")

def drop_c():
    if "c" in letters:
        drop_apple("c")

def drop_d():
    if "d" in letters:
        drop_apple("d")

def drop_e():
    if "e" in letters:
        drop_apple("e")

def drop_f():
    if "f" in letters:
        drop_apple("f")

# 7. Bind these functions to keypresses
wn.listen()
wn.onkeypress(drop_a, "a")
wn.onkeypress(drop_b, "b")
wn.onkeypress(drop_c, "c")
wn.onkeypress(drop_d, "d")
wn.onkeypress(drop_e, "e")
wn.onkeypress(drop_f, "f")

# Start main loop
trtl.mainloop()
