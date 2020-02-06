#include "SwapSorter.hpp"
#include <iostream> 
#include <vector>
#include <string>
#include "time.h"

int main() {
	std::vector<int> user_input;
	std::vector<int> output;
	std::cout << "Give me a number: ";
	std::string input;

	while (getline(std::cin, input)) {
		if (input.empty()) {
			std::cout << "Sorting then\n\n";
			break;
		}
		user_input.push_back(std::stoi(input));
		std::cout << "Another number? ";
	}

	SwapSorter *sorter = new SwapSorter(user_input);
    double start_time = clock();
	sorter->BFSsort();
    double finish_time = clock();
    double time = ((finish_time - start_time)/ CLOCKS_PER_SEC );
    std::cout<< "Time Taken by BFS: "<<time<<" sec"<<std::endl;

    start_time = clock();
    sorter->BFSsort();
    finish_time = clock();
    time = ((finish_time - start_time)/ CLOCKS_PER_SEC );
    std::cout<< "Time Taken by IDS: "<<time<<" sec"<<std::endl;
	delete sorter;


	std::cout << std::endl;
	return 0;
}

