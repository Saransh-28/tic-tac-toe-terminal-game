from curses import wrapper

player = 'o'
bot = 'x'

grid = {1: " ", 2: " ", 3: " ",
        4: " ", 5: " ", 6: " ",
        7: " ", 8: " ", 9: " "}


def print_end_grid(grid):
    print(f" {grid[1]} | {grid[2]} | {grid[3]} ")
    print(" - + - + - ")
    print(f" {grid[4]} | {grid[5]} | {grid[6]} ")
    print(" - + - + - ")
    print(f" {grid[7]} | {grid[8]} | {grid[9]} \n")


def print_grid(stdscr, grid):
    stdscr.addstr(6, 10, f" {grid[1]} | {grid[2]} | {grid[3]} ")
    stdscr.addstr(7, 10, " - + - + - ")
    stdscr.addstr(8, 10, f" {grid[4]} | {grid[5]} | {grid[6]} ")
    stdscr.addstr(9, 10, " - + - + - ")
    stdscr.addstr(10, 10, f" {grid[7]} | {grid[8]} | {grid[9]} \n")


def check_space(position):
    if grid[position] == ' ':
        return True
    else:
        return False


def draw():
    for key in grid.keys():
        if (grid[key] == ' '):
            return False
    return True


def win():
    if (grid[1] == grid[2] and grid[1] == grid[3] and grid[1] != ' '):
        return True
    elif (grid[4] == grid[5] and grid[4] == grid[6] and grid[4] != ' '):
        return True
    elif (grid[7] == grid[8] and grid[7] == grid[9] and grid[7] != ' '):
        return True
    elif (grid[1] == grid[4] and grid[1] == grid[7] and grid[1] != ' '):
        return True
    elif (grid[2] == grid[5] and grid[2] == grid[8] and grid[2] != ' '):
        return True
    elif (grid[3] == grid[6] and grid[3] == grid[9] and grid[3] != ' '):
        return True
    elif (grid[1] == grid[5] and grid[1] == grid[9] and grid[1] != ' '):
        return True
    elif (grid[7] == grid[5] and grid[7] == grid[3] and grid[7] != ' '):
        return True
    else:
        return False


def who_win(winner):
    if (grid[1] == grid[2] and grid[1] == grid[3] and grid[1] == winner):
        return True
    elif (grid[4] == grid[5] and grid[4] == grid[6] and grid[4] == winner):
        return True
    elif (grid[7] == grid[8] and grid[7] == grid[9] and grid[7] == winner):
        return True
    elif (grid[1] == grid[4] and grid[1] == grid[7] and grid[1] == winner):
        return True
    elif (grid[2] == grid[5] and grid[2] == grid[8] and grid[2] == winner):
        return True
    elif (grid[3] == grid[6] and grid[3] == grid[9] and grid[3] == winner):
        return True
    elif (grid[1] == grid[5] and grid[1] == grid[9] and grid[1] == winner):
        return True
    elif (grid[7] == grid[5] and grid[7] == grid[3] and grid[7] == winner):
        return True
    else:
        return False


def insert_value(stdscr, value, position):
    if check_space(position):
        grid[position] = value
        print_grid(stdscr, grid)
        if draw():
            print_end_grid(grid)
            print("The match is draw")
            exit()
        if win():
            if value == 'x':
                print_end_grid(grid)
                print("bot wins!")
                exit()
            else:
                print_end_grid(grid)
                print("you wins!")
                exit()
        return
    else:
        stdscr.addstr(14, 0, "invalid position")
        stdscr.addstr(13, 0, "Enter the new position - ")
        insert_value(stdscr, value, position)
        return


def player_move(stdscr):
    stdscr.addstr(13, 0, "Enter the position('o')- ")
    position = stdscr.getch()
    insert_value(stdscr, player, position-48)
    return


def bot_move(stdscr):
    bestscore = -100
    bestmove = 0
    for key in grid.keys():
        if (grid[key] == ' '):
            grid[key] = bot
            score = minmax(grid, 0, False)
            grid[key] = ' '
            if (score > bestscore):
                bestscore = score
                bestmove = key
    insert_value(stdscr, bot, bestmove)
    return


def minmax(grid, depth, isMax):
    if who_win(bot):
        return (5)
    elif who_win(player):
        return (-5)
    elif draw():
        return 0

    if isMax:
        bestscore = -100
        for key in grid.keys():
            if (grid[key] == ' '):
                grid[key] = bot
                score = (minmax(grid, depth+1, False))
                grid[key] = ' '
                if (score > bestscore):
                    bestscore = score
        return bestscore
    else:
        bestscore = 100
        for key in grid.keys():
            if (grid[key] == ' '):
                grid[key] = bot
                score = minmax(grid, depth+1, True)
                grid[key] = ' '
                if (score < bestscore):
                    bestscore = score
        return bestscore


def instruction(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "player char = o\nbot char = x")
    stdscr.addstr(1, 0, "layout -")
    stdscr.addstr(2, 0, "1|2|3\n4|5|6\n7|8|9")
    print_grid(stdscr, grid)
    bot_move(stdscr)
    player_move(stdscr)
    stdscr.refresh()


while not win():

    wrapper(instruction)
