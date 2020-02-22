.SUFFIXES: .o .cpp .out

FLAGS=-std=c++17 -ggdb

objects=SwapSorter.o MinHeap.o

A.out: $(objects) main.o
	g++ $(FLAGS) -o A.out main.o $(objects)

test.out: $(objects) test.o
	g++ $(FLAGS) -o test.out test.o $(objects)

.cpp.o: 
	g++ $(FLAGS) -c $< -o $@

main.o: main.cpp

test.o: test.cpp

SwapSorter.o: SwapSorter.cpp SwapSorter.hpp

MinHeap.o: MinHeap.cpp MinHeap.hpp

clean:
	rm -fr *.o *~ *.out
