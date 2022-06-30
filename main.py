import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# Color constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pose(self):
        return self.row, self.col

    def is_closed(self):  # Close node
        return self.color == RED

    def is_open(self):   # Open node
        return self.color == GREEN

    def is_wall(self):  # Creating obstacles
        return self.color == BLACK

    def is_start(self):  # Start Point
        return self.color == ORANGE

    def is_end(self):    # Target Point
        return self.color == TURQUOISE

    def reset(self):     # Cell(Node) Color
        self.color = WHITE

    def make_close(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_wall(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_start(self):
        self.color = ORANGE

    def make_path(self):  # The shortest path thanks to A* Algorithm
        self.color = PURPLE

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x, self.y, self.width, self.width))

    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows -1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col< self.total_rows - 1 and not grid[self.row][self.col +1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col -1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def h(p1,p2):   # heuristic calculation manhattan distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(close_node, current_node, draw):  # draw the path at the end
    while current_node in close_node:
        current_node = close_node[current_node]
        current_node.make_path()
        draw()

def algorithm(draw, grid, start, end):  # A* algorithm, all g_score is infinitive
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    close_node = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pose(), end.get_pose())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = open_set.get()[2]
        open_set_hash.remove(current_node)

        if current_node == end:
            reconstruct_path(close_node, end, draw)
            end.make_end()
            return True

        for neighbor in current_node.neighbors:
            temp_g_score = g_score[current_node] + 1
            if temp_g_score < g_score[neighbor]:
                close_node[neighbor] = current_node
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pose(), end.get_pose())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current_node != start:
            current_node.make_close()
    return False

def make_grid(rows, width):  # Create grid
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap,rows)
            grid[i].append(node)

    return grid

def draw_grid(win, rows, width):   # Draw the grid
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap, 0), (j * gap, width))

def draw(win, grid, rows, width):  # Initiate all cells(nodes) to white color
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):   # geting position of clicked area
    gap = width // rows
    y,x = pos

    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, WIDTH)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]: #LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_wall()

            elif  pygame.mouse.get_pressed()[2]: #RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda : draw(win,grid,ROWS,width),grid,start,end)



    pygame.quit()

main(WIN, WIDTH)