import turtle as trtl

painter = trtl.Turtle()
painter.pensize(40)
painter.circle(20)

num_spokes = 8  # Number of legs
line_length = 70 # Making legs same length
angle_increment = 360 / num_spokes  # Equal spacing

painter.pensize(5)

current_spoke = 0
while current_spoke < num_spokes:
  angle = angle_increment * current_spoke
  print(f"Iteration {current_spoke + 1}: current_spoke={current_spoke}, angle_increment={angle_increment:.4f}, angle={angle:.4f}")
  
  painter.penup()
  painter.goto(0, 20)
  painter.pendown()
  painter.setheading(angle)
  painter.forward(line_length)
  
  current_spoke += 1


# Eye Code
painter.penup()
painter.goto(-7, 30)
painter.pendown()
painter.pensize(10)
painter.dot(10, "white")

painter.penup()
painter.goto(7, 30)
painter.pendown()
painter.dot(10, "white")

# End Code
painter.hideturtle()
wn = trtl.Screen()
wn.mainloop()
