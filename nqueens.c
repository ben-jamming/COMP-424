#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

int m;
int m_minus_1;

void printBoard(int* queens) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            if (j == queens[i]) {
                printf("1 ");
            } else {
                printf("0 ");
            }
        }
        printf("\n");
    }
    printf("\n");
}

int diag_i(int row, int col) {
    return row - col + m - 1;
}

int adiag_i(int row, int col) {
    return row + col;
}

void build_conflicts(int* queens, int* conflicts) {
    int* row_conflicts = (int*)malloc(m * sizeof(int));
    int* diag_conflicts = (int*)malloc(2 * m * sizeof(int));
    int* anti_diag_conflicts = (int*)malloc(2 * m * sizeof(int));

    for (int i = 0; i < m; i++) {
        row_conflicts[i] = -1;
    }
    for (int i = 0; i < 2 * m - 1; i++) {
        diag_conflicts[i] = -1;
        anti_diag_conflicts[i] = -1;
    }

    for (int col = 0; col < m; col++) {
        int row = queens[col];
        row_conflicts[row]++;
        diag_conflicts[diag_i(row, col)]++;
        anti_diag_conflicts[adiag_i(row, col)]++;
    }

    for (int col = 0; col < m; col++) {
        int row = queens[col];
        conflicts[col] = row_conflicts[row] + diag_conflicts[diag_i(row, col)] + anti_diag_conflicts[adiag_i(row, col)];
    }

    free(row_conflicts);
    free(diag_conflicts);
    free(anti_diag_conflicts);
}

void construct_A(int* queens) {
    int n = m / 2;
    for (int k = 1; k <= n; k++) {
        queens[k-1] = 2*k-1;
        queens[2*n-k] = 2*n-2*k;
    }
}

void construct_B(int* queens) {
    int n = m / 2;
    for (int k = 1; k <= n; k++) {
        queens[k-1] = (1 + (2*(k-1) + n-1) % m) - 1;
        queens[2*n-k] = (2*n - (2*(k-1) + n-1) % m) - 1;
    }
}

void construct_C(int* queens) {
    queens[m-1] = m-1;
}

int main() {
    printf("Enter the maximum value of m: ");
    scanf("%d", &m);

    if (m < 4) {
        printf("The solution is applicable for m >= 4 only.\n");
        return 1;
    }

    int* queens = (int*)malloc(m * sizeof(int));
    for (int i = 0; i < m; i++) {
        queens[i] = -1;
    }

    if (m % 2 == 0) {
        if (m % 6 != 2 && m % 6 != 3) {
            construct_A(queens);
        } else {
            construct_B(queens);
        }
    } else if ((m - 1) % 6 != 0 && (m - 1) % 6 != 2) {
    construct_C(queens);
    } else {
        printf("No solution for m = %d based on provided constructions.\n", m);
        free(queens);
        return 1;
    }
    int total_conflicts = 0;
    int* conflicts = (int*)malloc(m * sizeof(int));
    build_conflicts(queens, conflicts);
    for (int i = 0; i < m; i++) {
        total_conflicts += conflicts[i];
    }
    printf("Total conflicts: %d\n", total_conflicts);
    free(conflicts);
    //printBoard(queens);
    free(queens);
    return 0;
}
