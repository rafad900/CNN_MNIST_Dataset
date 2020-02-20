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

	SwapSorter *sorter = new SwapSorter(user_input);
	std::cout<<"Start BFS:"<<std::endl;
	double start_time = clock();
	sorter->BFSsort();
	double finish_time = clock();
	double time = ((finish_time - start_time)/ CLOCKS_PER_SEC );
	std::cout<< "Time Taken by BFS       : "<<time<<" sec"<<std::endl;
	delete sorter;

	SwapSorter *sorter_ = new SwapSorter(user_input);
	std::cout<<"\nStart IDS:"<<std::endl;
	start_time = clock();
	sorter_->IDSsort();
	finish_time = clock();
	time = ((finish_time - start_time)/ CLOCKS_PER_SEC );
	std::cout<< "Time Taken by IDS       : "<<time<<" sec"<<std::endl;
	delete sorter_;


	std::cout << std::endl;
	return 0;
}

