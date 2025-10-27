import turtle as trtl

painter = trtl.Turtle()
painter.speed(0)
painter.pensize(10)

wn = trtl.Screen()
wn.tracer(0, 0)

start_x = -200
start_y = -150

num_floors = 63
tower_spacing = 100 

for tower in range(3): 
    x = start_x + tower * tower_spacing
    y = start_y

    for floor in range(num_floors):
        painter.penup()
        painter.goto(x, y)

        color_cycle = (floor // 3) % 3
        if color_cycle == 0:
            painter.color("red")
        elif color_cycle == 1:
            painter.color("orange")
        else:
            painter.color("yellow")

        y = y + 5

        painter.pendown()
        painter.forward(50)

wn.update()
wn.mainloop()
