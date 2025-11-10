import turtle as trtl

wn = trtl.Screen()
wn.setup(width=1.0, height=1.0)

drawer = trtl.Turtle()

# This function takes care of font and color.
def draw_an_A():
  drawer.color("blue")
  drawer.write("A", font=("Arial", 74, "bold")) 

# This call to the onkeypress function sets draw_an_A as the function
# that will be called when the "a" key is pressed.
wn.onkeypress(draw_an_A, "a")

wn.listen()

wn.mainloop()