import turtle
import random

def random_hex_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("#202020")  # Dark background to highlight colors

# Create turtle
t = turtle.Turtle()
t.speed(0)  # Fastest
t.pensize(2)

# Number of colors and steps
num_colors = 10
colors = [random_hex_color() for _ in range(num_colors)]

# Draw a colorful spiral star
for i in range(360):
    t.color(colors[i % num_colors])
    t.forward(i * 3 / num_colors + i)
    t.right(59)

turtle.done()
