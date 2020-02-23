#include "SwapSorter.hpp"
#include <iostream> 
#include <vector>
#include <string>
#include "time.h"
#include <sstream>

int main() {
	std::vector<int> user_input;
	std::string input;
	std::cout << "Enter a list of numbers with space in between them: ";
	getline(std::cin, input);
	std::istringstream iss(input);
	int temp;
	while(iss >> temp)
	{
		user_input.push_back(temp);
	}
    double start_time = clock();
	SwapSorter *sorter = new SwapSorter(user_input);

	if (sorter->sort()){
	    sorter->paths();
	}
	else{
	    std::cout<< " Path not found."<<std::endl;
	}
    double finish_time = clock();
    double time = ((finish_time - start_time)/ CLOCKS_PER_SEC );
    std::cout<< "Time Taken by A*       : "<<time<<" sec"<<std::endl;
	delete sorter;

	std::cout << std::endl;
	return 0;
}

