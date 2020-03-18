#include <vector>
#include <math.h>
#include "minMax.hpp"



TicTacToe(std::vector<std::vector<char>> board, short X , short O) {}
bool leaf(std::vector<std::vector<char>> current_board) {
    return true;
}

bool max_node(std::vector<std::vector<char>> current_board){
	return true;
}
double Eval (std::vector<std::vector<char>> current_board){

}

std::vector<std::vector<std::vector<char>>> successor(std::vector<std::vector<char>> current_board){

}



double minMax(std::vector<std::vector<char>> board){
    double value;
    if (leaf(board)) return Eval(board);

    if (max_node(board))
        value = -INFINITY;
    else
        value = INFINITY;

    std::vector<std::vector<std::vector<char>>> neighbors = successor(board);
    for (std::vector<std::vector<char>> n : neighbors){
        if (max_node(board))
            value = std::max(value, minMax(n));
        else
            value = std::min(value, minMax(n));
    }
    return false;
}
