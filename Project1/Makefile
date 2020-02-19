.SUFFIXES: .o .cpp .out

FLAGS=-std=c++17 -ggdb -I ./../Project1

objects=main.o SwapSorter.o 

m.out: $(objects) 
	g++ $(FLAGS) -o m.out $(objects)

.cpp.o: 
	g++ $(FLAGS) -c $< -o $@

main.o: main.cpp

SwapSorter.o: SwapSorter.cpp SwapSorter.hpp

clean:
	rm -fr *.o *~ *.out
