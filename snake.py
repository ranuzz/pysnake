"""
class SnakeGame:

    def __init__(self, width: int, height: int, food: List[List[int]]):
        self.food = food
        self.cf = 0
        self.w = width
        self.h = height
        self.snake = [(0,0)]

    def move(self, direction: str) -> int:
        d = direction
        head = [self.snake[-1][0], self.snake[-1][1]]
        if d == 'U':
            head[0] -= 1
        elif d == 'L':
            head[1] -= 1
        elif d == 'R':
            head[1] += 1
        elif d == 'D':
            head[0] += 1
            
        #print(head)
        if head[0] < 0 or head[0] >= self.h or head[1] < 0 or head[1] >= self.w:
            return -1
        
        new_head = (head[0], head[1])
        
        if self.cf < len(self.food):
            f = self.food[self.cf]
            
            if head[0] == f[0] and head[1] == f[1]:
                self.cf += 1
            else:
                self.snake.pop(0)
        else:
            self.snake.pop(0)
            
        if new_head in self.snake:
            return -1
        self.snake.append(new_head)
        return len(self.snake)-1
"""

import curses
from curses import wrapper
import random
from curses.textpad import Textbox, rectangle

def get_screen():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.curs_set(0)
    return stdscr


def exit_screen(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def setup_game(stdscr):
    stdscr.clear()
    stdscr.addstr(1, 2, "py-curses-snake-ranuzz", curses.A_REVERSE)

    center_y = curses.LINES // 2
    center_x = curses.COLS // 2

    ul_x = center_x - (curses.COLS//4)
    ul_y = center_y - (curses.LINES//4)

    lr_x = center_x + (curses.COLS//4)
    lr_y = center_y + (curses.LINES//4)

    rectangle(stdscr, ul_y, ul_x, lr_y, lr_x) # # win, uly, ulx, lry, lrx

    """
    for c in range(ul_x, lr_x+1):
        stdscr.addch(ul_y, c, "#")
        stdscr.addch(lr_y, c, "#")
    
    for r in range(ul_y+1, lr_y):
        stdscr.addch(r, ul_x, "|")
        stdscr.addch(r, lr_x, "|")
    """

    rows = lr_y - ul_y - 1
    cols = lr_x - ul_x - 1

    arena = []
    for i in range(rows):
        arena.append(cols*[0])

    stdscr.refresh()
    return arena, ul_x, ul_y, lr_x, lr_y

def get_food(rows, cols, snake):

    row = random.randint(0, rows-1)
    col = random.randint(0, cols-1)

    while (row, col) in snake:
        row = random.randint(0, rows-1)
        col = random.randint(0, cols-1)

    return (row, col)

def game_over(stdscr, arena, ul_x, ul_y, lr_x, lr_y, score):

    c_row = (ul_y + lr_y) // 2
    c_col = (ul_x + lr_x) // 2

    message = "GAME OVER : {}".format(score-1)

    c_col -= len(message) // 2

    stdscr.addstr(c_row, c_col, message, curses.A_REVERSE)

    stdscr.refresh()
    key = stdscr.getch()
    while key != ord('q'):
        if key == ord('r'):
            start_game(stdscr, arena, ul_x, ul_y, lr_x, lr_y)
        key = stdscr.getch()

def start_game(stdscr, arena, ul_x, ul_y, lr_x, lr_y):
    rows = len(arena)
    cols = len(arena[0])

    snake = [(0,0)]
    food = get_food(rows, cols, snake)

    key = ''
    while key != ord('q'):
        head = [snake[-1][0], snake[-1][1]]    
        if key == curses.KEY_UP:
            head[0] -= 1
        elif key == curses.KEY_DOWN:
            head[0] += 1
        elif key == curses.KEY_LEFT:
            head[1] -= 1
        elif key == curses.KEY_RIGHT:
            head[1] += 1
    
        if head[0] < 0 or head[0] >= rows or head[1] < 0 or head[1] >= cols:
            break

        nhead = (head[0], head[1])
        snake.append(nhead)

        for i in range(rows):
            for j in range(cols):
                stdscr.addch(ul_y+i, ul_x+j, " ")

        if nhead[0] == food[0] and nhead[1] == food[1]:
            food = get_food(rows, cols, snake)
        else:
            snake.pop(0)

        stdscr.addch(ul_y+food[0], ul_x+food[1], "X")

        for s in snake:
            stdscr.addch(ul_y+s[0], ul_x+s[1], "S")      
        
        if nhead in snake[:-1]:
            break
                    
        stdscr.refresh()
        key = stdscr.getch()  

    game_over(stdscr, arena, ul_x, ul_y, lr_x, lr_y, len(snake))

def init_game():
    stdscr = get_screen()

    stdscr.clear()
    arena, ul_x, ul_y, lr_x, lr_y = setup_game(stdscr)
    start_game(stdscr, arena, ul_x+1, ul_y+1, lr_x-1, lr_y-1)
    exit_screen(stdscr)
init_game()