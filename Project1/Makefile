.SUFFIXES: .o .cpp .out

objects=main.o SwapSorter.o 

FLAGS=-std=c++17 -ggdb

m.out: $(objects) 
	g++ $(FLAGS) -o m.out $(objects)

.cpp.o: 
	g++ $(FLAGS) -c $< -o $@

main.o: main.cpp

SwapSorter.o: SwapSorter.cpp SwapSorter.hpp

clean:
	rm -fr *.o *~ *.out
