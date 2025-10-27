import turtle as trtl

painter = trtl.Turtle()
painter.speed(0)

for i in range(0):
    painter.forward(100)

while True:
    painter.circle(50)
    painter.right(10)

wn = trtl.Screen()
wn.mainloop()
