import turtle as trtl

painter = trtl.Turtle()
painter.penup()
painter.goto(-200, 0)
painter.pendown()

x = -200
y = 0
move_x = 1
move_y = 1

peak_count = 0  # Count how many peaks drawn

while peak_count < 2:  # Draw 2 peaks
    # Move up
    while y < 100:
        x = x + move_x
        y = y + move_y
        painter.goto(x, y)
    move_y = -1

    # Move down
    while y > 0:
        x = x + move_x
        y = y + move_y
        painter.goto(x, y)
    move_y = 1

    peak_count += 1  # One peak (up and down) completed

wn = trtl.Screen()
wn.mainloop()
