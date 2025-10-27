import turtle as trtl

painter = trtl.Turtle()
painter.speed(0)
painter.hideturtle()
painter.pensize(5)

# Parameters
body_radius = 40
leg_length = 120
leg_curvature = 60  # degrees for leg arcs
body_center = (0, 0)

# Draw solid black spider body (filled circle)
painter.penup()
painter.goto(body_center[0], body_center[1] - body_radius)
painter.pendown()
painter.color("black")
painter.begin_fill()
painter.circle(body_radius)
painter.end_fill()

# Draw eight curved legs (4 on each side)
painter.pensize(7)
painter.color("black")

# Function to draw a curved leg starting from body edge
def draw_leg(start_x, start_y, heading, curve_direction):
    painter.penup()
    painter.goto(start_x, start_y)
    painter.setheading(heading)
    painter.pendown()
    # Draw a curved leg as an arc
    # curve_direction: 1 for left curve, -1 for right curve
    painter.circle(curve_direction * leg_length / 2, leg_curvature)
    painter.forward(leg_length / 2)

# Calculate leg start positions on body edge
# Legs start roughly at angles 45, 75, 105, 135 degrees on each side from vertical
angles_left = [135, 105, 75, 45]
angles_right = [45, 75, 105, 135]

for angle in angles_left:
    # Convert angle to start position on left side edge of circle
    rad = angle * 3.14159 / 180
    start_x = body_center[0] + body_radius * -1 * (3.14159 / 180) * 0 # placeholder, better to use trig
    # Correct calculation with trig:
    import math
    start_x = body_center[0] + body_radius * math.cos(math.radians(angle))
    start_y = body_center[1] + body_radius * math.sin(math.radians(angle))
    draw_leg(start_x, start_y, angle - 90, 1)  # curve left

for angle in angles_right:
    # For right legs, mirror horizontally by using negative cosine
    import math
    start_x = body_center[0] + body_radius * math.cos(math.radians(-angle))
    start_y = body_center[1] + body_radius * math.sin(math.radians(-angle))
    # legs curve to the right (negative curve_direction)
    draw_leg(start_x, start_y, -angle - 90, -1)

# Draw small rounded purple area under body with two small loops inside
painter.penup()
painter.goto(body_center[0], body_center[1] - body_radius - 20)
painter.color("purple")
painter.pensize(3)
painter.pendown()
painter.begin_fill()
painter.circle(20)
painter.end_fill()

# Draw two small purple loops/ovals inside the purple area (mouth features)
painter.penup()
painter.goto(body_center[0] - 10, body_center[1] - body_radius - 15)
painter.pendown()
painter.pensize(5)
painter.color("purple")
# Draw left loop
painter.circle(5, 360)

painter.penup()
painter.goto(body_center[0] + 10, body_center[1] - body_radius - 15)
painter.pendown()
# Draw right loop
painter.circle(5, 360)

# Finish up
wn = trtl.Screen()
wn.bgcolor("white")
wn.mainloop()
