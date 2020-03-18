.SUFFIXES: .o .cpp .out

FLAGS=-std=c++17 -ggdb

objects= TicTacToe.o

TicTacToe.out: $(objects) main.o
	g++ $(FLAGS) -o TicTacToe.out main.o $(objects)

T.out: $(objects) test.o
	g++ $(FLAGS) -o T.out test.o $(objects)

.cpp.o: 
	g++ $(FLAGS) -c $< -o $@

main.o: main.cpp TicTacToe.hpp

test.o: test.cpp

TicTacToe.o: TicTacToe.hpp TicTacToe.cpp

clean:
	rm -fr *.o *~ *.out
