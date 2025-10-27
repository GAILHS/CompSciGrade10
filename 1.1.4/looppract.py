import turtle as trtl

color1 = "orange"
color2 = "purple"

wn = trtl.Screen()
height = 250

painter = trtl.Turtle()
painter.speed(0)
painter.color(color1)

space = 1
angle = 45
seg = int(360 / angle)

while painter.distance(0, 0) < height:
    if space % 5 == 0:
        
        if painter.color()[0] == color1:
            painter.color(color2)
            painter.fillcolor(color2)
        else:
            painter.color(color1)
            painter.fillcolor(color1)

    painter.right(angle)
    painter.forward(2 * space + 10)
    painter.begin_fill()
    painter.circle(3)
    painter.end_fill()
    space += 1

wn.mainloop()
