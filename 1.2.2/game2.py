import turtle as trtl
import random
import os

#-----game configuration variables-----
shape_size = 2
shape_shape = "circle"

background_color = "lightblue"
colors = ["red", "orange", "yellow", "green", "blue", "purple", "magenta"]
# Exclude the background color (if present)
colors = [c for c in colors if c.lower() != background_color.lower()]
sizes = [0.5, 1, 1.5, 2, 2.5, 3]

#-----countdown variables-----
font_setup = ("Arial", 20, "normal")
initial_timer = 3.0  # seconds for countdown (float for tenths)
counter_interval = 100  # 100 ms = 0.1 second
timer = initial_timer
timer_up = False

#-----screen setup-----
wn = trtl.Screen()
wn.title("Click the Shape Game")
wn.bgcolor(background_color)
wn.setup(width=1.0, height=1.0)  # fullscreen

# Turn off automatic screen updates
wn.tracer(0)

#-----game variables-----
score = 0
timer_running = False

#-----player name input-----
player_name = wn.textinput("Player Name", "Please enter your name:")

#-----turtle setup-----
player_turtle = trtl.Turtle()
player_turtle.shape(shape_shape)
player_turtle.penup()
player_turtle.speed(0)
player_turtle.shapesize(stretch_wid=shape_size, stretch_len=shape_size)

#-----score display-----
score_turtle = trtl.Turtle()
score_turtle.hideturtle()
score_turtle.penup()
score_turtle.goto(0, wn.window_height()//2 - 60)

#-----countdown writer-----
counter = trtl.Turtle()
counter.hideturtle()
counter.penup()
counter.goto(0, wn.window_height()//2 - 100)

#-----leaderboard writer-----
leaderboard_turtle = trtl.Turtle()
leaderboard_turtle.hideturtle()
leaderboard_turtle.penup()
leaderboard_turtle.goto(0, -30)

LEADERBOARD_FILE = "leaderboard.txt"
MAX_LEADERS = 5  # max top scores to keep

def update_score():
    score_turtle.clear()
    score_turtle.write(f"Score: {score}", align="center", font=("Arial", 24, "normal"))
    wn.update()

def move_turtle_random():
    width = wn.window_width() // 2 - 40
    height = wn.window_height() // 2 - 140  # leave space for timer and score
    x = random.randint(-width, width)
    y = random.randint(-height, height)
    player_turtle.goto(x, y)
    wn.update()

def load_leaderboard():
    leaderboard = []
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) == 2:
                        name, score_str = parts
                        try:
                            score_val = int(score_str)
                            leaderboard.append((name, score_val))
                        except ValueError:
                            pass
    # Sort leaderboard descending by score
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    return leaderboard

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as f:
        for name, score_val in leaderboard[:MAX_LEADERS]:
            f.write(f"{name},{score_val}\n")

def update_leaderboard():
    global score, player_name
    leaderboard = load_leaderboard()
    # Check if current score qualifies
    if len(leaderboard) < MAX_LEADERS or score >= leaderboard[-1][1]:
        # Insert score in correct position
        inserted = False
        for i, (_, s) in enumerate(leaderboard):
            if score >= s:
                leaderboard.insert(i, (player_name, score))
                inserted = True
                break
        if not inserted:
            leaderboard.append((player_name, score))
        # Keep only top MAX_LEADERS
        leaderboard = leaderboard[:MAX_LEADERS]
        save_leaderboard(leaderboard)
    return leaderboard

def display_leaderboard(leaderboard):
    leaderboard_turtle.clear()
    leaderboard_turtle.goto(0, -80)  # lowered to avoid overlap with game over text
    leaderboard_turtle.write("Leaderboard:", align="center", font=("Arial", 26, "bold"))
    y_offset = -110  # start below the title
    for i, (name, s) in enumerate(leaderboard, start=1):
        leaderboard_turtle.goto(0, y_offset)
        leaderboard_turtle.write(f"{i}. {name} - {s}", align="center", font=("Arial", 20, "normal"))
        y_offset -= 30
    wn.update()

def game_over():
    global timer_running
    timer_running = False
    player_turtle.hideturtle()
    counter.clear()
    counter.goto(0, 0)
    counter.write("Time's Up! Game Over.", align="center", font=("Arial", 30, "bold"))
    # Update and show leaderboard
    leaderboard = update_leaderboard()
    display_leaderboard(leaderboard)
    wn.update()

def countdown():
    global timer, timer_up, timer_running
    if not timer_running:
        return  # stop countdown if game is over
    counter.clear()
    if timer <= 0:
        timer_up = True
        game_over()
    else:
        counter.write(f"Timer: {timer:.1f} s", font=font_setup)
        timer -= 0.1
        wn.ontimer(countdown, counter_interval)
    wn.update()

def get_new_color():
    return random.choice(colors)

def respawn_turtle():
    new_color = get_new_color()
    player_turtle.color(new_color)
    new_size = random.choice(sizes)
    player_turtle.shapesize(stretch_wid=new_size, stretch_len=new_size)
    move_turtle_random()
    player_turtle.showturtle()
    wn.update()

def on_turtle_click(x, y):
    global score, timer, timer_running, timer_up
    if timer_running and not timer_up:
        player_turtle.hideturtle()  # vanish immediately on click
        score += 1
        update_score()
        timer = initial_timer  # reset timer on click
        counter.clear()
        counter.write(f"Timer: {timer:.1f} s", font=font_setup)
        wn.ontimer(respawn_turtle, 300)  # wait 300ms before respawn
        wn.update()

def start_game():
    global score, timer, timer_running, timer_up
    score = 0
    timer = initial_timer
    timer_up = False
    timer_running = True
    update_score()
    counter.clear()
    counter.write(f"Timer: {timer:.1f} s", font=font_setup)
    player_turtle.color(get_new_color())
    player_turtle.shapesize(stretch_wid=random.choice(sizes), stretch_len=random.choice(sizes))
    move_turtle_random()
    player_turtle.showturtle()
    wn.ontimer(countdown, counter_interval)
    wn.update()

player_turtle.onclick(on_turtle_click)
start_game()
wn.mainloop()
