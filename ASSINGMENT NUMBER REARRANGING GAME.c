#include <stdio.h>

int main() {
    int grid[5][5] = {
        { 1,  2,  3,  4,  5},
        { 6,  7,  8,  9, 10},
        {11, 12, 13, 14, 15},
        {16, 17, 18, 19, 20},
        {21, 22, 23, 0, 24}  // Scrambled for starting position
    };

    char move;
    int moves = 0;
    int i, j;

    printf("Welcome to the Scribbled Numbers Game!\n");

    while (1) {
        // Display the current grid state
        for (i = 0; i < 5; i++) {
            for (j = 0; j < 5; j++) {
                if (grid[i][j] == 0)
                    printf("   "); // Print space for the empty tile
                else
                    printf("%2d ", grid[i][j]); // Print the number
            }
            printf("\n");
        }
      									
        // Check if the player has won
        int won = 1;
        for (i = 0; i < 5; i++) {
            for (j = 0; j < 5; j++) {
                if (i == 4 && j == 4) {
                    if (grid[i][j] != 0) won = 0; // Last tile must be empty
                } else {
                    if (grid[i][j] != (i * 5 + j + 1)) won = 0; // Check if tiles are in correct order
                }
            }
        }

        // controlls
        printf("Enter move (w/a/s/d for up/left/down/right, q to quit, r to see rules): ");
        scanf(" %c", &move);

        if (move == 'q') {
            printf("You exited the game after %d moves.\n", moves);
            break;
        } else if (move == 'r') {
            printf("Rules:\n");
            printf("1. The game consists of a 5x5 grid with numbers from 1 to 24 and one empty space (0).\n");
            printf("2. Your goal is to arrange the numbers in ascending order by moving them into the empty space.\n");
            printf("\nControls:\n");
            printf("   - 'w' to move a number up\n");
            printf("   - 'a' to move a number left\n");
            printf("   - 's' to move a number down\n");
            printf("   - 'd' to move a number right\n");
            printf("   - 'q' to quit the game at any time.\n");
            printf("Good luck!\n\n");
            continue;
        }

        // Find the position of the empty tile (0)
        int emptyRow, emptyCol;
        for (i = 0; i < 5; i++) {
            for (j = 0; j < 5; j++) {
                if (grid[i][j] == 0) { // Locate the empty space
                    emptyRow = i;
                    emptyCol = j;
                }
            }
        }

        // Determine the target position based on user input
        int targetRow = emptyRow;
        int targetCol = emptyCol;

        if (move == 'w') targetRow--; // Move the empty tile up
        else if (move == 's') targetRow++; // Move the empty tile down
        else if (move == 'a') targetCol--; // Move the empty tile left
        else if (move == 'd') targetCol++; // Move the empty tile right

        // Check if the move is within the bounds of the grid
        if (targetRow >= 0 && targetRow < 5 && targetCol >= 0 && targetCol < 5) {
            // Perform the move
            grid[emptyRow][emptyCol] = grid[targetRow][targetCol]; // Move the number into the empty space
            grid[targetRow][targetCol] = 0; // Update the empty space position
            moves++; // Increment the move counter
            
            won = 1;// Check if the player has won after the move
            for (i = 0; i < 5; i++) {
                for (j = 0; j < 5; j++) {
                    if (i == 4 && j == 4) {
                        if (grid[i][j] != 0) {
						  won = 0; // Last tile must be empty
					}
                    } else {
                        if (grid[i][j] != (i * 5 + j + 1)) {
						won = 0; // Check if tiles are in correct order
					}
                    }
                }
            }

            if (won) {
                printf("Congratulations! You've completed the game in %d moves.\n", moves);
                break; // Exit the game loop
            }
        } else {
            // Notify the user of an invalid move
            printf("Move not possible! Please try a different direction.\n");
        }
    }

    return 0; // End of the program
}

