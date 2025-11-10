import turtle
import random

class MazeGenerator:
    def __init__(self, rows=10, cols=10, cell_size=40, wall_color="black", path_color="white", delay=0,
                 start_color="green", end_color="red", debug_path_color="yellow",
                 extra_branches=20):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.wall_color = wall_color
        self.path_color = path_color
        self.delay = delay
        self.start_color = start_color
        self.end_color = end_color
        self.debug_path_color = debug_path_color
        self.extra_branches = extra_branches  # Number of extra random branches to add
        
        self.screen = turtle.Screen()
        self.screen.title("Maze Generator with Extra Paths")
        self.screen.setup(width=cols*cell_size + 50, height=rows*cell_size + 50)
        self.screen.bgcolor(path_color)
        
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.hideturtle()
        self.t.penup()
        
        self.maze = [[{'N': True, 'S': True, 'E': True, 'W': True, 'visited': False} for _ in range(cols)] for _ in range(rows)]
        
    def draw_cell_walls(self, row, col):
        x = col * self.cell_size - (self.cols * self.cell_size) / 2
        y = (self.rows * self.cell_size) / 2 - row * self.cell_size
        
        self.t.penup()
        self.t.goto(x, y)
        self.t.pendown()
        
        cell = self.maze[row][col]
        
        if cell['N']:
            self.t.goto(x + self.cell_size, y)
        else:
            self.t.penup()
            self.t.goto(x + self.cell_size, y)
            self.t.pendown()
        
        if cell['E']:
            self.t.goto(x + self.cell_size, y - self.cell_size)
        else:
            self.t.penup()
            self.t.goto(x + self.cell_size, y - self.cell_size)
            self.t.pendown()
        
        if cell['S']:
            self.t.goto(x, y - self.cell_size)
        else:
            self.t.penup()
            self.t.goto(x, y - self.cell_size)
            self.t.pendown()
        
        if cell['W']:
            self.t.goto(x, y)
        else:
            self.t.penup()
            self.t.goto(x, y)
            self.t.pendown()
    
    def draw_start_end(self):
        start_x = 0 * self.cell_size - (self.cols * self.cell_size) / 2
        start_y = (self.rows * self.cell_size) / 2 - 0 * self.cell_size
        self.t.penup()
        self.t.goto(start_x + self.cell_size/2, start_y - self.cell_size/2)
        self.t.dot(self.cell_size * 0.6, self.start_color)
        
        end_x = (self.cols-1) * self.cell_size - (self.cols * self.cell_size) / 2
        end_y = (self.rows * self.cell_size) / 2 - (self.rows-1) * self.cell_size
        self.t.penup()
        self.t.goto(end_x + self.cell_size/2, end_y - self.cell_size/2)
        self.t.dot(self.cell_size * 0.6, self.end_color)
        
    def draw_maze(self):
        self.t.color(self.wall_color)
        self.t.pensize(3)
        for row in range(self.rows):
            for col in range(self.cols):
                self.draw_cell_walls(row, col)
        self.draw_start_end()
        self.screen.update()
        
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
                opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
                self.maze[new_row][new_col][opposite[direction]] = False
                
                if self.delay > 0:
                    self.draw_maze()
                    turtle.delay(self.delay)
                
                self.carve_passages_from(new_row, new_col)

    def add_extra_branches(self):
        # Try to add extra random paths from already visited cells by knocking down walls
        added = 0
        attempts = 0
        max_attempts = self.rows * self.cols * 10  # Prevent infinite loops
        
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
                    # Only knock down wall if neighbor is visited but there's a wall between
                    if neighbor['visited'] and cell[direction] and neighbor[self.opposite(direction)]:
                        cell[direction] = False
                        neighbor[self.opposite(direction)] = False
                        added += 1
                        break

    def opposite(self, direction):
        return {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}[direction]
        
    def find_path(self):
        stack = [(0, 0, [])]
        visited = set()
        
        while stack:
            row, col, path = stack.pop()
            if (row, col) in visited:
                continue
            visited.add((row, col))
            path = path + [(row, col)]
            if row == self.rows - 1 and col == self.cols - 1:
                return path
            
            cell = self.maze[row][col]
            if not cell['N'] and (row - 1, col) not in visited:
                stack.append((row - 1, col, path))
            if not cell['S'] and (row + 1, col) not in visited:
                stack.append((row + 1, col, path))
            if not cell['E'] and (row, col + 1) not in visited:
                stack.append((row, col + 1, path))
            if not cell['W'] and (row, col - 1) not in visited:
                stack.append((row, col - 1, path))
        return []
    
    def draw_debug_path(self, path):
        if not path:
            return
        self.t.color(self.debug_path_color)
        self.t.pensize(self.cell_size // 5)
        self.t.penup()
        
        for i, (row, col) in enumerate(path):
            x = col * self.cell_size - (self.cols * self.cell_size) / 2 + self.cell_size / 2
            y = (self.rows * self.cell_size) / 2 - row * self.cell_size - self.cell_size / 2
            if i == 0:
                self.t.goto(x, y)
                self.t.pendown()
            else:
                self.t.goto(x, y)
        self.t.penup()
        
    def generate(self):
        self.screen.tracer(0)
        self.carve_passages_from(0, 0)
        self.add_extra_branches()
        self.draw_maze()
        path = self.find_path()
        self.draw_debug_path(path)
        self.screen.tracer(1)
        self.screen.mainloop()

maze = MazeGenerator(rows=20, cols=20, cell_size=25, wall_color="blue", path_color="black", delay=0,
                     extra_branches=40)
maze.generate()
