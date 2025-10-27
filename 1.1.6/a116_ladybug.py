import turtle as trtl

ladybug = trtl.Turtle()

# Parameters
body_center_x = 0
body_center_y = -35
body_radius = 20
red_pensize = 40
head_radius = 5
leg_length = 50
num_legs = 6
angle_increment = 360 / num_legs

# Draw legs starting exactly at body center
ladybug.pensize(5)
for i in range(num_legs):
    angle = angle_increment * i
    ladybug.penup()
    ladybug.goto(body_center_x, body_center_y)  # Legs start at body center
    ladybug.setheading(angle)
    ladybug.pendown()
    ladybug.forward(leg_length)

# Draw body circle centered at (body_center_x, body_center_y)
ladybug.penup()
ladybug.goto(body_center_x, body_center_y - body_radius)
ladybug.setheading(0)
ladybug.color("red")
ladybug.pensize(red_pensize)
ladybug.pendown()
ladybug.circle(body_radius)

# Draw center black line splitting the full visible body in half
line_length = 2 * (body_radius + red_pensize / 2)
ladybug.penup()
ladybug.goto(body_center_x, body_center_y + body_radius + red_pensize / 2)  # Top edge including pen thickness
ladybug.setheading(270)  # Downward
ladybug.color("black")
ladybug.pensize(2)
ladybug.pendown()
ladybug.forward(line_length)

# Draw smaller black dots on body relative to center
ladybug.pensize(10)
dot_positions = [
    (body_center_x - 15, body_center_y - 5), (body_center_x - 8, body_center_y - 22),
    (body_center_x + 15, body_center_y - 10), (body_center_x + 8, body_center_y - 28),
    (body_center_x - 12, body_center_y + 7), (body_center_x + 7, body_center_y + 10),
    (body_center_x - 10, body_center_y + 15), (body_center_x + 13, body_center_y + 18)
]
ladybug.color("black")
for pos in dot_positions:
    ladybug.penup()
    ladybug.goto(pos)
    ladybug.pendown()
    ladybug.dot(7)

# Draw head centered above body circle
ladybug.penup()
ladybug.goto(body_center_x, body_center_y + body_radius + head_radius)
ladybug.setheading(0)
ladybug.color("black")
ladybug.pensize(40)
ladybug.pendown()
ladybug.circle(head_radius)

ladybug.hideturtle()
wn = trtl.Screen()
wn.mainloop()
