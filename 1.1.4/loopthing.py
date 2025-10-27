import turtle as trtl

color1 = "orange"
color2 = "purple"

wn = trtl.Screen()
width = 400
height = 300

painter = trtl.Turtle()
painter.speed(0)
painter.color(color1)

answer = "y"
while answer == "y":
    wn.clearscreen()  
    painter = trtl.Turtle()  # Reset turtle after clearscreen
    painter.speed(0)
    painter.penup()
    painter.goto(0, 0)
    painter.pendown()

    angle = int(input("angle:"))
    seg = int(360 / angle)

    space = 1
    current_color = color1

    while painter.ycor() < height:
        # Draw 100 steps with current_color
        for _ in range(100):
            if painter.ycor() >= height:
                break
            painter.fillcolor(current_color)
            painter.color(current_color)

            painter.right(angle)
            painter.forward(2 * space + 10)
            painter.begin_fill()
            painter.circle(3)
            painter.end_fill()

            space += 1

        # Switch color after 100 steps
        if current_color == color1:
            current_color = color2
        else:
            current_color = color1

    answer = input("again?")

wn.bye()
