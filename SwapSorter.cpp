#include "SwapSorter.hpp"

SwapSorter::SwapSorter(std::vector<int> user_input) {
	numbers = user_input;
}
std::vector<int> SwapSorter::sort() {
	for (int i = 0; i < numbers.size(); i++) {
		std::cout << numbers[i] << " ";
	}
	return numbers;
}
