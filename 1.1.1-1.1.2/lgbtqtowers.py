import turtle as trtl

painter = trtl.Turtle()
painter.speed(9)
painter.pensize(1)

wn = trtl.Screen()
wn.tracer(0, 0)
wn.colormode(1.0)

stripe_width = 80       
tower_spacing_x = stripe_width
num_towers_x = 16
base_height = 180

start_x = - (num_towers_x * tower_spacing_x) / 2
start_y = -150

pride_flags = [
    [(0.89, 0.00, 0.13), (1.00, 0.56, 0.00), (1.00, 0.98, 0.00), (0.00, 0.56, 0.00), (0.00, 0.22, 0.66), (0.56, 0.00, 0.66)],  # Rainbow
    [(0.54, 0.89, 0.98), (0.98, 0.54, 0.81), (1.00, 1.00, 1.00), (0.98, 0.54, 0.81), (0.54, 0.89, 0.98)],  # Transgender
    [(0.75, 0.04, 0.40), (0.42, 0.16, 0.62), (0.00, 0.28, 0.67)],  # Bisexual
    [(1.00, 0.20, 0.60), (1.00, 1.00, 0.00), (0.00, 0.69, 0.94)],  # Pansexual
    [(0.00, 0.00, 0.00), (0.58, 0.58, 0.58), (1.00, 1.00, 1.00), (0.56, 0.00, 0.56)],  # Asexual
    [(1.00, 1.00, 0.00), (1.00, 1.00, 1.00), (0.56, 0.00, 0.56), (0.00, 0.00, 0.00)],  # Non-binary
    [(0.89, 0.00, 0.13), (1.00, 0.56, 0.00), (1.00, 1.00, 1.00), (0.00, 0.28, 0.67), (0.42, 0.16, 0.62)],  # Lesbian
    [(0.94, 0.24, 0.32), (0.99, 0.54, 0.33), (1.00, 0.84, 0.67), (1.00, 1.00, 1.00), (0.85, 0.68, 0.75), (0.63, 0.21, 0.33), (0.50, 0.00, 0.13)],  # Genderqueer
    [(0.89, 0.00, 0.13), (1.00, 0.56, 0.00), (1.00, 0.98, 0.00), (0.00, 0.56, 0.00), (0.00, 0.22, 0.66), (0.56, 0.00, 0.66), (0.54, 0.89, 0.98)],  # Progress Pride
    [(0.00, 0.78, 0.65), (1.00, 0.00, 0.64), (0.00, 0.32, 0.92)],  # Intersex (updated colors)
    [(0.00, 0.26, 0.15), (0.55, 0.67, 0.49), (0.82, 0.82, 0.82), (1.00, 1.00, 1.00), (0.00, 0.00, 0.00)],  # Aromantic
    [(0.00, 0.00, 0.00), (0.55, 0.55, 0.55), (1.00, 1.00, 1.00), (0.43, 0.85, 0.53), (1.00, 1.00, 1.00), (0.55, 0.55, 0.55), (0.00, 0.00, 0.00)],  # Agender
    [(0.10, 0.10, 0.44), (0.22, 0.38, 0.63), (0.44, 0.71, 0.93), (0.71, 0.88, 0.96), (1.00, 1.00, 1.00)],  # Polysexual
    [(0.72, 0.25, 0.58), (0.36, 0.18, 0.29), (0.18, 0.09, 0.15)],  # Demisexual
    [(0.56, 0.00, 0.56), (0.82, 0.82, 0.82), (1.00, 1.00, 1.00), (0.00, 0.00, 0.00)],  # Genderfluid
    [(0.00, 0.53, 0.74), (0.01, 0.82, 0.89), (0.99, 0.88, 0.21), (1.00, 0.53, 0.21), (0.66, 0.31, 0.53)],  # Bigender
    [(0.94, 0.50, 0.50), (0.99, 0.90, 0.80), (1.00, 1.00, 1.00), (0.80, 0.90, 0.99), (0.50, 0.50, 0.94)]   # Graysexual
]

def draw_stripe(x, y, width, height, color):
    painter.penup()
    painter.goto(x, y)
    painter.pendown()
    painter.color(color)
    painter.fillcolor(color)
    painter.begin_fill()
    for _ in range(2):
        painter.forward(width)
        painter.left(90)
        painter.forward(height)
        painter.left(90)
    painter.end_fill()
    painter.penup()

for col in range(num_towers_x):
    x = start_x + col * tower_spacing_x
    y = start_y

    flag_colors = pride_flags[col % len(pride_flags)]
    num_stripes = len(flag_colors)
    stripe_height = base_height / num_stripes

    for i, color in enumerate(flag_colors):
        stripe_y = y + i * stripe_height
        draw_stripe(x, stripe_y, stripe_width, stripe_height, color)

wn.mainloop()
