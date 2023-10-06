// Student ID: 260976774
// Name: Ben Hepditch
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

#define N 30 // Define the board size. Adjust N for different board sizes.

// Function to count the number of conflicts in the current board configuration
int countConflicts(int board[N]) {
    int conflicts = 0; // Initialize conflict count to 0

    // Arrays to mark the diagonals and rows occupied by queens
    int leftDiagonal[2*N] = {0};  // Main diagonal (top-left to bottom-right)
    int rightDiagonal[2*N] = {0}; // Anti-diagonal (top-right to bottom-left)
    int row[N] = {0};             // Rows occupied by queens

    // Iterate over each column (queen) in the board
    for (int i = 0; i < N; i++) {
        int j = board[i]; // Get the row of the queen in the i-th column

        // Check for conflicts with previously placed queens
        if (leftDiagonal[i - j + N - 1] || rightDiagonal[i + j] || row[j]) {
            conflicts++;
        }

        // Mark the current queen's position to detect future conflicts
        leftDiagonal[i - j + N - 1] = 1;
        rightDiagonal[i + j] = 1;
        row[j] = 1;
    }

    return conflicts;
}

// Function to check if placing a queen at a specific position is safe
bool isSafe(int board[N], int col, int row) {
    // Check for conflicts with previously placed queens
    for (int i = 0; i < col; i++) {
        // Check for row and diagonal conflicts
        if (board[i] == row || abs(board[i] - row) == abs(i - col)) {
            return false; // Conflict found, placement is not safe
        }
    }
    return true; // No conflict found, placement is safe
}

// Recursive backtracking function to solve the N-Queens problem
bool solveNQueens(int board[N], int col) {
    if (col >= N) {
        return true; // All queens are successfully placed
    }

    // Try placing a queen in each row of the current column
    for (int row = 0; row < N; row++) {
        if (isSafe(board, col, row)) {
            board[col] = row; // Place the queen
            if (solveNQueens(board, col + 1)) {
                return true; // Continue with the next column
            }
            // If no valid position found, backtrack (handled by the loop's next iteration)
        }
    }
    return false; // No safe position found for this column
}

int main() {
    int board[N];
    for (int i = 0; i < N; i++) {
        board[i] = -1; // Initialize the board with no queens placed
    }

    if (solveNQueens(board, 0) == false) {
        printf("Solution does not exist\n");
    } else {
        // Display the number of conflicts (should be 0 for a correct solution)
        printf("Number of conflicts: %d\n", countConflicts(board));
        // Display the solution
        for (int i = 0; i < N; i++) {
            printf("%d ", board[i]);
        }
    }
    return 0;
}