import turtle as trtl
import random

painter = trtl.Turtle()
painter.speed(9)
painter.pensize(10)

wn = trtl.Screen()
wn.tracer(0, 0)

wn = trtl.Screen()
wn.colormode(1.0)

start_x = -300
start_y = -150

tower_spacing_x = 70 
num_towers_x = 7

base_height = 63 

def random_color():
    return (random.random(), random.random(), random.random())

row = 0  # only one row
for col in range(num_towers_x):
    x = start_x + col * tower_spacing_x
    y = start_y

    
    num_floors = base_height + random.randint(-5, 5)

    for floor in range(num_floors):
        painter.penup()
        painter.goto(x, y + floor * 5)
        painter.color(random_color())
        painter.pendown()
        painter.forward(50)
        painter.penup()

wn.mainloop()
