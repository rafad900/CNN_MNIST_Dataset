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
