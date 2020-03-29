#include <vector>
#include <math.h>
#include "TicTacToe.hpp"
#include <iostream>
#include <limits.h>


TicTacToe::TicTacToe(std::vector<std::vector<char>> board): _board{board}  {positionGenerator();}

void TicTacToe::count(std::vector<std::vector<char>> &curr_board, int &countX , int &countO){
    for (int x = 1; x < 5; x++) {
        for (int y = 1; y < 5; y++) {
            if (curr_board[x][y] == 'X')
                countX++;
            else if (curr_board[x][y] == 'O')
                countO++;
        }
    }
}

int checkWinner(std::vector<std::vector<char>> &curr_board) {

    bool Xrows[5] = {0, 0, 0, 0, 0};
    bool Orows[5] = {0, 0, 0, 0, 0};
    bool Xcols[5] = {0, 0, 0, 0, 0};
    bool Ocols[5] = {0, 0, 0, 0, 0};

    for (int x = 1; x < 5; x++) {
        for (int y = 1; y < 5; y++) {
            char rowpiece = curr_board[y][x];   // So what changes here is the first position according to your if statements for row
            char colpiece = curr_board[x][y];	// Then for column, the second position changes
            if (rowpiece == 'X')
                Xrows[y] = 1;		// I use y because regardless of the if statement, they always increase by 1
            if (rowpiece == 'O')
                Orows[y] = 1;
            if (colpiece == 'X')
                Xcols[y] = 1;
            if (colpiece == 'O')
                Ocols[y] = 1;
        }
    }
    if (Xcols[1] && Xcols[2] && Xcols[3] && Xcols[4]  && Xrows[1] && Xrows[2] && Xrows[3] && Xrows[4])
        return 10;
    else if (Ocols[1] && Ocols[2] && Ocols[3] && Ocols[4] && Orows[1] && Orows[2] && Orows[3] && Orows[4])
        return -10;
    else
        return 0;
}
bool TicTacToe::leaf(std::vector<std::vector<char>> &curr_board) {
    int countX = 0, countO = 0;
    count(curr_board, countX , countO);

    if ( countX ==  8 &&  countO == 8 )
        return true;
    else if( checkWinner(curr_board) != 0)
		return true;

	return false;
}

bool TicTacToe::max_node(std::vector<std::vector<char>> &current_board){
    int countX = 0, countO = 0;
    count(current_board, countX, countO);
    if ( countX <= countO)
		return true;
	return false;
}

int TicTacToe::Eval (std::vector<std::vector<char>> &curr_board){
    return checkWinner(curr_board);
}


std::vector<std::vector<std::vector<char>>> TicTacToe::successor(std::vector<std::vector<char>> &current_board, bool turn){
	std::vector<std::vector<std::vector<char>>> children;
	std::vector<std::vector<char>> newBoard  = current_board;
    for (int i = 1 ; i < 5; i++){
        for (int j =1 ; j < 5; j++){
            if (newBoard[i][j] == '\0'){
                if (turn){
                    newBoard[i][j] = 'X';
                    children.push_back(newBoard);
                    newBoard[i][j] = '\0';
                }else{
                    newBoard[i][j] = 'O';
                    children.push_back(newBoard);
                    newBoard[i][j] = '\0';
                }
            }
        }
    }
	return children;
}



int TicTacToe::minMax(std::vector<std::vector<char>>& board, int &nodes){
	int value;
	bool max_turn = false;
    int countX = 0, countO = 0;
    count(board, countX , countO);
    if ( std::abs(countX - countO) > 1) {
        std::cout<< "Invalid Board" << std::endl;
        return -1;
    }
    nodes++;
    if (leaf(board)) {
        return Eval(board);
    }

	if (max_node(board)) {
		value = INT_MIN;
		max_turn = true;
	}
	else {
		value = INT_MAX;
		max_turn = false;
	}

    std::vector<std::vector<std::vector<char>>> neighbors = successor(board,max_turn );
	for (std::vector<std::vector<char>> n : neighbors){

		if (max_node(board)) {
            value = std::max(value, minMax(n, nodes));
        }
		else {
            value = std::min(value, minMax(n,nodes));
        }
	}
	return value;
}
/**********************************************************************************************/
// THIS IS THE STUFF THAT I ADDED 
/**********************************************************************************************/

// This generates all the 4 tuple that are winning moves
void TicTacToe::positionGenerator() {
	int num = 0; // Number of possible wins
	for (int i = 1; i < 5; i++) {
		for (int j = 1; j < 5; j++) {
			if (j != i) {
				for (int k = 1; k < 5; k++) {
					if (k != i && k != j) {
						for (int l = 1; l < 5; l++) {
							if (l != i && l != j && l != k) {
								p[num][1][1] = 1;
								p[num][1][2] = i;
								p[num][2][1] = 2;
								p[num][2][2] = j;
								p[num][3][1] = 3;
								p[num][3][2] = k;
								p[num][4][1] = 4;
								p[num][4][2] = l;
								num++;
							}
						}
					}
				}
			}
		}
	}
}

// The min max with alpha and beta
int TicTacToe::minMaxAB(std::vector< std::vector<char> > &board, int depth , int A, int B, int &nodes, int &nodeAB, int &nodeMM) {
    nodes++;
	if ( leaf(board) || depth == 0) {
	    int e0 = Eval(board);
	    if (e0 != 0)
	        return e0;
        else if ( (A + B) % 2 == 0) {
			nodeMM++;
            return evalOne(board);
        } else {
			nodeAB++;
			return evalTwo(board);
		}
	}
	int res;
    if (max_node(board)) {
		res = A;
		std::vector< std::vector< std::vector<char> > > successors = successor(board, true);
		for (std::vector< std::vector<char> > c: successors) {
			int val = minMaxAB(c, depth -1, res, B, nodes, nodeAB, nodeMM);
			res = std::max(res, val);
			if (res >= B)
				return res;
		}
	} else {
		res = B;
		std::vector< std::vector< std::vector<char> > > successors = successor(board, false);
		for (std::vector< std::vector<char> > c: successors) {
			int val = minMaxAB(c, depth -1, A, res, nodes, nodeAB, nodeMM);
			res = std::min(res, val);
			if (res <= A)
				return res;
		}
	}
	return res;
}

// This is the first evaluate function 
int TicTacToe::evalOne(std::vector< std::vector<char> > board) {
	int numberofwaysX = 0;
	int numberofwaysO = 0;
	for (int n = 0; n < 24; n++) {
		// Just the positions of each tuple
		int onex = p[n][1][1];
		int oney = p[n][1][2];
		int twox = p[n][2][1];
		int twoy = p[n][2][2];
		int threex = p[n][3][1];
		int threey = p[n][3][2];
		int fourx = p[n][4][1];
		int foury = p[n][4][2];

		// This is for player1
		if ((board[onex][oney]=='X'||board[onex][oney]=='\0')&&(board[twox][twoy]=='X'||board[twox][twoy]=='\0')
		  &&(board[threex][threey]=='X'||board[threex][threey]=='\0')&&(board[fourx][foury]=='X'||board[fourx][foury]=='\0'))
			numberofwaysX++;
		// This is now for the player2
		if ((board[onex][oney]=='O'||board[onex][oney]=='\0')&&(board[twox][twoy]=='O'||board[twox][twoy]=='\0')
		  &&(board[threex][threey]=='O'||board[threex][threey]=='\0')&&(board[fourx][foury]=='O'||board[fourx][foury]=='\0'))
			numberofwaysO++;
	}
	return numberofwaysX - numberofwaysO;
}

// This is the second evaluate function
int TicTacToe::evalTwo(std::vector< std::vector<char> > board) {
	// These don't mean the same thing as the other evaluate function
	int fiveX = 0;
	int fiveO = 0;
	int twoX = 0;
	int twoO = 0;
	int oneX = 0;
	int oneO = 0;
	int countofplayer1 = 0;
	int countofplayer2 = 0;

	for (int n = 0; n < 24; n++) {
		// These here are the positions of the tuple
        int onex = p[n][1][1];
        int oney = p[n][1][2];
        int twox = p[n][2][1];
        int twoy = p[n][2][2];
        int threex = p[n][3][1];
        int threey = p[n][3][2];
        int fourx = p[n][4][1];
        int foury = p[n][4][2];
		
		// Make sure that no pieces of player 2 are in the tuple positions when checking for player1
		if (board[onex][oney]=='O' || board[twox][twoy]=='O' || board[threex][threey]=='O' || board[fourx][foury]=='O')
			continue;
		if (board[onex][oney]=='X') { countofplayer1++; }
		if (board[twox][twoy]=='X') { countofplayer1++; }
		if (board[threex][threey]=='X') { countofplayer1++; }
		if (board[fourx][foury]=='X' && countofplayer1 <= 3) { countofplayer1++; }

		if (countofplayer1 == 3) { fiveX++; }
		if (countofplayer1 == 2) { twoX++;  }
		if (countofplayer1 == 1) { oneX++;  }
	}

	for (int n = 0; n < 24; n++) {
        int onex = p[n][1][1];
        int oney = p[n][1][2];
        int twox = p[n][2][1];
        int twoy = p[n][2][2];
        int threex = p[n][3][1];
        int threey = p[n][3][2];
        int fourx = p[n][4][1];
        int foury = p[n][4][2];
		
		if (board[onex][oney]=='X' || board[twox][twoy]=='X' || board[threex][threey]=='X' || board[fourx][foury]=='X')
			continue;
		if (board[onex][oney]=='O') { countofplayer2++; }
		if (board[twox][twoy]=='O') { countofplayer2++; }
		if (board[threex][threey]=='O') { countofplayer2++; }
		if (board[fourx][foury]=='O' && countofplayer2 <= 3) { countofplayer2++; }

		if (countofplayer1 == 3) { fiveO++; }
		if (countofplayer1 == 2) { twoO++;  }
		if (countofplayer1 == 1) { oneO++;  }
	}
	
	// Maybe I'm still doing it wrong but this is the only way that I could make sense of it 
	// And it's consistent with the examples that ravi gives. 
	return ( ( 5 * fiveX + 2 * twoX + 1 * oneX ) - ( 5 * fiveO + 2 * twoO + 1 * oneO) );	
}

// Gets the best move of the starting board
void TicTacToe::bestmove() {
	// Set the variables
	int max = INT_MIN;
	std::vector<std::vector<std::vector<char>>> children = successor(_board, max_node(_board));
	std::vector<std::vector<char>> best_child;
	// Look through all the children and find best one
	for (std::vector<std::vector<char>> c: children) {
		int possible_max = Eval(c);
		if (possible_max > max) 
			max = possible_max;
			best_child = c;
	}
	// Set the position to the pointer
	for (int x = 1; x < 5; x++) { 
		for (int y = 1; y < 5; y++) {
			if (best_child[x][y] != _board[x][y]) {
				pbm[0] = x;
				pbm[1] = y;
			}
		}
	}
}

// Prints out the best move of the starting board
void TicTacToe::print_best_move() {
	std::cout << pbm[0] << " " << pbm[1];
}
