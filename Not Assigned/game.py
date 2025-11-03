import turtle
import random
import time

# Screen setup - fullscreen
screen = turtle.Screen()
screen.title("Dino Game")
screen.bgcolor("#87CEEB")  # Sky blue
screen.setup(width=1.0, height=1.0)  # Fullscreen window
screen.tracer(0)

# Ground line
ground = turtle.Turtle()
ground.hideturtle()
ground.penup()
ground.goto(-screen.window_width()//2, -120)
ground.pendown()
ground.color("#654321")  # Brown ground line
ground.pensize(5)
ground.forward(screen.window_width())

# Dino setup
dino = turtle.Turtle()
dino.shape("square")
dino.color("green")
dino.penup()
dino.goto(-screen.window_width()//3, -100)
dino.dy = 0
gravity = -0.6
jump_speed = 14
ground_level = -100
is_jumping = False

# Obstacle setup
obstacle = turtle.Turtle()
obstacle.shape("square")
obstacle.color("#8B0000")  # Dark red
obstacle.shapesize(stretch_wid=3, stretch_len=2)
obstacle.penup()
obstacle.goto(screen.window_width()//2, -100)
base_speed = 6
obstacle.speed = base_speed

# Score display
score = 0
score_display = turtle.Turtle()
score_display.hideturtle()
score_display.penup()
score_display.goto(screen.window_width()//3, screen.window_height()//3 - 40)
score_display.color("black")
score_display.write(f"Score: {score}", align="center", font=("Arial", 24, "bold"))

# Clouds setup
clouds = []
num_clouds = 5
cloud_colors = ["#ffffff", "#f0f8ff", "#e0ffff"]

for _ in range(num_clouds):
    c = turtle.Turtle()
    c.shape("circle")
    c.color(random.choice(cloud_colors))
    c.shapesize(stretch_wid=2, stretch_len=4)
    c.penup()
    c.goto(random.randint(-screen.window_width()//2, screen.window_width()//2),
           random.randint(50, screen.window_height()//3))
    clouds.append(c)

# Functions
def jump():
    global is_jumping
    if not is_jumping and dino.ycor() <= ground_level:
        dino.dy = jump_speed
        is_jumping = True

def update_score():
    global score, base_speed
    score += 1
    score_display.clear()
    score_display.write(f"Score: {score}", align="center", font=("Arial", 24, "bold"))
    obstacle.speed = min(base_speed + score * 0.4, 25)

def reset_obstacle():
    obstacle.goto(screen.window_width()//2, -100)

def game_over():
    screen.clear()
    screen.bgcolor("black")
    screen.title("Game Over")
    game_over_turtle = turtle.Turtle()
    game_over_turtle.color("white")
    game_over_turtle.hideturtle()
    game_over_turtle.write(f"Game Over! Final Score: {score}", align="center", font=("Arial", 36, "bold"))

# Keyboard binding
screen.listen()
screen.onkey(jump, "space")

# Main game loop
while True:
    screen.update()

    # Move clouds slowly left
    for c in clouds:
        c.setx(c.xcor() - 1)
        if c.xcor() < -screen.window_width()//2 - 50:
            c.goto(screen.window_width()//2 + 50, random.randint(50, screen.window_height()//3))

    # Dino physics
    dino.dy += gravity
    new_y = dino.ycor() + dino.dy

    if new_y < ground_level:
        new_y = ground_level
        dino.dy = 0
        is_jumping = False

    dino.sety(new_y)

    # Move obstacle left
    obstacle.setx(obstacle.xcor() - obstacle.speed)

    # When obstacle goes off screen, reset it and increase score
    if obstacle.xcor() < -screen.window_width()//2:
        reset_obstacle()
        update_score()

    # Collision detection (simple box collision)
    dino_x, dino_y = dino.xcor(), dino.ycor()
    obs_x, obs_y = obstacle.xcor(), obstacle.ycor()

    if abs(obs_x - dino_x) < 40 and abs(obs_y - dino_y) < 50:
        if dino_y < (ground_level + 40):
            game_over()
            break

    time.sleep(0.017)  # ~60 FPS

screen.mainloop()
