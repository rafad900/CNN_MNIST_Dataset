#include <iostream>
#include<vector>
#include <fstream>
#include "TicTacToe.hpp"
#include <limits.h>
#include "time.h"
#define onunderline "\033[4m"
#define offunderline "\033[0m"

int main() {
    std::cout << " MY PROGRAM USES X, O, - or _  OPTIONS." << std::endl;

    while (true) {
        int option;
        std::cout << "Options : 1, 2, 3 (to quit): ";
        std::cin >> option;
        if (option == 1 || option ==2) {
            std::vector <std::vector<char>> board(5, std::vector<char>(5, '\0'));
            std::string fileName;
            std::cout << "File Name? ";
            std::cin >> fileName;


            std::ifstream inputStream;
            inputStream.open(fileName, std::ios::in);
            if (!inputStream.is_open()) {
                std::cout << "Unable to open " << fileName << ". Terminating...";
                perror("Error when attempting to open the input file.");
                exit(2);
            }


            char c;
            short row = 1, column = 1;
            short num_X = 0, num_O = 0;
            while (!inputStream.eof()) {
                while (inputStream.get(c) && isspace(c) && c != '\n');
                if (c == 'X' || c == 'x') {
                    board[row][column] = 'X';
                    column++;
                    num_X++;
                } else if (c == 'O' || c == 'o') {
                    board[row][column] = 'O';
                    column++;
                    num_O++;
                } else if (c == '\n') {
                    column = 1;
                    row++;
                } else if (c == '-' || c == '_') {
                    column++;
                } else {
                    std::cout << "Invalid character in input -->" << c << "<--" << std::endl;
                    exit(2);
                }

            }
            inputStream.close();
            for (int i = 1; i < 5; ++i) {
                for (int j = 1; j < 5; ++j) {
					if (board[i][j] == 'X' || board[i][j] == 'O')
 	                   	std::cout << onunderline << board[i][j] << offunderline;
					else 
						std::cout << onunderline << " " << offunderline;
                }
                std::cout << std::endl;
            }
            int nodes = 0;
			int nodes1 = 0;
			int nodes2 = 0;
            TicTacToe *game = new TicTacToe(board);
            game->bestmove();
            if (option == 1) {
                double start_time = clock();
                int point = game->minMax(board, nodes);
                double finish_time = clock();
                double time = ((finish_time - start_time) / CLOCKS_PER_SEC);
                std::cout << "\nMinimax Algorithm: " << std::endl;
                std::cout << "Root Node Value          : " << point << std::endl;
                std::cout << "Number of nodes expanded : " << nodes << std::endl;
                std::cout << "Best Move Found          : (";
                game->print_best_move();
                std::cout << ")" << std::endl;
                std::cout << "CPU time                 : " << time << " s" << std::endl;
                delete game;

            } else if (option == 2) {
                int depth;
                std::cout << "Depth? ";
                std::cin >> depth;
                nodes = 0;
                double start_time = clock();
                int pointAB = game->minMaxAB(board, depth, INT_MIN, INT_MAX, nodes, nodes1, nodes2);
                double finish_time = clock();
                double time = ((finish_time - start_time) / CLOCKS_PER_SEC);
                std::cout << "\nAlpha-Beta Pruning Algorithm: " << std::endl;
                std::cout << "Root Node Value          : " << pointAB << std::endl;
                std::cout << "Number of nodes expanded : " << nodes << std::endl;
				std::cout << "Nodes expanded by e1	 : " << nodes1 << std::endl;
				std::cout << "Nodes expanded by e2	 : " << nodes2 << std::endl;
                std::cout << "Best Move Found          : (";
                game->print_best_move();
                std::cout << ")" << std::endl;
                std::cout << "CPU time                 : " << time << " s" << std::endl;
                delete game;
            }
        }
        else if (option == 3) {
            exit(2);
        }
        else {
            std::cout << " Invalid option Choice" << std::endl;
            exit(2);
        }
    }
	return 0;
}
