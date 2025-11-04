import turtle as trtl
import random
import os

# ----- leaderboard.py code -----

bronze_score = 15
silver_score = 20
gold_score = 25

def get_names(file_name):
    if not os.path.exists(file_name):
        open(file_name, "w").close()
    with open(file_name, "r") as leaderboard_file:
        names = []
        for line in leaderboard_file:
            leader_name = ""
            index = 0
            while index < len(line) and line[index] != ",":
                leader_name += line[index]
                index += 1
            names.append(leader_name)
    return names

def get_scores(file_name):
    if not os.path.exists(file_name):
        open(file_name, "w").close()
    with open(file_name, "r") as leaderboard_file:
        scores = []
        for line in leaderboard_file:
            leader_score = ""
            index = 0
            while index < len(line) and line[index] != ",":
                index += 1
            index += 1
            while index < len(line) and line[index] != "\n":
                leader_score += line[index]
                index += 1
            try:
                scores.append(int(leader_score))
            except ValueError:
                pass
    return scores

def update_leaderboard(file_name, leader_names, leader_scores, player_name, player_score):
    index = 0
    for i in range(len(leader_scores)):
        if player_score >= leader_scores[i]:
            index = i
            break
        else:
            index = i + 1
    leader_names.insert(index, player_name)
    leader_scores.insert(index, player_score)
    leader_names = leader_names[:5]
    leader_scores = leader_scores[:5]
    with open(file_name, "w") as leaderboard_file:
        for i in range(len(leader_names)):
            leaderboard_file.write(leader_names[i] + "," + str(leader_scores[i]) + "\n")
    return leader_names, leader_scores

def draw_leaderboard(high_scorer, leader_names, leader_scores, turtle_object, player_name, player_score):
    font_setup = ("Arial", 20, "normal")
    turtle_object.clear()
    turtle_object.penup()
    turtle_object.goto(-160, 100)
    turtle_object.hideturtle()
    turtle_object.pendown()

    player_rank = None
    for index in range(len(leader_names)):
        entry = f"{index + 1}. {leader_names[index]:<10} {leader_scores[index]}"
        turtle_object.write(entry, font=font_setup)
        turtle_object.penup()
        turtle_object.goto(-160, int(turtle_object.ycor()) - 50)
        turtle_object.pendown()
        if high_scorer and leader_names[index] == player_name and leader_scores[index] == player_score:
            player_rank = index + 1  # ranks start at 1

    turtle_object.penup()
    turtle_object.goto(-160, int(turtle_object.ycor()) - 50)
    turtle_object.pendown()

    if high_scorer:
        turtle_object.write("Congratulations!\nYou made the leaderboard!", font=font_setup)
    else:
        turtle_object.write("Sorry!\nYou didn't make the leaderboard.\nMaybe next time!", font=font_setup)

    turtle_object.penup()
    turtle_object.goto(-160, int(turtle_object.ycor()) - 50)
    turtle_object.pendown()

    if player_rank == 1:
        turtle_object.write("You earned a gold medal!", font=font_setup)
    elif player_rank == 2:
        turtle_object.write("You earned a silver medal!", font=font_setup)
    elif player_rank == 3:
        turtle_object.write("You earned a bronze medal!", font=font_setup)

# ----- End leaderboard.py code -----

# Game config
shape_size = 2
shape_shape = "circle"

background_color = "lightblue"
colors = [c for c in ["red", "orange", "yellow", "green", "blue", "purple", "magenta"] if c.lower() != background_color.lower()]
sizes = [0.5, 1, 1.5, 2, 2.5, 3]

font_setup = ("Arial", 20, "normal")
initial_timer = 3.0
counter_interval = 100

wn = trtl.Screen()
wn.title("Click the Shape Game")
wn.bgcolor(background_color)
wn.setup(width=1.0, height=1.0)
wn.tracer(0)

score = 0
timer_running = False
timer = initial_timer
timer_up = False

player_name = wn.textinput("Player Name", "Please enter your name:")
if not player_name:
    player_name = "Player"

player_turtle = trtl.Turtle()
player_turtle.shape(shape_shape)
player_turtle.penup()
player_turtle.speed(0)
player_turtle.shapesize(stretch_wid=shape_size, stretch_len=shape_size)

score_turtle = trtl.Turtle()
score_turtle.hideturtle()
score_turtle.penup()
score_turtle.goto(0, wn.window_height() // 2 - 60)

counter = trtl.Turtle()
counter.hideturtle()
counter.penup()
counter.goto(0, wn.window_height() // 2 - 150)  # Higher to avoid overlap

leaderboard_turtle = trtl.Turtle()
leaderboard_turtle.hideturtle()
leaderboard_turtle.penup()
leaderboard_turtle.goto(0, 0)

LEADERBOARD_FILE = "leaderboard.txt"

def update_score():
    score_turtle.clear()
    score_turtle.write(f"Score: {score}", align="center", font=("Arial", 24, "normal"))
    wn.update()

def move_turtle_random():
    width = wn.window_width() // 2 - 40
    height = wn.window_height() // 2 - 140
    x = random.randint(-width, width)
    y = random.randint(-height, height)
    player_turtle.goto(x, y)
    wn.update()

def game_over():
    global timer_running
    timer_running = False
    player_turtle.hideturtle()
    counter.clear()
    counter.goto(0, wn.window_height() // 2 - 150)  # Higher position
    counter.write("Time's Up! Game Over.", align="center", font=("Arial", 30, "bold"))
    wn.update()

    leader_names = get_names(LEADERBOARD_FILE)
    leader_scores = get_scores(LEADERBOARD_FILE)

    qualifies = False
    if len(leader_scores) < 5 or score >= min(leader_scores):
        qualifies = True

    if qualifies:
        leader_names, leader_scores = update_leaderboard(LEADERBOARD_FILE, leader_names, leader_scores, player_name, score)

    draw_leaderboard(qualifies, leader_names, leader_scores, leaderboard_turtle, player_name, score)
    wn.update()

def countdown():
    global timer, timer_up, timer_running
    if not timer_running:
        return
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
        player_turtle.hideturtle()
        score += 1
        update_score()
        timer = initial_timer
        counter.clear()
        counter.write(f"Timer: {timer:.1f} s", font=font_setup)
        wn.ontimer(respawn_turtle, 300)
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
