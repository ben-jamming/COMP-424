import numpy as np

def is_valid_move(board, row, col, num):
    """
    Check if placing the given number at the given position is valid.
    """
    # Check row
    if num in board[row]:
        return False
    
    # Check column
    if num in board[:, col]:
        return False
    
    # Check 2x2 box
    start_row, start_col = 2 * (row // 2), 2 * (col // 2)
    for i in range(2):
        for j in range(2):
            if board[start_row + i][start_col + j] == num:
                return False
                
    return True

def forward_checking(board, row, col):
    """
    Update the domains of unassigned variables based on the current state of the board.
    """
    # Domains for all cells (1-4 initially for all cells)
    domains = [[set(range(1, 5)) for _ in range(4)] for _ in range(4)]
    
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                domains[i][j] = set()
    
    # If a cell is unassigned, update its domain based on current board state
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                for num in range(1, 5):
                    if not is_valid_move(board, i, j, num):
                        domains[i][j].discard(num)
    
    return domains

def visualize_board(board, domains=[], print_domains=False):
    """
    Visualize the current state of the board and the domains for each slot.
    """
    cell_width = 6
    for i in range(4):
        # if i == 2:
        
        for j in range(4):
            # if j == 2:
            print("|", end="")
            if domains:
                content = str(domains[i][j])
            else:
                content = "Empty" if board[i][j] == 0 else str(board[i][j])
            print(content.ljust(cell_width), end="")

        print()
        print("-" * (cell_width * 4 + 3))


def backtrack(board, row, col, steps):
    """
    Perform backtracking with forward checking and visualize each step.
    """
    # If we've reached the end of the board, return True (solution found)
    if row == 4:
        return True
    
    # If the current cell is already filled, move to the next cell
    if board[row][col] != 0:
        next_row, next_col = (row, col + 1) if col < 3 else (row + 1, 0)
        return backtrack(board, next_row, next_col, steps)
    
    # Get the current domains based on forward checking
    domains = forward_checking(board, row, col)
    
    # Iterate over possible values for the current cell
    for num in sorted(list(domains[row][col])):
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            steps[0] += 1
            print(f"Step {steps[0]}: Assigning {num} to cell ({row+1}, {col+1})")
            print("Board: ")
            visualize_board(board)
            print("Domains: ")
            visualize_board(board, forward_checking(board, row, col), print_domains=True)

            print("\n")
            
            next_row, next_col = (row, col + 1) if col < 3 else (row + 1, 0)
            
            if steps[0] >= 10:
                return True
            
            # Recursively continue the search
            if backtrack(board, next_row, next_col, steps):
                return True
            
            # If the assignment didn't lead to a solution, backtrack
            board[row][col] = 0
            
    return False

# Initialize the counter for steps and perform backtracking

if __name__ == "__main__":
    # Initialize the 4x4 Sudoku board
    board = np.zeros((4, 4), dtype=int)
    board[0][1] = 1
    board[1][2] = 1
    board[2][1] = 4
    board[2][3] = 3
    board[3][1] = 3

    board
    # Get the initial domains after forward checking
    initial_domains = forward_checking(board, 0, 0)
    initial_domains
    steps = [0]
    backtrack(board, 0, 0, steps)