def print_board(board):
    """Pretty print the Sudoku board"""
    print("    1 2 3   4 5 6   7 8 9")
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("   " + "-" * 21)
        print(i+1, end="  ")  # Show row numbers starting from 1
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(board[i][j] if board[i][j] != "." else ".", end=" ")
        print()
    print()


def check_invalid_reason(board, row, col, num):
    """Return a string reason if the move is invalid, else return None."""
    # Check row
    for i in range(9):
        if board[row][i] == num:
            return f"Invalid because {num} is already in row {row+1}."

    # Check column
    for i in range(9):
        if board[i][col] == num:
            return f"Invalid because {num} is already in column {col+1}."

    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return f"Invalid because {num} is already in the 3x3 box."

    return None


def solve_sudoku(board):
    """Backtracking solver to complete the Sudoku"""
    for row in range(9):
        for col in range(9):
            if board[row][col] == ".":
                for num in map(str, range(1, 10)):
                    if check_invalid_reason(board, row, col, num) is None:
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = "."
                return False
    return True


def main():
    # Initial Sudoku board (empty cells as ".")
    board = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]

    # Pre-solve to get solution reference
    solved_board = [row[:] for row in board]
    solve_sudoku(solved_board)

    print("Welcome to Interactive Sudoku!")
    print("Initial Board:")
    print_board(board)

    while True:
        try:
            row_col_num = input("Enter row, column, and number (e.g., 3 5 9): ").split()
            if len(row_col_num) != 3:
                print("❌ Please enter row, column, and number separated by spaces.")
                continue

            row, col, num = int(row_col_num[0]) - 1, int(row_col_num[1]) - 1, row_col_num[2]

            if not (0 <= row < 9 and 0 <= col < 9):
                print("❌ Row and column must be between 1 and 9.")
                continue

            if num not in "123456789":
                print("❌ Number must be between 1 and 9.")
                continue

            if board[row][col] != ".":
                print("❌ This cell is already filled. Try another one.")
                continue

            # Local rule check
            reason = check_invalid_reason(board, row, col, num)
            if reason is not None:
                print(f"❌ {reason}")
                print_board(board)
                continue

            # Correctness check against solved board
            if solved_board[row][col] != num:
                print(f"❌ Incorrect solution. The correct number here is not {num}.")
                print_board(board)
                continue

            # If passed all checks
            board[row][col] = num
            print("✅ Move accepted!")
            print_board(board)

        except Exception:
            print("❌ Invalid input. Please try again.")

    print("\n✅ Final Solved Board:")
    print_board(solved_board)


if __name__ == "__main__":
    main()
