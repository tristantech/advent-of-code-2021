import re

FILE = "days/04/input.txt"

def calculate_board_score(b):
    score = 0
    for row in b:
        for cell in row:
            if cell >= 0:
                # Not called
                score += cell
    return score

def check_if_winner(b):
    # Horizontal win
    for row in b:
        if all([cell == -1 for cell in row]):
            return True
    
    # Vertical win
    for col in range(5):
        if all([row[col] == -1 for row in b]):
            return True
    
    return False

def strike_number(b, num):
    for i in range(5):
        for j in range(5):
            if b[i][j] == num:
                b[i][j] = -1

with open(FILE) as f:
    lines = f.readlines()

    called_nums = list(map(int, lines[0].strip().split(",")))

    # Build boards
    boards = list()
    current_board = list()
    r = re.compile("([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)")
    for l in lines[2:]:
        if len(l) < 3:
            # Board done
            boards.append(current_board)
            current_board = list()
            continue
        current_board.append(
            [int(x) for x in r.findall(l)[0]]
        )
    boards.append(current_board)

    # Part I
    done = False
    for num in called_nums:
        for b in boards:
            strike_number(b, num)
            if check_if_winner(b):
                print("This board won. Num =", num)
                for row in b:
                    print(row)
                print()
                print("Part I answer: ", calculate_board_score(b) * num)
                done = True
        if done:
            break

    # Part II
    finish_order = []
    for num in called_nums:
        for i, b in enumerate(boards):
            strike_number(b, num)
            if check_if_winner(b) and (i not in finish_order):
                finish_order.append(i)
                if len(finish_order) == len(boards):
                    # Got the last one
                    print("Part II answer: ", calculate_board_score(b) * num)
    
