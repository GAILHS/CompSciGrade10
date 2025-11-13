import turtle
import random
import time

class MazeGenerator:
    def __init__(self, rows=10, cols=10, cell_size=40, wall_color="black", path_color="white", delay=0,
                 start_color="green", end_color="red", debug_path_color="yellow", extra_branches=20):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.wall_color = wall_color
        self.path_color = path_color
        self.delay = delay
        self.start_color = start_color
        self.end_color = end_color
        self.debug_path_color = debug_path_color
        self.extra_branches = extra_branches
        self.victory = False
        self.start_time = None

        self.screen = turtle.Screen()
        self.screen.title("Maze Generator with Runner")
        self.screen.setup(width=cols*cell_size + 50, height=rows*cell_size + 50)
        self.screen.bgcolor(path_color)

        self.drawer = turtle.Turtle()
        self.drawer.speed(0)
        self.drawer.hideturtle()
        self.drawer.penup()

        self.writer = turtle.Turtle()
        self.writer.hideturtle()
        self.writer.penup()

        # Maze grid: walls and visited flags
        self.maze = [[{'N': True, 'S': True, 'E': True, 'W': True, 'visited': False}
                      for _ in range(cols)] for _ in range(rows)]

        # Maze runner (player)
        self.runner = turtle.Turtle()
        self.runner.shape("circle")
        self.runner.color("orange")
        self.runner.penup()
        self.runner.speed(0)

    def opposite(self, direction):
        return {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}[direction]

    def carve_passages_from(self, row, col):
        self.maze[row][col]['visited'] = True
        directions = ['N', 'S', 'E', 'W']
        random.shuffle(directions)
        for direction in directions:
            new_row, new_col = row, col
            if direction == 'N':
                new_row -= 1
            elif direction == 'S':
                new_row += 1
            elif direction == 'E':
                new_col += 1
            elif direction == 'W':
                new_col -= 1
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols and not self.maze[new_row][new_col]['visited']:
                self.maze[row][col][direction] = False
                self.maze[new_row][new_col][self.opposite(direction)] = False
                if self.delay > 0:
                    self.draw_maze()
                    turtle.delay(self.delay)
                self.carve_passages_from(new_row, new_col)

    def add_extra_branches(self):
        added = 0
        attempts = 0
        max_attempts = self.rows * self.cols * 10
        while added < self.extra_branches and attempts < max_attempts:
            attempts += 1
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            cell = self.maze[row][col]
            if not cell['visited']:
                continue
            directions = ['N', 'S', 'E', 'W']
            random.shuffle(directions)
            for direction in directions:
                new_row, new_col = row, col
                if direction == 'N':
                    new_row -= 1
                elif direction == 'S':
                    new_row += 1
                elif direction == 'E':
                    new_col += 1
                elif direction == 'W':
                    new_col -= 1
                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    neighbor = self.maze[new_row][new_col]
                    if neighbor['visited'] and cell[direction] and neighbor[self.opposite(direction)]:
                        cell[direction] = False
                        neighbor[self.opposite(direction)] = False
                        added += 1
                        break

    def draw_cell_walls(self, row, col):
        x = col * self.cell_size - (self.cols * self.cell_size) / 2
        y = (self.rows * self.cell_size) / 2 - row * self.cell_size
        self.drawer.penup()
        self.drawer.goto(x, y)
        self.drawer.pendown()
        cell = self.maze[row][col]
        if cell['N']:
            self.drawer.goto(x + self.cell_size, y)
        else:
            self.drawer.penup(); self.drawer.goto(x + self.cell_size, y); self.drawer.pendown()
        if cell['E']:
            self.drawer.goto(x + self.cell_size, y - self.cell_size)
        else:
            self.drawer.penup(); self.drawer.goto(x + self.cell_size, y - self.cell_size); self.drawer.pendown()
        if cell['S']:
            self.drawer.goto(x, y - self.cell_size)
        else:
            self.drawer.penup(); self.drawer.goto(x, y - self.cell_size); self.drawer.pendown()
        if cell['W']:
            self.drawer.goto(x, y)
        else:
            self.drawer.penup(); self.drawer.goto(x, y); self.drawer.pendown()

    def draw_start_end(self):
        sx = 0 * self.cell_size - (self.cols * self.cell_size) / 2 + self.cell_size/2
        sy = (self.rows * self.cell_size) / 2 - 0 * self.cell_size - self.cell_size/2
        self.drawer.penup(); self.drawer.goto(sx, sy); self.drawer.dot(self.cell_size * 0.6, self.start_color)
        ex = (self.cols-1) * self.cell_size - (self.cols * self.cell_size) / 2 + self.cell_size/2
        ey = (self.rows * self.cell_size) / 2 - (self.rows-1) * self.cell_size - self.cell_size/2
        self.drawer.penup(); self.drawer.goto(ex, ey); self.drawer.dot(self.cell_size * 0.6, self.end_color)

    def draw_maze(self):
        self.drawer.clear()
        self.drawer.color(self.wall_color)
        self.drawer.pensize(3)
        for r in range(self.rows):
            for c in range(self.cols):
                self.draw_cell_walls(r, c)
        self.draw_start_end()
        self.screen.update()

    def cell_center(self, row, col):
        x = col * self.cell_size - (self.cols * self.cell_size) / 2 + self.cell_size / 2
        y = (self.rows * self.cell_size) / 2 - row * self.cell_size - self.cell_size / 2
        return x, y

    def place_runner_at_start(self):
        x, y = self.cell_center(0, 0)
        self.runner.goto(x, y)
        self.runner.setheading(90)

    def current_cell(self):
        x, y = self.runner.position()
        col = int((x + (self.cols * self.cell_size) / 2) // self.cell_size)
        row = int(((self.rows * self.cell_size) / 2 - y) // self.cell_size)
        return row, col

    def try_move(self, direction_name, heading_angle):
        if self.victory:
            return
        self.runner.setheading(heading_angle)
        row, col = self.current_cell()
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        cell = self.maze[row][col]
        if not cell[direction_name]:
            if direction_name == 'N':
                row -= 1
            elif direction_name == 'S':
                row += 1
            elif direction_name == 'E':
                col += 1
            elif direction_name == 'W':
                col -= 1
            new_x, new_y = self.cell_center(row, col)
            self.runner.goto(new_x, new_y)
            if row == self.rows - 1 and col == self.cols - 1:
                self.on_victory()

    def on_w(self):
        self.try_move('N', 90)

    def on_s(self):
        self.try_move('S', 270)

    def on_a(self):
        self.try_move('W', 180)

    def on_d(self):
        self.try_move('E', 0)

    def enable_controls(self):
        wn = self.screen
        wn.onkeypress(self.on_w, "w")
        wn.onkeypress(self.on_s, "s")
        wn.onkeypress(self.on_a, "a")
        wn.onkeypress(self.on_d, "d")
        wn.listen()

    def on_victory(self):
        if self.victory:
            return
        self.victory = True
        # stop timer and compute elapsed
        elapsed = 0.0
        if self.start_time is not None:
            elapsed = time.time() - self.start_time
        minutes = int(elapsed // 60)
        seconds = elapsed % 60
        # Clear maze and runner visuals
        self.drawer.clear()
        self.runner.hideturtle()
        # Draw victory screen
        self.screen.bgcolor("black")
        self.writer.clear()
        self.writer.color("gold")
        self.writer.goto(0, 40)
        self.writer.write("CONGRATULATIONS!", align="center", font=("Arial", 32, "bold"))
        self.writer.goto(0, 0)
        self.writer.write("You reached the end!", align="center", font=("Arial", 20, "normal"))
        self.writer.goto(0, -30)
        self.writer.write(f"Time: {minutes:d}:{seconds:04.1f}", align="center", font=("Arial", 18, "normal"))
        self.writer.goto(0, -70)
        self.writer.write("Press ESC to exit", align="center", font=("Arial", 12, "normal"))
        # Disable movement keys
        wn = self.screen
        wn.onkeypress(lambda: None, "w")
        wn.onkeypress(lambda: None, "s")
        wn.onkeypress(lambda: None, "a")
        wn.onkeypress(lambda: None, "d")
        wn.onkeypress(self.screen.bye, "Escape")
        wn.listen()

    def generate(self):
        self.screen.tracer(0)
        self.carve_passages_from(0, 0)
        self.add_extra_branches()
        self.draw_maze()
        self.place_runner_at_start()
        self.enable_controls()
        # start timer when generation finished and player can move
        self.start_time = time.time()
        self.screen.tracer(1)
        self.screen.mainloop()

if __name__ == "__main__":
    maze = MazeGenerator(rows=15, cols=20, cell_size=25, wall_color="blue", path_color="white", delay=0,
                         start_color="green", end_color="red", debug_path_color="yellow", extra_branches=40)
    maze.generate()
