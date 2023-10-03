import random

def Random(x, n):
    """Returns a random integer between x and n."""
    return random.randint(x, n)

def Swap(queens, i, j):
    """Swaps the positions of queens at indices i and j."""
    queens[i], queens[j] = queens[j], queens[i]

def InitialSearch(n):
    """Generates an initial permutation for the n-queens problem."""
    
    # Initialize the permutation with queens in default positions
    queens = list(range(1, n+1))
    
    # Arrays to track the number of queens on negative and positive diagonal lines
    negative_diagonals = [0] * (2*n - 1)
    positive_diagonals = [0] * (2*n - 1)
    
    # Randomly shuffle the queens to produce an initial permutation
    random.shuffle(queens)
    
    # Update the diagonal arrays based on the initial permutation
    for j in range(n):
        i = queens[j] - 1
        negative_diagonals[i + j] += 1
        positive_diagonals[n - 1 + i - j] += 1
    
    # Compute the number of collisions based on the diagonal arrays
    collisions = sum([(count - 1) for count in negative_diagonals if count > 1]) + \
                 sum([(count - 1) for count in positive_diagonals if count > 1])
    
    # Attempt to minimize collisions by swapping queens
    for _ in range(2*n):  # number of iterations can be adjusted
        i, j = Random(0, n-1), Random(0, n-1)
        if i != j:
            # Swap queens and check if collisions are reduced
            Swap(queens, i, j)
            
            # Recalculate the number of queens on diagonal lines after the swap
            new_negative_diagonals = [0] * (2*n - 1)
            new_positive_diagonals = [0] * (2*n - 1)
            for col in range(n):
                row = queens[col] - 1
                new_negative_diagonals[row + col] += 1
                new_positive_diagonals[n - 1 + row - col] += 1
            
            # Compute the new number of collisions after the swap
            new_collisions = sum([(count - 1) for count in new_negative_diagonals if count > 1]) + \
                             sum([(count - 1) for count in new_positive_diagonals if count > 1])
            
            # If the new number of collisions is not reduced, revert the swap
            if new_collisions >= collisions:
                Swap(queens, i, j)
            else:
                # Update the number of collisions and diagonal arrays
                collisions = new_collisions
                negative_diagonals, positive_diagonals = new_negative_diagonals, new_positive_diagonals
    
    return queens, collisions

def PartialCollisions(i, queens):
    """Returns the number of collisions on diagonals to the left of the ith column."""
    collisions = 0
    current_queen_row = queens[i]
    
    # Check queens to the left of the current queen
    for j in range(i):
        other_queen_row = queens[j]
        
        # Check for negative slope diagonal
        if current_queen_row + i == other_queen_row + j:
            collisions += 1
        
        # Check for positive slope diagonal
        if current_queen_row - i == other_queen_row - j:
            collisions += 1
    
    return collisions

def TotalCollisions(i, queens):
    """Returns the total number of collisions on diagonals for the ith queen."""
    collisions = 0
    current_queen_row = queens[i]
    
    # Check all other queens
    for j in range(len(queens)):
        if i == j:  # Skip the current queen
            continue
        other_queen_row = queens[j]
        
        # Check for negative slope diagonal
        if current_queen_row + i == other_queen_row + j:
            collisions += 1
        
        # Check for positive slope diagonal
        if current_queen_row - i == other_queen_row - j:
            collisions += 1
    
    return collisions

def FinalSearch(queens, max_steps=7000):
    """Performs the final search to resolve the positions of the queens with collisions."""
    n = len(queens)
    
    # Helper function to compute the total number of collisions for the entire board
    def compute_total_collisions():
        return sum([TotalCollisions(i, queens) for i in range(n)])
    
    total_collisions = compute_total_collisions()
    
    steps = 0
    while total_collisions > 0 and steps < max_steps:
        
        if n < 200:
            # Systematically test each queen with collisions with all other queens
            found_better_swap = False
            for i in range(n):
                if PartialCollisions(i, queens) > 0:
                    for j in range(n):
                        if i != j:
                            Swap(queens, i, j)
                            new_collisions = compute_total_collisions()
                            if new_collisions < total_collisions:
                                total_collisions = new_collisions
                                found_better_swap = True
                                break
                            else:
                                Swap(queens, i, j)  # Revert the swap if not beneficial
            if not found_better_swap:
                queens, _ = InitialSearch(n)  # Generate a new initial permutation
                total_collisions = compute_total_collisions()
        
        else:
            # Choose two queens for a possible swap
            i = Random(0, n-1)
            while PartialCollisions(i, queens) == 0:  # Ensure the first queen has collisions
                i = Random(0, n-1)
            j = Random(0, n-1)
            while j == i:
                j = Random(0, n-1)
            
            # Swap the queens and check if the total number of collisions is reduced
            Swap(queens, i, j)
            new_collisions = compute_total_collisions()
            if new_collisions < total_collisions:
                total_collisions = new_collisions
            else:
                Swap(queens, i, j)  # Revert the swap if not beneficial
        
        steps += 1
    
    return queens, total_collisions

def solve_n_queens(n):
    """Driver function to solve the n-queens problem."""
    
    # 1. Initial Search
    queens, initial_collisions = InitialSearch(n)
    
    # 2. Final Search
    final_queens, final_collisions = FinalSearch(queens)
    
    # 3. Return the final solution and number of collisions
    return final_queens, final_collisions

def visualize_solution(queens):
    """Visualizes the configuration of queens on a chessboard with a more visually appealing representation."""
    n = len(queens)
    
    # Define light and dark squares
    light_square = "□"
    dark_square = "■"
    
    # Display the board
    for i, q in enumerate(queens):
        for j in range(n):
            # Alternate between light and dark squares
            square_color = light_square if (i + j) % 2 == 0 else dark_square
            
            # Place the queen symbol if the square contains a queen, otherwise display the square color
            if j == q - 1:
                print("♛", end=" ")
            else:
                print(square_color, end=" ")
        print()  # Move to the next row

def calculate_run_time(func, *args):
    """Calculates the run time of a function."""
    import time
    start_time = time.time()
    func(*args)
    end_time = time.time()
    return end_time - start_time

def solve_n_queens_runtime(n):
    """Calculates the run time of the n-queens problem over a range of n values.
    - Creates a table of n values and run times.
    - Plots the run time against n values.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Calculate the run time for each n value
    n_values = list(range(1, n+1))
    run_times = []
    for n in n_values:
        run_time = calculate_run_time(solve_n_queens, n)
        run_times.append(run_time)
    
    # Create a table of n values and run times
    print('n\tRun Time')
    for n, run_time in zip(n_values, run_times):
        print(f'{n}\t{run_time}')
    
    # Plot the run time against n values
    plt.plot(n_values, run_times)
    plt.xlabel('n')
    plt.ylabel('Run Time (s)')
    plt.title('Run Time vs. n')
    plt.show()

if __name__ == '__main__':
    # solution, collisions = solve_n_queens(400)
    # print('Number of collisions:', collisions)
    #print(solution)
    solve_n_queens_runtime(1000)
    # Visualizing the solution obtained earlier for the 8-queens problem
    #visualize_solution(solution)

