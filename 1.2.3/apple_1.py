import turtle as trtl
import tkinter as tk

#-----setup-----

apple_image = "1.2.3/apple.gif"
background_image = "1.2.3/background.gif"

# Get screen size dynamically
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

wn = trtl.Screen()
wn.setup(width=screen_width, height=screen_height)
wn.addshape(apple_image)
wn.bgpic(background_image)

apple = trtl.Turtle()
apple.penup()

letter_writer = trtl.Turtle()
letter_writer.hideturtle()
letter_writer.penup()

falling = False  # Flag to control falling animation
gravity_speed = 5  # Pixels to move per frame
floor_y = -screen_height // 2 + 50  # Floor position to stop falling

#-----functions-----

def show_letter_once():
    x, y = apple.position()
    letter_writer.clear()
    letter_writer.goto(x + 18, y + 40)
    letter_writer.color("white")
    letter_writer.write("A", font=("Arial", 55, "bold"))
    # Clear the letter after 500 milliseconds
    wn.ontimer(letter_writer.clear, 500)

def draw_apple(active_apple):
    wn.tracer(0)
    active_apple.shape(apple_image)
    wn.update()
    wn.tracer(1)

def fall():
    global falling
    if not falling:
        return
    x, y = apple.position()
    if y > floor_y:
        wn.tracer(0)
        apple.sety(y - gravity_speed)
        wn.update()
        wn.tracer(1)
        wn.ontimer(fall, 30)
    else:
        falling = False
        letter_writer.clear()
        apple.hideturtle()

def start_fall():
    global falling
    if not falling:
        apple.showturtle()
        show_letter_once()  # Flash letter once on keypress
        falling = True
        fall()

#-----function calls-----
draw_apple(apple)

wn.listen()
wn.onkey(start_fall, "a")

wn.mainloop()
