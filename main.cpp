#include "SwapSorter.hpp"
#include <iostream> 
#include <vector>
#include <string>

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
	output = sorter->sort();
	sorter->print();
	delete sorter;
	std::cout << std::endl;
	return 0;
}

