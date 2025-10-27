import turtle as trtl
import math


painter = trtl.Turtle()
painter.speed(9)
painter.pensize(1)

wn = trtl.Screen()
wn.tracer(0, 0)

# Repeat shapes and colors 4 times for more turtles
base_shapes = ["arrow", "turtle", "circle", "square", "triangle", "classic"]
base_colors = ["red", "blue", "green", "orange", "purple", "gold"]

turtle_shapes = base_shapes * 4  # 24 turtles
initial_colors = base_colors * 4

# Create turtles
my_turtles = []
turtle_colors = initial_colors.copy()
for s in turtle_shapes:
    t = trtl.Turtle(shape=s)
    color = turtle_colors.pop(0)
    t.fillcolor(color)
    t.pencolor(color)
    t.penup()
    my_turtles.append(t)

startx = 0
starty = 0
radius_increment = 20  # larger step for longer spiral
angle_increment = 360 / len(my_turtles)

positions = []

# Position turtles in a spiral outward
for i, t in enumerate(my_turtles):
    radius = radius_increment * i
    angle = angle_increment * i
    t.goto(startx, starty)
    t.setheading(angle)
    t.forward(radius)
    positions.append(t.position())

# Create line drawers for each connecting line
line_drawers = []
for _ in range(len(my_turtles)):
    ld = trtl.Turtle(visible=False)
    ld.penup()
    ld.pensize(3)
    line_drawers.append(ld)

colors = initial_colors
colors_len = len(colors)
index_offset = 0
delay_ms = 150  # update interval in milliseconds

def update_colors():
    global index_offset
    # Update turtle colors
    for i, t in enumerate(my_turtles):
        color_index = (i + index_offset) % colors_len
        new_color = colors[color_index]
        t.fillcolor(new_color)
        t.pencolor(new_color)

    # Update line colors and redraw lines
    for i, ld in enumerate(line_drawers):
        start_pos = positions[i]
        end_pos = positions[(i + 1) % len(my_turtles)]
        color_index = (i + index_offset) % colors_len
        line_color = colors[color_index]
        ld.clear()
        ld.pencolor(line_color)
        ld.goto(start_pos)
        ld.pendown()
        ld.goto(end_pos)
        ld.penup()

    # Set headings of turtles toward next clockwise turtle
    for i, t in enumerate(my_turtles):
        next_index = (i + 1) % len(my_turtles)
        next_pos = positions[next_index]
        current_pos = positions[i]
        dx = next_pos[0] - current_pos[0]
        dy = next_pos[1] - current_pos[1]
        heading_angle = math.degrees(math.atan2(dy, dx))
        t.setheading(heading_angle)

    index_offset = (index_offset + 1) % colors_len
    trtl.ontimer(update_colors, delay_ms)

# Start animation
update_colors()

trtl.done()
