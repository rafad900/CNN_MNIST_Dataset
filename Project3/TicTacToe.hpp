class TicTacToe{
public:
    TicTacToe(std::vector<std::vector<char>> board);
    bool leaf(std::vector<std::vector<char>> current_board);
    bool max_node(std::vector<std::vector<char>> current_board);
    int Eval (std::vector<std::vector<char>> current_board);
    std::vector<std::vector<std::vector<char>>> successor(std::vector<std::vector<char>> current_board, bool turn);
    int minMax(std::vector<std::vector<char>> board);
    int count(std::vector<std::vector<char>> curr_board, char X_or_O);

	// THIS IS THE STUFF I ADDED ***************************************/
	int minMaxAB(std::vector< std::vector<char> > board, int depth, int A, int B );
	void positionGenerator();
	int evalOne (std::vector< std::vector<char> > board);
	int evalTwo (std::vector< std::vector<char> > board);



private:
	int p [24][4][2];
    std::vector<std::vector<char>> _board;
};
