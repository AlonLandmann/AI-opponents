#include <stdio.h>
#include <stdlib.h>

// generic functions
int maxFromArray(int numbers[], int length) {
    // returns the largest integer of an array
    int i;
    int current = numbers[0];
    for(i = 1; i < length; i++) {
        current = current >= numbers[i] ? current : numbers[i];
    }
    return current;
}
int minFromArray(int numbers[], int length) {
    // returns the smallest integer of an array
    int i;
    int current = numbers[0];
    for(i = 1; i < length; i++) {
        current = current <= numbers[i] ? current : numbers[i];
    }
    return current;
}
int matchFirstIndex(int array[], int length, int value) {
    // returns the index of the first element with a given value in an array
    int i;
    for(i = 0; i < length; i++) {
        if(array[i] == value) {
            return i;
        }
    }
    return -1;
}

// program specific functions
void paint(char position[9]) {
    // prints a position to the console
    printf("%c %c %c\n%c %c %c\n%c %c %c\n\n", position[0], position[1], position[2], position[3], position[4], position[5], position[6], position[7], position[8]);
}
int isFree(char position[9], int field) {
    // checks if a field is free
    if(position[field] == '-') return 1;
    return 0;
}
int determineResult(char position[9]) {
    // determines the result of a position if there is one (0: undecided, 1: X wins, 2: draw, 3: O wins)
    int i, j;
    int horiX, horiO, vertX, vertO;
    int undecided = 0;
    for(i = 0; i < 3; i++) {
        horiX = 0;
        horiO = 0;
        vertX = 0;
        vertO = 0;
        for(j = 0; j < 3; j++) {
            if(position[i * 3 + j] == '-') undecided = 1;
            if(position[i * 3 + j] == 'X') horiX++;
            if(position[i * 3 + j] == 'O') horiO++;
            if(position[j * 3 + i] == 'X') vertX++;
            if(position[j * 3 + i] == 'O') vertO++;
        }
        if(horiX == 3 || vertX == 3) return 1;
        if(horiO == 3 || vertO == 3) return 3;
    }
    if(position[0] == 'X' && position[4] == 'X' && position[8] == 'X') return 1;
    if(position[2] == 'X' && position[4] == 'X' && position[6] == 'X') return 1;
    if(position[0] == 'O' && position[4] == 'O' && position[8] == 'O') return 3;
    if(position[2] == 'O' && position[4] == 'O' && position[6] == 'O') return 3;
    if(undecided == 0) return 2;
    return 0;
}
char determineTurn(char position[9]) {
    // determines who's turn it is
    int i;
    int countX = 0, countO = 0;
    for(i = 0; i < 9; i++) {
        if(position[i] == 'X') countX++;
        if(position[i] == 'O') countO++;
    }
    if(countX <= countO) return 'X';
    return 'O';
}
void move(char oldPosition[9], char newPosition[9], int field, char player) {
    // makes a move from a position onto a new position
    int i;
    for(i = 0; i < 9; i++) {
        newPosition[i] = oldPosition[i];
    }
    if(newPosition[field] == '-' && determineResult(newPosition) == 0) {
        newPosition[field] = player;
    }
}
int dive(char position[9], int *moveToPlay) {
    // the recursive function that determines the best move in any given position
    int i, j = 0;
    char nodes[9][9];
    int evals[9];
    int moves[9];
    if(determineResult(position) != 0) {
        *moveToPlay = -1;
        return determineResult(position);
    }
    for(i = 0; i < 9; i++) {
        if(isFree(position, i)) {
            move(position, nodes[j], i, determineTurn(position));
            evals[j] = dive(nodes[j], moveToPlay);
            moves[j] = i;
            j++;
        }
    }
    if(determineTurn(position) == 'X') {
        *moveToPlay = moves[matchFirstIndex(evals, j, minFromArray(evals, j))];
        return minFromArray(evals, j);
    }
    if(determineTurn(position) == 'O') {
        *moveToPlay = moves[matchFirstIndex(evals, j, maxFromArray(evals, j))];
        return maxFromArray(evals, j);
    }
    return -1;
}
int getMove(int mode, char player) {
    // requests and returns user input for a move
    int move;
    if(mode == 0) printf("Enter your move: ");
    if(mode == 1 && player == 'X') printf("Player 1 (X), enter your move: ");
    if(mode == 1 && player == 'O') printf("Player 2 (O), enter your move: ");
    scanf("%d", &move);
    return move - 1;
}
void makeNextMove(char position[9], int *movePointer, int mode, char human) {
     // executes all the steps for a move to be played
    if(determineResult(position) == 0) {
        if(mode == 1) {
            move(position, position, getMove(mode, determineTurn(position)), determineTurn(position));
        }
        if(mode == 0 && determineTurn(position) == human) {
            move(position, position, getMove(mode, determineTurn(position)), determineTurn(position));
        } else if(mode == 0) {
            printf("The computer is thinking...\n");
            dive(position, movePointer);
            move(position, position, *movePointer, determineTurn(position));
        }
        paint(position);
    }
}

// main function
int main() {

    // initialization
    char currentPosition[9] = {'-', '-', '-', '-', '-', '-', '-', '-', '-'};
    char demoPosition[9] = {'1', '2', '3', '4', '5', '6', '7', '8', '9'};
    int currentMove;
    int *currentMovePointer = &currentMove;
    int mode = -1;
    char human = '-';

    // program
    printf("Welcome to TicTacToe unbeatable!\n\nThe squares of the board are numbered from 1-9 as shown:\n\n");
    paint(demoPosition);
    printf("To make a move, enter the number of the target square.\nNow, enter 0 if you want to play against the unbeatable computer or enter 1 if you want to play with another human: ");
    while(mode != 0 && mode != 1) {
          scanf("%d", &mode);
    }
    if(mode == 0) {
        printf("\nPlease enter the character X if you want to start the game or the character O if you want the computer to start: ");
        while(human != 'X' && human != 'O') {
              scanf("%c", &human);
        }
    }
    printf("\nThank you and good luck...\n");
    if(mode == 1 || human == 'X') {
        paint(currentPosition);
    }
    while(determineResult(currentPosition) == 0) {
        makeNextMove(currentPosition, currentMovePointer, mode, human);
    }
    if(mode == 0 && ((human == 'X' && determineResult(currentPosition) == 1) || (human == 'O' && determineResult(currentPosition) == 3))) printf("VICTORY!\n");
    if(mode == 0 && ((human == 'X' && determineResult(currentPosition) == 3) || (human == 'O' && determineResult(currentPosition) == 1))) printf("DEFEAT!\n");
    if(mode == 1 && determineResult(currentPosition) == 1) printf("PLAYER 1 (X) WINS!\n");
    if(mode == 1 && determineResult(currentPosition) == 3) printf("PLAYER 2 (O) WINS!\n");
    if(determineResult(currentPosition) == 2) printf("It's a draw.\n");

    // exit
    return 0;
}
