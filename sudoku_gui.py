import tkinter as tk
from tkinter import messagebox

# ---------------- SOLVER LOGIC ---------------- #

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None


def is_valid(board, num, pos):
    row, col = pos

    for j in range(9):
        if board[row][j] == num:
            return False

    for i in range(9):
        if board[i][col] == num:
            return False

    box_x = col // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num:
                return False

    return True


def solve(board):
    find = find_empty(board)
    if not find:
        return True

    row, col = find

    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            update_gui(board, row, col)

            if solve(board):
                return True

            board[row][col] = 0
            update_gui(board, row, col)

    return False


# ---------------- GUI HELPERS ---------------- #

def update_gui(board, r, c):
    cells[r][c].delete(0, tk.END)
    if board[r][c] != 0:
        cells[r][c].insert(0, str(board[r][c]))
    root.update()
    root.after(40)   # animation speed


def get_board():
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            value = cells[i][j].get()
            if value == "":
                row.append(0)
            elif value.isdigit() and 1 <= int(value) <= 9:
                row.append(int(value))
            else:
                return None
        board.append(row)
    return board


def validate_board(board):
    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num != 0:
                board[i][j] = 0
                if not is_valid(board, num, (i, j)):
                    highlight_error(i, j)
                    board[i][j] = num
                    return False
                board[i][j] = num
    return True


def highlight_error(r, c):
    cells[r][c].config(bg="red")


def reset_colors():
    for row in cells:
        for cell in row:
            cell.config(bg="white")


# ---------------- BUTTON ACTIONS ---------------- #

def solve_sudoku():
    reset_colors()
    board = get_board()

    if board is None:
        messagebox.showerror("Invalid Input", "Only single digits (1–9) allowed.")
        return

    if not validate_board(board):
        messagebox.showerror("Invalid Sudoku", "Sudoku rules violated.")
        return

    if find_empty(board) is None:
        messagebox.showinfo("Sudoku Solver", "Sudoku is already solved!")
        return

    if not solve(board):
        messagebox.showerror("Sudoku Solver", "No solution exists.")
        return

    messagebox.showinfo("Sudoku Solver", "Sudoku solved successfully!")


def clear():
    for row in cells:
        for cell in row:
            cell.delete(0, tk.END)
            cell.config(bg="white")


# ---------------- INPUT RESTRICTION ---------------- #

def validate_entry(P):
    return P == "" or (P.isdigit() and len(P) == 1 and 1 <= int(P) <= 9)


# ---------------- GUI SETUP ---------------- #

root = tk.Tk()
root.title("Sudoku Solver (AI Backtracking)")
root.geometry("460x560")

vcmd = root.register(validate_entry)
cells = []

for i in range(9):
    row = []
    for j in range(9):
        e = tk.Entry(
            root,
            width=2,
            font=("Arial", 18),
            justify="center",
            validate="key",
            validatecommand=(vcmd, "%P"),
            borderwidth=2
        )
        e.grid(row=i, column=j, padx=5, pady=5)
        row.append(e)
    cells.append(row)

tk.Button(root, text="Solve", font=("Arial", 14), command=solve_sudoku)\
    .grid(row=9, column=0, columnspan=4, pady=20)

tk.Button(root, text="Clear", font=("Arial", 14), command=clear)\
    .grid(row=9, column=5, columnspan=4, pady=20)

root.mainloop()
