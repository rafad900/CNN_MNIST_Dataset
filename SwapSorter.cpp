#include "SwapSorter.hpp"

SwapSorter::SwapSorter(std::vector<int> user_input): numbers(user_input) {} //{ numbers = user_input; } Im using a initilizer list just if you wondering

void SwapSorter::print() {
	std::cout << "This is the original sequence: [";
	for (int i = 0; i < numbers.size(); i++) {
		std::cout << numbers[i] << " ";
	} 
	std::cout << "]\n These are the swaps: \n";
	for (int i = 0; i < swaps.size(); i++) {
		std::cout << "[";
		for (int j = 0; j < swaps[i].size(); j++) {
			std::cout << swaps[i][j] << " ";
		}
		std::cout << "]";
		std::cout << std::endl;
	}
}

std::vector<int> SwapSorter::swap_section(int l, int r) {
	std::vector<int> swapped_vector (numbers.size(), 0);
	for (int i = 0; i <  l; i++) {
		swapped_vector[i] = numbers[i];
	}
	for (int i = l; i <= r; i++) {
		swapped_vector[l+(r-i)] = numbers[i];
	}
	for (int i = r+1; i < numbers.size(); i++) {
		swapped_vector[i] = numbers[i];
	}
	return swapped_vector;
}

std::vector<int> SwapSorter::sort() {
	
	for (int a = 0; a < numbers.size(); a++) {
		for (int b = numbers.size()-1; b >= 0; b--) {
			swaps.push_back(swap_section(a, b));
		}
	}
	return numbers;
}
