class TicTacToe{
public:
    TicTacToe(std::vector<std::vector<char>> board, short X , short O);
    bool leaf(std::vector<std::vector<char>> current_board);
    bool max_node(std::vector<std::vector<char>> current_board);
    double Eval (std::vector<std::vector<char>> current_board);
    std::vector<std::vector<std::vector<char>>> successor(std::vector<std::vector<char>> current_board);
    double minMax(std::vector<std::vector<char>> board);

private:
    std::vector<std::vector<char>> board;
    short numbOfX;
    short numOfO;
};