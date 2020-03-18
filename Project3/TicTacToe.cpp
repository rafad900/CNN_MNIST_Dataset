#include <vector>
#include <math.h>
#include "TicTacToe.hpp"
#include <iostream>
#include <limits.h>


TicTacToe::TicTacToe(std::vector<std::vector<char>> board): _board{board}  {}

int TicTacToe::count(std::vector<std::vector<char>> curr_board, char X_or_O){
    int xCount = 0, oCount =0;
    for (int x = 0; x < curr_board.size(); x++)
        for (int y = 0; y < curr_board[x].size(); y++)
            if (curr_board[x][y] == 'X')
                xCount++;
            else if( curr_board[x][y] == 'O')
                oCount++;
    if (X_or_O == 'X')
        return xCount;
    else
        return oCount;

}

int checkWinner(std::vector<std::vector<char>> curr_board) {
    bool Xrow1 = 0, Xrow2 = 0, Xrow3 = 0, Xrow4 = 0;
    bool Orow1 = 0, Orow2 = 0, Orow3 = 0, Orow4 = 0;
    bool Xcol1 = 0, Xcol2 = 0, Xcol3 = 0, Xcol4 = 0;
    bool Ocol1 = 0, Ocol2 = 0, Ocol3 = 0, Ocol4 = 0;

    if (curr_board[1][1] == 'X' || curr_board[1][2] == 'X' || curr_board[1][3] == 'X' || curr_board[1][4] == 'X')
        Xrow1 = 1;
    if (curr_board[2][1] == 'X' || curr_board[2][2] == 'X' || curr_board[2][3] == 'X' || curr_board[2][4] == 'X')
        Xrow2 = 1;
    if (curr_board[3][1] == 'X' || curr_board[3][2] == 'X' || curr_board[3][3] == 'X' || curr_board[3][4] == 'X')
        Xrow3 = 1;
    if (curr_board[4][1] == 'X' || curr_board[4][2] == 'X' || curr_board[4][3] == 'X' || curr_board[4][4] == 'X')
        Xrow4 = 1;

    if (curr_board[1][1] == 'X' || curr_board[2][1] == 'X' || curr_board[3][1] == 'X' || curr_board[4][1] == 'X')
        Xcol1 = 1;
    if (curr_board[1][2] == 'X' || curr_board[2][2] == 'X' || curr_board[3][2] == 'X' || curr_board[4][2] == 'X')
        Xcol2 = 1;
    if (curr_board[1][3] == 'X' || curr_board[2][3] == 'X' || curr_board[3][3] == 'X' || curr_board[4][3] == 'X')
        Xcol3 = 1;
    if (curr_board[1][4] == 'X' || curr_board[2][4] == 'X' || curr_board[3][4] == 'X' || curr_board[4][4] == 'X')
        Xcol4 = 1;


    if (curr_board[1][1] == 'O' || curr_board[1][2] == 'O' || curr_board[1][3] == 'O' || curr_board[1][4] == 'O')
        Orow1 = 1;
    if (curr_board[2][1] == 'O' || curr_board[2][2] == 'O' || curr_board[2][3] == 'O' || curr_board[2][4] == 'O')
        Orow2 = 1;
    if (curr_board[3][1] == 'O' || curr_board[3][2] == 'O' || curr_board[3][3] == 'O' || curr_board[3][4] == 'O')
        Orow3 = 1;
    if (curr_board[4][1] == 'O' || curr_board[4][2] == 'O' || curr_board[4][3] == 'O' || curr_board[4][4] == 'O')
        Orow4 = 1;

    if (curr_board[1][1] == 'O' || curr_board[2][1] == 'O' || curr_board[3][1] == 'O' || curr_board[4][1] == 'O')
        Ocol1 = 1;
    if (curr_board[1][2] == 'O' || curr_board[2][2] == 'O' || curr_board[3][2] == 'O' || curr_board[4][2] == 'O')
        Ocol2 = 1;
    if (curr_board[1][3] == 'O' || curr_board[2][3] == 'O' || curr_board[3][3] == 'O' || curr_board[4][3] == 'O')
        Ocol3 = 1;
    if (curr_board[1][4] == 'O' || curr_board[2][4] == 'O' || curr_board[3][4] == 'O' || curr_board[4][4] == 'O')
        Ocol4 = 1;

// 1 --> X wins
// -1 --> O wins
// 0 --> draw
    if (Xcol1 && Xcol2 && Xcol3 && Xcol4 && Xrow1 && Xrow2 && Xrow3 && Xrow4)
        return 10;
    else if (Ocol1 && Ocol2 && Ocol3 && Ocol4 && Orow1 && Orow2 && Orow3 && Orow4)
        return -10;
    else
        return 0;
}
bool TicTacToe::leaf(std::vector<std::vector<char>> curr_board) {
    if ( count(curr_board, 'X') == 8 &&  count(curr_board,'O') == 8 )
        return true;
    else if( checkWinner(curr_board) != 0)
		return true;

	return false;
}

bool TicTacToe::max_node(std::vector<std::vector<char>> current_board){
    if ( count(current_board, 'X') <= count(current_board,'O'))
		return true;
	return false;
}

int TicTacToe::Eval (std::vector<std::vector<char>> curr_board){
    return checkWinner(curr_board);
}


std::vector<std::vector<std::vector<char>>> TicTacToe::successor(std::vector<std::vector<char>> current_board, bool turn){
	std::vector<std::vector<std::vector<char>>> children;
	std::vector<std::vector<char>> newBoard  = current_board;
	int totalSpots = 16 - (count(current_board, 'X') + count(current_board,'O'));
	if (turn){
		while ( totalSpots != 0){
			for (int i = 1 ; i < 5; i++){
				for (int j =1 ; j < 5; j++){
					if (newBoard[i][j] == '\0'){
						newBoard[i][j] = 'X';
						totalSpots--;
						children.push_back(newBoard);
                        newBoard[i][j] = '\0';
					}
				}
			}
		}
	}
	else{
		while ( totalSpots != 0){
			for (int i = 1 ; i < 5; i++){
				for (int j =1 ; j < 5; j++){
					if (newBoard[i][j] == '\0'){
						newBoard[i][j] = 'O';
						totalSpots--;
						children.push_back(newBoard);
                        newBoard[i][j] = '\0';
					}
				}
			}
		}
	}
	return children;
}



int TicTacToe::minMax(std::vector<std::vector<char>> board){
	int value;
	bool max_turn = false;
    if ( std::abs(count(board, 'X') - count(board,'O')) > 1) {
        std::cout<< "Invalid Board" << std::endl;
        return -1;
    }
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
            value = std::max(value, minMax(n));
        }
		else {
            value = std::min(value, minMax(n));
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
	for (int i = 0; i < 4; i++) {
		p[num][0][0] = 0;
		p[num][0][1] = i;
		for (int j = 0; j < 4; j++) {
			if (j != i) {
				p[num][1][0] = 1;
				p[num][1][1] = j;
				for (int k = 0; k < 4; k++) {
					if (k != i && k != j) {
						p[num][2][0] = 2;
						p[num][2][1] = k;
						for (int l = 0; l < 4; l++) {
							if (l != i && l != j && l != k) {
								p[num][3][0] = 3;
								p[num][3][1] = l;
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
int TicTacToe::minMaxAB(std::vector< std::vector<char> > board, int depth, int A, int B) {
	if (depth == 0 || leaf(board)) return Eval(board);
	int res;
	if (max_node(board)) {
		res = A;
		std::vector< std::vector< std::vector<char> > > successors = successor(board, true);
		for (std::vector< std::vector<char> > c: successors) {
			int val = minMaxAB(c, depth-1, res, B);
			int maxVal = std::max(res, A);
			if (res >= B)
				return res;
		}
	} else {
		res = B;
		std::vector< std::vector< std::vector<char> > > successors = successor(board, true);
		for (std::vector< std::vector<char> > c: successors) {
			int val = minMaxAB(board, depth-1, A, res);
			int res = std::min(res, val);
			if (res >= A) 
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
		int onex = p[n][0][0];
		int oney = p[n][0][1];
		int twox = p[n][1][0];
		int twoy = p[n][1][1];
		int threex = p[n][2][0];
		int threey = p[n][2][1];
		int fourx = p[n][3][0];
		int foury = p[n][3][1];

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
		int onex = p[n][0][0];
		int oney = p[n][0][1];
		int twox = p[n][1][0];
		int twoy = p[n][1][1];
		int threex = p[n][2][0];
		int threey = p[n][2][1];
		int fourx = p[n][3][0];
		int foury = p[n][3][1];
		
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
		int onex = p[n][0][0];
		int oney = p[n][0][1];
		int twox = p[n][1][0];
		int twoy = p[n][1][1];
		int threex = p[n][2][0];
		int threey = p[n][2][1];
		int fourx = p[n][3][0];
		int foury = p[n][3][1];
		
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
