#include <iostream>
#include<vector>
#include <fstream>
#include "TicTacToe.hpp"
#include <limits.h>
#include "time.h"


int main(int argc, char *argv[]) {
	std::vector< std::vector<char> > board (5, std::vector<char> (5,'\0')); 
	if (argc != 2) {
		std::cout << "usage: " << argv[0] << " nameOfAnInputFile\n";
		exit(1);
	}

	std::ifstream inputStream;
	inputStream.open(argv[1], std::ios::in);
	if (!inputStream.is_open()) {
		std::cout << "Unable to open " << argv[1] << ". Terminating...";
		perror("Error when attempting to open the input file.");
		exit(2);
	}

	char c;
	short row =1,column = 1;
	short num_X =0, num_O = 0;
	while ( !inputStream.eof()){
		while (inputStream.get(c) && isspace(c) && c != '\n')
			;
		if (c == 'X' || c == 'x'){
			//std::cout<< "X at :: ("<<row<<" , "<< column<<")"<< std::endl;
			board[row][column] = 'X';
			column++;
			num_X++;
		}
		else if( c == 'O' || c == 'o'){
			//std::cout<< " O at :: ("<<row<<" , "<< column<<")"<< std::endl;
			board[row][column] = 'O';
			column++;
			num_O++;
		}
		else if (c == '\n'){
			column =1;
			row++;
		}
		else if (c =='-' || c =='_'){
			column++;
		}
		else{
			std::cout<<"Invalid character in input -->"<< c <<"<--"<<std::endl;
			exit(2);
		}

	}
	for (int i = 0; i < 5; ++i)
	{
		for (int j = 0; j < 5; ++j)
		{
			std::cout<<board[i][j];
		}
		std::cout<<std::endl;
	}
	int nodes = 0;
	TicTacToe * game = new TicTacToe(board);
	game->bestmove();

	double start_time = clock();
	int point = game->minMax(board, nodes);
	double finish_time = clock();
 	double time = ((finish_time - start_time)/ CLOCKS_PER_SEC );
	std::cout << "\nMinimax Algorithm: "<< std::endl;
	std::cout << "Root Node Value          : "<< point <<std::endl;
	std::cout << "Number of nodes expanded : " << nodes  <<std::endl;
	std::cout << "Best Move Found          : (" ; game->print_best_move();  std::cout <<")"<<std::endl;
	std::cout << "CPU time                 : " << time<<" s" << std::endl;
	nodes = 0;

	start_time = clock();
	point = game->minMaxAB(board,5,INT_MIN,INT_MAX, nodes);
	finish_time = clock();
	time = ((finish_time - start_time)/ CLOCKS_PER_SEC );
	std::cout << "\n\nAlpha-Beta Pruning Algorithm: "<< std::endl;
	std::cout << "Root Node Value          : "<< point <<std::endl;
	std::cout << "Number of nodes expanded : " << nodes <<std::endl;
	std::cout << "Best Move Found          : ("; game->print_best_move();  std::cout <<")"<<std::endl;
	std::cout << "CPU time                 : " << time<< " s" << std::endl;

	return 0;
}
