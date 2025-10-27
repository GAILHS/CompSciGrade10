import turtle
import time
import math
import random

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("1.1.9")

# Set fullscreen window so it fills whole screen
screen.setup(width=1.0, height=1.0)
screen.cv._rootwindow.attributes('-fullscreen', True)

# Get the actual size of the fullscreen window
screen_width = screen.window_width()
screen_height = screen.window_height()

# Calculate how wide vs tall the screen is
aspect_ratio = screen_width / screen_height

# Margin around the drawing so it doesn't touch edges
margin = 100

# Set up coordinate system to keep shapes proportional
if aspect_ratio > 1:
    # Screen is wider than tall
    world_width = screen_width + 2 * margin
    world_height = world_width / aspect_ratio
else:
    # Screen is taller than wide
    world_height = screen_height + 2 * margin
    world_width = world_height * aspect_ratio

# Calculate edges of the coordinate system
left = -world_width / 2
right = world_width / 2
bottom = -world_height / 2
top = world_height / 2

# Apply the coordinate system to the screen
screen.setworldcoordinates(left, bottom, right, top)

screen.tracer(0)  # Turn off automatic drawing


artist = turtle.Turtle()
artist.speed(0)  # Fastest drawing
artist.width(2)  # Line thickness
artist.hideturtle()  # Hide the turtle icon

sparkle = turtle.Turtle()
sparkle.speed(0)
sparkle.hideturtle()
sparkle.penup()  # Sparkle turtle doesn't draw lines


# Colors of the rainbow
rainbow_colors = [
    (255, 0, 0),       # Red
    (255, 127, 0),     # Orange
    (255, 255, 0),     # Yellow
    (0, 255, 0),       # Green
    (0, 0, 255),       # Blue
    (75, 0, 130),      # Indigo
    (139, 0, 255),     # Violet
]

# Convert RGB triple to hex color string
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

# Blend two colors together
def interpolate_color(c1, c2, t):
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t)
    )

# Get a smooth rainbow color based on angle
def get_smooth_gradient_color(angle_deg):
    angle = angle_deg % 360
    t = (angle / 360) * len(rainbow_colors)
    index = int(t) % len(rainbow_colors)
    next_index = (index + 1) % len(rainbow_colors)
    fraction = t - int(t)
    c1 = rainbow_colors[index]
    c2 = rainbow_colors[next_index]
    return interpolate_color(c1, c2, fraction)

# Draw basic shapes

def draw_square(t, size):
    for _ in range(4):
        t.forward(size)
        t.right(90)

def draw_triangle(t, size):
    for _ in range(3):
        t.forward(size)
        t.left(120)

def draw_circle(t, size):
    t.circle(size)

def draw_star(t, size):
    for _ in range(5):
        t.forward(size)
        t.right(144)

def draw_pentagon(t, size):
    for _ in range(5):
        t.forward(size)
        t.right(72)

def draw_hexagon(t, size):
    for _ in range(6):
        t.forward(size)
        t.right(60)

def draw_octagon(t, size):
    for _ in range(8):
        t.forward(size)
        t.right(45)

# List of shapes
shape_functions = [
    draw_square,
    draw_triangle,
    draw_circle,
    draw_star,
    draw_pentagon,
    draw_hexagon,
    draw_octagon,
]

# Basic settings
base_size = 18             # Starting size for shapes
max_radius = 280           # Max distance shapes can be from center
min_pulse_factor = 0.4     # Smallest pulse size factor
max_pulse_factor = 1.6     # Biggest pulse size factor
pulse_amplitude = max_pulse_factor - min_pulse_factor
num_shapes = 24            # Number of shapes per spiral
angle_step = 360 / num_shapes  # How far apart shapes are in degrees

# Different spirals with speed, direction, size, and position offsets
spirals = [
    {"id": 0, "speed": 0.08, "direction": 1, "size_offset": 0,   "pos_offset": (0, 0)},
    {"id": 1, "speed": 0.08, "direction": 1, "size_offset": 2,   "pos_offset": (90, 30)},
    {"id": 2, "speed": 0.08, "direction": 1, "size_offset": 4,   "pos_offset": (-90, -30)},
    {"id": 3, "speed": 0.08, "direction": 1, "size_offset": 6,   "pos_offset": (60, -70)},
    {"id": 4, "speed": 0.08, "direction": 1, "size_offset": 8,   "pos_offset": (-60, 70)},
]

# More spirals that orbit with different speeds and directions
orbiting_spirals = [
    {"id": 5, "speed": 0.15, "direction": -1, "size_offset": 1, "pos_offset": (0, 0)},
    {"id": 6, "speed": 0.12, "direction": 1,  "size_offset": 3, "pos_offset": (0, 0)},
    {"id": 7, "speed": 0.1,  "direction": -1, "size_offset": 5, "pos_offset": (0, 0)},
]

rotation = 0.0             # Current rotation angle
rotation_increment = 3.0   # How much rotation changes each frame

mode = "fade"              # Background color mode (fade or flash)
flash_frame = 0
flash_max_frames = 15

# Variables for burst effect when clicking
burst_active = False
burst_start_time = 0
burst_duration = 4  # How long burst explosion lasts in seconds
drift_duration = 4  # How long burst drifts back in seconds
easing_duration = 1 # Smooth easing time back to spiral
total_burst_time = burst_duration + drift_duration + easing_duration
click_x, click_y = 0, 0

explosion_data = []  # Stores info for burst explosion shapes

# Prepare explosion data for burst animation
def prepare_explosion():
    global explosion_data
    explosion_data = []
    all_spirals = spirals + orbiting_spirals
    for spiral in all_spirals:
        pos_x, pos_y = spiral["pos_offset"]
        spiral_id = spiral["id"]
        for i in range(num_shapes):
            angle = i * angle_step + rotation * 5
            pulse_factor = min_pulse_factor + (math.sin(rotation * spiral["speed"] * spiral["direction"] + i) + 1) / 2 * pulse_amplitude
            raw_distance = i * 6 + (rotation * 2)
            distance = min(raw_distance * pulse_factor, max_radius)
            x = pos_x + distance * math.cos(math.radians(angle))
            y = pos_y + distance * math.sin(math.radians(angle))

            # Calculate velocity for explosion pieces away from click point
            dx = x - click_x
            dy = y - click_y
            dist = math.hypot(dx, dy)
            if dist == 0:
                dist = 0.01  # Avoid division by zero
            base_angle = math.atan2(dy, dx)
            rand_angle = base_angle + random.uniform(-math.pi/4, math.pi/4)  # Add randomness to direction
            speed = random.uniform(150, 300)  # Random speed of explosion pieces

            vx = math.cos(rand_angle) * speed
            vy = math.sin(rand_angle) * speed

            explosion_data.append({
                "original_x": x,
                "original_y": y,
                "vx": vx,
                "vy": vy,
                "spiral_id": spiral_id,
                "shape_index": i,
                "pos_x": x,
                "pos_y": y,
            })

# Linear interpolation helper function
def lerp(a, b, t):
    return a + (b - a) * t

# Draw a spiral of shapes with animation
def draw_spiral(rotation_offset, time_step, rocking_angle, config, burst=False):
    speed = config["speed"]
    direction = config["direction"]
    size_offset = config["size_offset"]
    pos_x, pos_y = config["pos_offset"]
    spiral_id = config["id"]

    shape_centers = []

    for i in range(num_shapes):
        shape_index = i % len(shape_functions)

        angle = i * angle_step + rotation_offset * 5

        grad_color = get_smooth_gradient_color(angle)
        pen_col = rgb_to_hex(grad_color)

        # Lighter fill color for the shape
        fill_rgb = (
            min(255, int(grad_color[0] + (255 - grad_color[0]) * 0.5)),
            min(255, int(grad_color[1] + (255 - grad_color[1]) * 0.5)),
            min(255, int(grad_color[2] + (255 - grad_color[2]) * 0.5)),
        )
        fill_col = rgb_to_hex(fill_rgb)

        artist.pencolor(pen_col)
        artist.fillcolor(fill_col)

        # Pulse size changes
        pulse_factor = min_pulse_factor + (math.sin(time_step * speed * direction + i) + 1) / 2 * pulse_amplitude

        raw_distance = i * 6 + (rotation_offset * 2)
        distance = min(raw_distance * pulse_factor, max_radius)

        if burst:
            global_idx = spiral_id * num_shapes + i
            if global_idx < len(explosion_data):
                ex = explosion_data[global_idx]
                elapsed = time.time() - burst_start_time

                if elapsed <= burst_duration:
                    dt = elapsed
                    burst_x = ex["original_x"] + ex["vx"] * dt
                    burst_y = ex["original_y"] + ex["vy"] * dt
                    x, y = burst_x, burst_y
                elif elapsed <= burst_duration + drift_duration:
                    dt = elapsed - burst_duration
                    t = dt / drift_duration
                    burst_x = ex["original_x"] + ex["vx"] * burst_duration
                    burst_y = ex["original_y"] + ex["vy"] * burst_duration
                    x = lerp(burst_x, ex["original_x"], t)
                    y = lerp(burst_y, ex["original_y"], t)
                elif elapsed <= total_burst_time:
                    dt = elapsed - burst_duration - drift_duration
                    t = dt / easing_duration
                    burst_end_x = ex["original_x"]
                    burst_end_y = ex["original_y"]
                    spiral_x = pos_x + distance * math.cos(math.radians(angle))
                    spiral_y = pos_y + distance * math.sin(math.radians(angle))
                    x = lerp(burst_end_x, spiral_x, t)
                    y = lerp(burst_end_y, spiral_y, t)
                else:
                    x = pos_x + distance * math.cos(math.radians(angle))
                    y = pos_y + distance * math.sin(math.radians(angle))
            else:
                x = pos_x + distance * math.cos(math.radians(angle))
                y = pos_y + distance * math.sin(math.radians(angle))
        else:
            x = pos_x + distance * math.cos(math.radians(angle))
            y = pos_y + distance * math.sin(math.radians(angle))

        shape_centers.append((x, y))

        artist.penup()
        artist.goto(x, y)
        artist.setheading(angle)
        artist.pendown()

        artist.begin_fill()
        shape_functions[shape_index](artist, base_size + ((i + size_offset) % 6) * 2)
        artist.end_fill()

    return shape_centers

# Wrapper for orbiting spirals
def draw_orbiting_spiral(rotation_offset, time_step, rocking_angle, config, burst=False):
    pos_x, pos_y = config["pos_offset"]
    config["pos_offset"] = (pos_x, pos_y)
    return draw_spiral(rotation_offset, time_step, rocking_angle, config, burst)

# When screen is clicked, start burst animation at click location
def on_click(x, y):
    global burst_active, burst_start_time, click_x, click_y
    burst_active = True
    burst_start_time = time.time()
    click_x, click_y = x, y
    prepare_explosion()

screen.onclick(on_click)  # Link mouse click to on_click function

try:
    while True:
        current_time = time.time()
        if burst_active:
            elapsed = current_time - burst_start_time
            if elapsed > total_burst_time:
                burst_active = False  # Stop burst after total time

        # Change background color smoothly or flash randomly
        if mode == "fade":
            color_index = int(rotation / 60) % len(rainbow_colors)
            next_color_index = (color_index + 1) % len(rainbow_colors)
            fade_progress = (rotation % 60) / 60
            c1 = rainbow_colors[color_index]
            c2 = rainbow_colors[next_color_index]
            interp_color = interpolate_color(c1, c2, fade_progress)
            screen.bgcolor(rgb_to_hex(interp_color))

        elif mode == "flash":
            screen.bgcolor(rgb_to_hex(random.choice(rainbow_colors)))
            flash_frame += 1
            if flash_frame > flash_max_frames:
                mode = "fade"

        artist.clear()   # Clear previous frame drawings
        sparkle.clear()  # Clear sparkles
        all_centers = []

        rocking_angle = 0  # Placeholder for possible rocking effect, WIP

        # Draw all spirals
        for spiral in spirals:
            centers = draw_spiral(rotation, rotation, rocking_angle, spiral, burst_active)
            all_centers.extend(centers)

        # Draw orbiting spirals
        for orbit_spiral in orbiting_spirals:
            centers = draw_orbiting_spiral(rotation, rotation, rocking_angle, orbit_spiral, burst_active)
            all_centers.extend(centers)

        # Draw sparkles randomly on some shapes
        for (x, y) in all_centers:
            if random.random() < 0.4:
                sparkle.goto(x, y)
                sparkle.dot(3, rgb_to_hex(rainbow_colors[int(rotation/5) % len(rainbow_colors)]))
            if random.random() < 0.05:
                sparkle.goto(x, y)
                sparkle.dot(7, rgb_to_hex(rainbow_colors[int(rotation/3) % len(rainbow_colors)]))

        screen.update()
        rotation += rotation_increment  # Increase rotation for next frame
        time.sleep(0.02)  # Pause a bit to control frame rate
except turtle.Terminator:
    pass
