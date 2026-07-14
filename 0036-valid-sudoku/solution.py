def valid_sudoku(board):
    for i in board:
        hash_set = set()
        for j in i:
            if j == ".":
                continue
            if j in hash_set:
                return False
            else:
                hash_set.add(j)

    for cols in range(0, 9):
        hash_set = set()
        for array in board:
            if array[cols] == ".":
                continue
            if array[cols] in hash_set:
                return False
            else:
                hash_set.add(array[cols])

    for i in range(0, 9):
        row = (i // 3) * 3
        column = (i % 3) * 3
        hash_set = set()
        for j in range(row, row + 3):
            for k in range(column, column + 3):
                if board[j][k] == ".":
                    continue
                if board[j][k] in hash_set:
                    return False
                else:
                    hash_set.add(board[j][k])

    return True


def valid_sudoku_onepass(board):
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    for i in range(len(board)):
        rows = set()
        for j in range(len(board[i])):
            box = ((i // 3) * 3) + (j // 3)
            value = board[i][j]
            if value == ".":
                continue
            if value in rows or value in cols[j] or value in boxes[box]:
                return False
            rows.add(value)
            cols[j].add(value)
            boxes[box].add(value)

    return True


board = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]

print(valid_sudoku(board))
