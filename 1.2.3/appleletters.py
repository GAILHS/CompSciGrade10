import turtle as trtl
import tkinter as tk
import random

#-----setup-----

apple_image = "1.2.3/apple.gif"
background_image = "1.2.3/background.gif"
letters = list("abcdef")  # Adjust letters as needed
number_of_apples = len(letters)

# Carefully spaced apple positions moved down by 30 pixels for better tree placement
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

gravity_speed = 5  # Pixels per frame
floor_y = -screen_height // 2 + 50  # Floor position

#-----globals-----

apples = []
letters_on_screen = {}  # Map apple to its letter_writer turtle

#-----functions-----

def reset_apple(apple, letters, apple_positions):
    if letters:
        letter_index = random.randint(0, len(letters) - 1)
        letter = letters[letter_index]
        # Choose a position not currently used by other apples
        used_positions = [a.position() for a in apples if a != apple]
        available_positions = [pos for pos in apple_positions if pos not in used_positions]
        pos = random.choice(available_positions) if available_positions else random.choice(apple_positions)
        apple.goto(pos)
        apple.letter = letter
        apple.letter_index = letter_index
        apple.showturtle()
        return letter
    return None

def draw_letter_on_apple(apple, letter_writer):
    x, y = apple.position()
    letter_writer.clear()
    # Draw letter slightly above apple center for visibility
    letter_writer.goto(x, y + 10)
    letter_writer.color("white")
    letter_writer.write(apple.letter.upper(), align="center", font=("Arial", 28, "bold"))

def draw_apple(apple, wn):
    wn.tracer(0)
    apple.shape(apple_image)
    draw_letter_on_apple(apple, letters_on_screen[apple])
    wn.update()
    wn.tracer(1)

def drop_apple(letter):
    for apple in apples:
        if apple.letter == letter:
            falling = True
            def fall():
                nonlocal falling
                if not falling:
                    return
                x, y = apple.position()
                if y > floor_y:
                    wn.tracer(0)
                    apple.sety(y - gravity_speed)
                    draw_letter_on_apple(apple, letters_on_screen[apple])
                    wn.update()
                    wn.tracer(1)
                    wn.ontimer(fall, 30)
                else:
                    falling = False
                    letters_on_screen[apple].clear()
                    apple.hideturtle()
                    # Reset apple after falling
                    reset_apple(apple, letters, apple_positions)
                    draw_apple(apple, wn)
            fall()
            break

# Define drop functions for each letter
def drop_a(): drop_apple("a")
def drop_b(): drop_apple("b")
def drop_c(): drop_apple("c")
def drop_d(): drop_apple("d")
def drop_e(): drop_apple("e")
def drop_f(): drop_apple("f")

#-----initialize apples-----

for i in range(number_of_apples):
    apple = trtl.Turtle()
    apple.penup()
    apple.speed(0)
    reset_apple(apple, letters, apple_positions)
    apples.append(apple)
    # Create a separate turtle to write the letter for each apple
    letter_writer = trtl.Turtle()
    letter_writer.hideturtle()
    letter_writer.penup()
    letters_on_screen[apple] = letter_writer

# Draw all apples initially
for apple in apples:
    draw_apple(apple, wn)

#-----key bindings-----

wn.listen()
wn.onkeypress(drop_a, "a")
wn.onkeypress(drop_b, "b")
wn.onkeypress(drop_c, "c")
wn.onkeypress(drop_d, "d")
wn.onkeypress(drop_e, "e")
wn.onkeypress(drop_f, "f")

wn.mainloop()
