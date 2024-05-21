#include <stdio.h>

#define UNDEFINED -1000
#define O_WIN -200
#define DRAW 0
#define X_WIN +200
#define UNDECIDED +1000

#define WEIGHT_DOUBLE 65
#define WEIGHT_SINGLE 25
#define WEIGHT_CENTRAL 10

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
void paint(char position[42]) {
    // prints a position to the console
    int row;
    for(row = 0; row < 6; row++) {
        printf("%c  %c  %c  %c  %c  %c  %c\n", position[row * 7 + 0], position[row * 7 + 1], position[row * 7 + 2], position[row * 7 + 3], position[row * 7 + 4], position[row * 7 + 5], position[row * 7 + 6]);
    }
    printf("\n");
}
int isFree(char position[42], int column) {
    // checks if a column still has space left
    if(position[column] == '-') {
        return 1;
    }
    return 0;
}
int determineResult(char position[42]) {
    // determines the result of a position if there is one
    int row, col;
    for(row = 0; row < 6; row++) {
        for(col = 0; col < 4; col++) {
            if(position[row * 7 + col] == 'X' && position[row * 7 + (col + 1)] == 'X' && position[row * 7 + (col + 2)] == 'X' && position[row * 7 + (col + 3)] == 'X') return X_WIN;
            if(position[row * 7 + col] == 'O' && position[row * 7 + (col + 1)] == 'O' && position[row * 7 + (col + 2)] == 'O' && position[row * 7 + (col + 3)] == 'O') return O_WIN;
        }
    }
    for(row = 0; row < 3; row++) {
        for(col = 0; col < 7; col++) {
            if(position[row * 7 + col] == 'X' && position[(row + 1) * 7 + col] == 'X' && position[(row + 2) * 7 + col] == 'X' && position[(row + 3) * 7 + col] == 'X') return X_WIN;
            if(position[row * 7 + col] == 'O' && position[(row + 1) * 7 + col] == 'O' && position[(row + 2) * 7 + col] == 'O' && position[(row + 3) * 7 + col] == 'O') return O_WIN;
        }
    }
    for(row = 0; row < 3; row++) {
        for(col = 0; col < 4; col++) {
            if(position[row * 7 + col] == 'X' && position[(row + 1) * 7 + (col + 1)] == 'X' && position[(row + 2) * 7 + (col + 2)] == 'X' && position[(row + 3) * 7 + (col + 3)] == 'X') return X_WIN;
            if(position[row * 7 + col] == 'O' && position[(row + 1) * 7 + (col + 1)] == 'O' && position[(row + 2) * 7 + (col + 2)] == 'O' && position[(row + 3) * 7 + (col + 3)] == 'O') return O_WIN;
        }
    }
    for(row = 0; row < 3; row++) {
        for(col = 3; col < 7; col++) {
            if(position[row * 7 + col] == 'X' && position[(row + 1) * 7 + (col - 1)] == 'X' && position[(row + 2) * 7 + (col - 2)] == 'X' && position[(row + 3) * 7 + (col - 3)] == 'X') return X_WIN;
            if(position[row * 7 + col] == 'O' && position[(row + 1) * 7 + (col - 1)] == 'O' && position[(row + 2) * 7 + (col - 2)] == 'O' && position[(row + 3) * 7 + (col - 3)] == 'O') return O_WIN;
        }
    }
    for(col = 0; col < 7; col++) {
        if(isFree(position, col)) return UNDECIDED;
    }
    return DRAW;
}
int determineHeuristic(char position[42]) {
    int row, col;
    int doubleX = 0, doubleO = 0;
    int singleX = 0, singleO = 0;
    int centralX = 0, centralO = 0;
    int totalX = 0, totalO = 0;
    double doubleFactor = 0.0;
    double singleFactor = 0.0;
    double centralFactor = 0.0;
    for(row = 0; row < 6; row++) {
        for(col = 0; col < 3; col++) {
            if(position[row * 7 + col] == '-' && position[row * 7 + (col + 1)] == 'X' && position[row * 7 + (col + 2)] == 'X' && position[row * 7 + (col + 3)] == 'X' && position[row * 7 + (col + 4)] == '-') doubleX++;
            if(position[row * 7 + col] == '-' && position[row * 7 + (col + 1)] == 'O' && position[row * 7 + (col + 2)] == 'O' && position[row * 7 + (col + 3)] == 'O' && position[row * 7 + (col + 4)] == '-') doubleO++;
        }
    }
    for(row = 0; row < 2; row++) {
        for(col = 0; col < 3; col++) {
            if(position[row * 7 + col] == '-' && position[(row + 1) * 7 + (col + 1)] == 'X' && position[(row + 2) * 7 + (col + 2)] == 'X' && position[(row + 3) * 7 + (col + 3)] == 'X' && position[(row + 4) * 7 + (col + 4)] == '-') doubleX++;
            if(position[row * 7 + col] == '-' && position[(row + 1) * 7 + (col + 1)] == 'O' && position[(row + 2) * 7 + (col + 2)] == 'O' && position[(row + 3) * 7 + (col + 3)] == 'O' && position[(row + 4) * 7 + (col + 4)] == '-') doubleO++;
        }
    }
    for(row = 0; row < 2; row++) {
        for(col = 4; col < 7; col++) {
            if(position[row * 7 + col] == '-' && position[(row + 1) * 7 + (col - 1)] == 'X' && position[(row + 2) * 7 + (col - 2)] == 'X' && position[(row + 3) * 7 + (col - 3)] == 'X' && position[(row + 4) * 7 + (col - 4)] == '-') doubleX++;
            if(position[row * 7 + col] == '-' && position[(row + 1) * 7 + (col - 1)] == 'O' && position[(row + 2) * 7 + (col - 2)] == 'O' && position[(row + 3) * 7 + (col - 3)] == 'O' && position[(row + 4) * 7 + (col - 4)] == '-') doubleO++;
        }
    }
    for(row = 0; row < 6; row++) {
        for(col = 0; col < 4; col++) {
            if(position[row * 7 + col] == '-' && position[row * 7 + (col + 1)] == 'X' && position[row * 7 + (col + 2)] == 'X' && position[row * 7 + (col + 3)] == 'X') singleX++;
            if(position[row * 7 + col] == 'X' && position[row * 7 + (col + 1)] == 'X' && position[row * 7 + (col + 2)] == 'X' && position[row * 7 + (col + 3)] == '-') singleX++;
            if(position[row * 7 + col] == '-' && position[row * 7 + (col + 1)] == 'O' && position[row * 7 + (col + 2)] == 'O' && position[row * 7 + (col + 3)] == 'O') singleO++;
            if(position[row * 7 + col] == 'O' && position[row * 7 + (col + 1)] == 'O' && position[row * 7 + (col + 2)] == 'O' && position[row * 7 + (col + 3)] == '-') singleO++;
        }
    }
    for(row = 0; row < 3; row++) {
        for(col = 0; col < 7; col++) {
            if(position[row * 7 + col] == '-' && position[(row + 1) * 7 + col] == 'X' && position[(row + 2) * 7 + col] == 'X' && position[(row + 3) * 7 + col] == 'X') singleX++;
            if(position[row * 7 + col] == '-' && position[(row + 1) * 7 + col] == 'O' && position[(row + 2) * 7 + col] == 'O' && position[(row + 3) * 7 + col] == 'O') singleO++;
        }
    }
	for(row = 0; row < 3; row++) {
        for(col = 0; col < 4; col++) {
            if(position[row * 7 + col] == '-' && position[(row + 1) * 7 + (col + 1)] == 'X' && position[(row + 2) * 7 + (col + 2)] == 'X' && position[(row + 3) * 7 + (col + 3)] == 'X') singleX++;
            if(position[row * 7 + col] == '-' && position[(row + 1) * 7 + (col + 1)] == 'O' && position[(row + 2) * 7 + (col + 2)] == 'O' && position[(row + 3) * 7 + (col + 3)] == 'O') singleO++;
			if(position[row * 7 + col] == 'X' && position[(row + 1) * 7 + (col + 1)] == 'X' && position[(row + 2) * 7 + (col + 2)] == 'X' && position[(row + 3) * 7 + (col + 3)] == '-') singleX++;
            if(position[row * 7 + col] == 'O' && position[(row + 1) * 7 + (col + 1)] == 'O' && position[(row + 2) * 7 + (col + 2)] == 'O' && position[(row + 3) * 7 + (col + 3)] == '-') singleO++;
        }
    }
    for(row = 0; row < 3; row++) {
        for(col = 3; col < 7; col++) {
            if(position[row * 7 + col] == '-' && position[(row + 1) * 7 + (col - 1)] == 'X' && position[(row + 2) * 7 + (col - 2)] == 'X' && position[(row + 3) * 7 + (col - 3)] == 'X') singleX++;
            if(position[row * 7 + col] == '-' && position[(row + 1) * 7 + (col - 1)] == 'O' && position[(row + 2) * 7 + (col - 2)] == 'O' && position[(row + 3) * 7 + (col - 3)] == 'O') singleO++;
			if(position[row * 7 + col] == 'X' && position[(row + 1) * 7 + (col - 1)] == 'X' && position[(row + 2) * 7 + (col - 2)] == 'X' && position[(row + 3) * 7 + (col - 3)] == '-') singleX++;
            if(position[row * 7 + col] == 'O' && position[(row + 1) * 7 + (col - 1)] == 'O' && position[(row + 2) * 7 + (col - 2)] == 'O' && position[(row + 3) * 7 + (col - 3)] == '-') singleO++;
        }
    }
    for(row = 0; row < 6; row++) {
        for(col = 0; col < 7; col++) {
            if(position[row * 7 + col] == 'X') {
                totalX++;
                if(col == 0 || col == 6) centralX += 1;
                if(col == 1 || col == 5) centralX += 2;
                if(col == 2 || col == 4) centralX += 5;
                if(col == 3) centralX += 8;
                if(row == 1 || row == 4) centralX += 1;
                if(row == 2 || row == 3) centralX += 2;
            }
            if(position[row * 7 + col] == 'O') {
                totalO++;
                if(col == 0 || col == 6) centralO += 1;
                if(col == 1 || col == 5) centralO += 2;
                if(col == 2 || col == 4) centralO += 5;
                if(col == 3) centralO += 8;
                if(row == 1 || row == 4) centralO += 1;
                if(row == 2 || row == 3) centralO += 2;
            }
        }
    }
    if(doubleX + doubleO > 0) {
        doubleFactor = (double)(doubleX - doubleO) / (double)(doubleX + doubleO);
    }
    if(singleX + singleO > 0) {
        singleFactor = (double)(singleX - singleO) / (double)(singleX + singleO);
    }
    if(totalX > 0 && totalO > 0) {
        centralFactor = (((double)centralX / (double)totalX) - ((double)centralO / (double)totalO)) / 10.0;
    }
    return (int)((double)WEIGHT_DOUBLE * doubleFactor + (double)WEIGHT_SINGLE * singleFactor + (double)WEIGHT_CENTRAL * centralFactor);
}
char determineTurn(char position[42]) {
    // determines who's turn it is
    int i;
    int countX = 0, countO = 0;
    for(i = 0; i < 42; i++) {
        if(position[i] == 'X') countX++;
        if(position[i] == 'O') countO++;
    }
    if(countX <= countO) {
        return 'X';
    }
    return 'O';
}
void move(char oldPosition[42], char newPosition[42], int column, char turn) {
    // makes a move from a position onto a new position
    int i, row;
    for(i = 0; i < 42; i++) {
        newPosition[i] = oldPosition[i];
    }
    if(isFree(newPosition, column) && determineResult(newPosition) == UNDECIDED) {
        for(row = 5; row >= 0; row--) {
            if(newPosition[row * 7 + column] == '-') {
                newPosition[row * 7 + column] = turn;
                row = -1;
            }
        }
    }
}

// algorithms
int dive(char position[42], int *moveToPlay, int *nodeCounter) {
    // primitive minMax algorithm
    int i, j = 0;
    char candidateNodes[7][42];
    int candidateEvals[7];
    int candidateMoves[7];
    int result = determineResult(position);
    char turn = determineTurn(position);
    int minMax;
    *nodeCounter = *nodeCounter + 1;
    if(result != UNDECIDED) {
        *moveToPlay = -1;
        return result;
    }
    for(i = 0; i < 7; i++) {
        if(isFree(position, i)) {
            move(position, candidateNodes[j], i, turn);
            candidateEvals[j] = dive(candidateNodes[j], moveToPlay, nodeCounter); // recursive call
            candidateMoves[j] = i;
            j++;
        }
    }
    if(turn == 'X') {
        minMax = maxFromArray(candidateEvals, j);
        *moveToPlay = candidateMoves[matchFirstIndex(candidateEvals, j, minMax)];
        return minMax;
    }
    if(turn == 'O') {
        minMax = minFromArray(candidateEvals, j);
        *moveToPlay = candidateMoves[matchFirstIndex(candidateEvals, j, minMax)];
        return minMax;
    }
    return -1;
}
int edgeDive(char position[42], int *moveToPlay, int *nodeCounter) {
    // slightly improved algorithm with edge trimming
    int i, j = 0;
    char candidateNodes[7][42];
    int candidateEvals[7];
    int candidateMoves[7];
    int result = determineResult(position);
    char turn = determineTurn(position);
    int minMax;
    *nodeCounter = *nodeCounter + 1;
    if(result != UNDECIDED) {
        *moveToPlay = -1;
        return result;
    }
    for(i = 0; i < 7; i++) {
        if(isFree(position, i)) {
            move(position, candidateNodes[j], i, turn);
            candidateEvals[j] = edgeDive(candidateNodes[j], moveToPlay, nodeCounter); // recursive call
            candidateMoves[j] = i;
            if(turn == 'X' && candidateEvals[j] == X_WIN) {
                *moveToPlay = i;
                return X_WIN;
            }
            if(turn == 'O' && candidateEvals[j] == O_WIN) {
                *moveToPlay = i;
                return O_WIN;
            }
            j++;
        }
    }
    if(turn == 'X') {
        minMax = maxFromArray(candidateEvals, j);
        *moveToPlay = candidateMoves[matchFirstIndex(candidateEvals, j, minMax)];
        return minMax;
    }
    if(turn == 'O') {
        minMax = minFromArray(candidateEvals, j);
        *moveToPlay = candidateMoves[matchFirstIndex(candidateEvals, j, minMax)];
        return minMax;
    }
    return -1;
}
int alphaBetaEdgeDive(char position[42], int *moveToPlay, int *nodeCounter, int alphaBetaValue) {
    // improved algorithm with edge and alpha-beta trimming
    int i, j = 0;
    char candidateNodes[7][42];
    int candidateEvals[7];
    int candidateMoves[7];
    int result = determineResult(position);
    char turn = determineTurn(position);
    int minMax;
    int sendAlphaBeta = UNDEFINED;
    *nodeCounter = *nodeCounter + 1;
    if(result != UNDECIDED) {
        *moveToPlay = -1;
        return result;
    }
    for(i = 0; i < 7; i++) {
        if(isFree(position, i)) {
            move(position, candidateNodes[j], i, turn);
            candidateEvals[j] = alphaBetaEdgeDive(candidateNodes[j], moveToPlay, nodeCounter, sendAlphaBeta); // recursive call
            candidateMoves[j] = i;
            if(turn == 'X' && candidateEvals[j] == X_WIN) {
                *moveToPlay = i;
                return X_WIN;
            }
            if(turn == 'O' && candidateEvals[j] == O_WIN) {
                *moveToPlay = i;
                return O_WIN;
            }
            if(alphaBetaValue != UNDEFINED && turn == 'X' && candidateEvals[j] >= alphaBetaValue) {
                return candidateEvals[j];
            }
            if(alphaBetaValue != UNDECIDED && turn == 'O' && candidateEvals[j] <= alphaBetaValue) {
                return candidateEvals[j];
            }
            if(turn == 'X') {
                sendAlphaBeta = minFromArray(candidateEvals, j + 1);
            }
            if(turn == 'O') {
                sendAlphaBeta = maxFromArray(candidateEvals, j + 1);
            }
            j++;
        }
    }
    if(turn == 'X') {
        minMax = minFromArray(candidateEvals, j);
        *moveToPlay = candidateMoves[matchFirstIndex(candidateEvals, j, minMax)];
        return minMax;
    }
    if(turn == 'O') {
        minMax = maxFromArray(candidateEvals, j);
        *moveToPlay = candidateMoves[matchFirstIndex(candidateEvals, j, minMax)];
        return minMax;
    }
    return -1;
}
int limitDive(char position[42], int *moveToPlay, int *nodeCounter, int alphaBetaValue, int currentDepth, int depthLimit) {
    // improved algorithm with edge and alpha-beta trimming that stops at a certain depth
    int i, j = 0;
    char candidateNodes[7][42];
    int candidateEvals[7];
    int candidateMoves[7];
    int result = determineResult(position);
    char turn = determineTurn(position);
    int minMax;
    int sendAlphaBeta = UNDEFINED;
    *nodeCounter = *nodeCounter + 1;
    if(result != UNDECIDED) {
        *moveToPlay = -1;
        return result;
    }
    currentDepth++;
    if(currentDepth == depthLimit) {
        *moveToPlay = -1;
        return determineHeuristic(position);
    }
    for(i = 0; i < 7; i++) {
        if(isFree(position, i)) {
            move(position, candidateNodes[j], i, turn);
            candidateEvals[j] = limitDive(candidateNodes[j], moveToPlay, nodeCounter, sendAlphaBeta, currentDepth, depthLimit); // recursive call
            candidateMoves[j] = i;
            if(turn == 'X' && candidateEvals[j] == X_WIN) {
                *moveToPlay = i;
                return X_WIN;
            }
            if(turn == 'O' && candidateEvals[j] == O_WIN) {
                *moveToPlay = i;
                return O_WIN;
            }
            if(alphaBetaValue != UNDEFINED && turn == 'X' && candidateEvals[j] >= alphaBetaValue) {
                return candidateEvals[j];
            }
            if(alphaBetaValue != UNDEFINED && turn == 'O' && candidateEvals[j] <= alphaBetaValue) {
                return candidateEvals[j];
            }
            if(turn == 'X') {
                sendAlphaBeta = minFromArray(candidateEvals, j + 1);
            }
            if(turn == 'O') {
                sendAlphaBeta = maxFromArray(candidateEvals, j + 1);
            }
            j++;
        }
    }
    if(turn == 'X') {
        minMax = maxFromArray(candidateEvals, j);
        *moveToPlay = candidateMoves[matchFirstIndex(candidateEvals, j, minMax)];
        return minMax;
    }
    if(turn == 'O') {
        minMax = minFromArray(candidateEvals, j);
        *moveToPlay = candidateMoves[matchFirstIndex(candidateEvals, j, minMax)];
        return minMax;
    }
    return -1;
}

// ui functions
int getMove(int mode, char turn) {
    // requests and returns user input for a move
    int move;
    if(mode > 0) printf("Enter your move: ");
    if(mode == 0 && turn == 'X') printf("Player 1 (X), enter your move: ");
    if(mode == 0 && turn == 'O') printf("Player 2 (O), enter your move: ");
    scanf("%d", &move);
    return move - 1;
}
void makeNextMove(char position[42], int mode, char humanCharacter, int *movePointer, int *nodeCounter) {
    // executes all the steps for a move to be played
    int evaluation;
    char turn = determineTurn(position);
    if(determineResult(position) == UNDECIDED) {
        if(mode == 0) {
            move(position, position, getMove(mode, turn), turn);
        }
        if(mode > 0) {
            if(turn == humanCharacter) {
                move(position, position, getMove(mode, turn), turn);
            } else {
                *nodeCounter = 0;
                printf("The computer is thinking...\n");
                evaluation = limitDive(position, movePointer, nodeCounter, UNDEFINED, 0, mode * 2);
                printf("Nodes reached: %d\n", *nodeCounter);
                printf("Evaluation: %d\n", evaluation);
                move(position, position, *movePointer, turn);
            }
        }
        paint(position);
    }
}

// main function
int main() {

    // initialization
    char currentPosition[42] = {
        '-', '-', '-', '-', '-', '-', '-',
        '-', '-', '-', '-', '-', '-', '-',
        '-', '-', '-', '-', '-', '-', '-',
        '-', '-', '-', '-', '-', '-', '-',
        '-', '-', '-', '-', '-', '-', '-',
        '-', '-', '-', '-', '-', '-', '-',
    };
    char demoPosition[42] = {
        '1', '2', '3', '4', '5', '6', '7',
        '1', '2', '3', '4', '5', '6', '7',
        '1', '2', '3', '4', '5', '6', '7',
        '1', '2', '3', '4', '5', '6', '7',
        '1', '2', '3', '4', '5', '6', '7',
        '1', '2', '3', '4', '5', '6', '7'
    };
    int currentMove;
    int *currentMovePointer = &currentMove;
    int nodeCounter = 0;
    int *nodeCounterPointer = &nodeCounter;
    int mode = -1;
    char humanCharacter = '-';

    // intro
    printf("=== Welcome to connect 4 almost unbeatable! ===\nThe columns of the board are numbered from 1 to 7 as shown below. To make a move, enter the number of the target column.\n\n");
    paint(demoPosition);
    printf("Now, enter 0 if you want to play against another human or enter an integer (1-8) to determine the strength of your almost unbeatable computer opponent.\nNote that levels 6-8 require significant calculation times: ");
    scanf("%d", &mode);
    if(mode > 0) {
        printf("\nPlease enter the character X if you want to start the game or the character O if you want the computer to start: ");
        while(humanCharacter != 'X' && humanCharacter != 'O') {
            scanf("%c", &humanCharacter);
        }
    }
    printf("\nThank you and good luck...\n");
    paint(currentPosition);

    // game
    while(determineResult(currentPosition) == UNDECIDED) {
        makeNextMove(currentPosition, mode, humanCharacter, currentMovePointer, nodeCounterPointer);
    }

    // result
    if(mode > 0 && ((humanCharacter == 'X' && determineResult(currentPosition) == X_WIN) || (humanCharacter == 'O' && determineResult(currentPosition) == O_WIN))) printf("=== VICTORY! ===\n");
    if(mode > 0 && ((humanCharacter == 'X' && determineResult(currentPosition) == O_WIN) || (humanCharacter == 'O' && determineResult(currentPosition) == X_WIN))) printf("=== DEFEAT! ===\n");
    if(mode == 0 && determineResult(currentPosition) == X_WIN) printf("=== PLAYER 1 (X) WINS! ===\n");
    if(mode == 0 && determineResult(currentPosition) == O_WIN) printf("=== PLAYER 2 (O) WINS! ===\n");
    if(determineResult(currentPosition) == DRAW) printf("It's a draw.\n");

    // exit
	getchar();
    return 0;
}
