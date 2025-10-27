import turtle as trtl
import random

# Constants
COLLISION_DISTANCE = 20
MAX_SPEED = 20
MIN_SPEED = 2
SPEED_INCREMENT = 0.5
BACKUP_DISTANCE = 30
LEFT_BOUND = -380
RIGHT_BOUND = 380
TOP_BOUND = 380
BOTTOM_BOUND = -380

# Collision indicator shape and color (simulate explosion)
collision_shape = "circle"
collision_color = "red"
collision_size = 3  # scaled up size for explosion effect
deactivated_color = "gray"

# Initialize turtles and properties
horiz_turtles = []
vert_turtles = []

# Added more shapes including some standard turtle shapes
turtle_shapes = [
    "arrow", "turtle", "circle", "square", "triangle", "classic"
]

# Expanded color lists to match extra shapes
horiz_colors = ["red", "blue", "green", "orange", "purple", "gold"]
vert_colors = ["darkred", "darkblue", "lime", "salmon", "indigo", "brown"]

tloc = 50
for s in turtle_shapes:
    ht = trtl.Turtle(shape=s)
    ht.penup()
    new_color = horiz_colors.pop()
    ht.fillcolor(new_color)
    ht.goto(LEFT_BOUND, tloc)
    ht.setheading(0)  # Face right
    ht.speed_value = random.uniform(MIN_SPEED, MAX_SPEED / 2)
    ht.original_shape = s
    ht.original_color = new_color
    horiz_turtles.append(ht)

    vt = trtl.Turtle(shape=s)
    vt.penup()
    new_color = vert_colors.pop()
    vt.fillcolor(new_color)
    vt.goto(-tloc, TOP_BOUND - 40)
    vt.setheading(270)  # Face down
    vt.speed_value = random.uniform(MIN_SPEED, MAX_SPEED / 2)
    vt.original_shape = s
    vt.original_color = new_color
    vert_turtles.append(vt)

    tloc += 50

steps = 100

def move_turtle(t, direction):
    t.speed_value += SPEED_INCREMENT
    if t.speed_value > MAX_SPEED:
        t.speed_value = MIN_SPEED

    if direction == 'horizontal':
        new_x = t.xcor() + t.speed_value
        if new_x > RIGHT_BOUND:
            new_x = RIGHT_BOUND
        t.goto(new_x, t.ycor())
    else:
        new_y = t.ycor() - t.speed_value
        if new_y < BOTTOM_BOUND:
            new_y = BOTTOM_BOUND
        t.goto(t.xcor(), new_y)

def check_collision(ht, vt):
    x_dist = abs(ht.xcor() - vt.xcor())
    y_dist = abs(ht.ycor() - vt.ycor())
    return (x_dist < COLLISION_DISTANCE) and (y_dist < COLLISION_DISTANCE)

def handle_collision(ht, vt):
    ht.shape(collision_shape)
    vt.shape(collision_shape)
    ht.fillcolor(collision_color)
    vt.fillcolor(collision_color)
    ht.shapesize(collision_size)
    vt.shapesize(collision_size)
    ht.backward(BACKUP_DISTANCE)
    vt.backward(BACKUP_DISTANCE)
    ht.shape(ht.original_shape)
    vt.shape(vt.original_shape)
    ht.fillcolor(ht.original_color)
    vt.fillcolor(vt.original_color)
    ht.shapesize(1)
    vt.shapesize(1)

for step in range(steps):
    for ht in horiz_turtles:
        move_turtle(ht, 'horizontal')
    for vt in vert_turtles:
        move_turtle(vt, 'vertical')
    for ht in horiz_turtles:
        for vt in vert_turtles:
            if check_collision(ht, vt):
                handle_collision(ht, vt)

for t in horiz_turtles:
    t.fillcolor(deactivated_color)
for t in vert_turtles:
    t.fillcolor(deactivated_color)

wn = trtl.Screen()
wn.mainloop()
