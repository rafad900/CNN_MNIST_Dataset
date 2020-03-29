#include <string>

class TicTacToe{
public:
    TicTacToe(std::vector<std::vector<char>> board);
    bool leaf(std::vector<std::vector<char>> &current_board);
    bool max_node(std::vector<std::vector<char>> &current_board);
    int Eval (std::vector<std::vector<char>> &current_board);
    std::vector<std::vector<std::vector<char>>> successor(std::vector<std::vector<char>> &current_board, bool turn);
    int minMax(std::vector<std::vector<char>>& board, int &nodes);
    void count(std::vector<std::vector<char>> &curr_board, int &countX , int &countO);

	// THIS IS THE STUFF I ADDED ***************************************/
	int minMaxAB(std::vector< std::vector<char> > &board, int depth, int A, int B , int & nodes, int &nodeAB, int &nodeMM);
	void positionGenerator();
	int evalOne (std::vector< std::vector<char> > board);
	int evalTwo (std::vector< std::vector<char> > board);
	void bestmove ();
	void print_best_move();



private:
	int best_move[2];
	int (*pbm) = best_move;
	int p [24][5][3];
    std::vector<std::vector<char>> _board;
};
