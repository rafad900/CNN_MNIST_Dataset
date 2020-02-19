.SUFFIXES: .o .cpp .out

FLAGS=-std=c++17 -ggdb

objects=main.o SwapSorter.o MinHeap.o

A.out: $(objects) 
	g++ $(FLAGS) -o A.out $(objects)

.cpp.o: 
	g++ $(FLAGS) -c $< -o $@

main.o: main.cpp

SwapSorter.o: SwapSorter.cpp SwapSorter.hpp

MinHeap.o: MinHeap.cpp MinHeap.hpp

clean:
	rm -fr *.o *~ *.out
