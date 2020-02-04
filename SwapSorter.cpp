#include <algorithm>
#include "SwapSorter.hpp"
#include "permToInt.cpp"

SwapSorter::SwapSorter(std::vector<int> user_input): numbers(user_input) {
	sorted_numbers = numbers; 
	std::sort(sorted_numbers.begin(), sorted_numbers.end());
} //{ numbers = user_input; } Im using a initilizer list just if you wondering

void SwapSorter::print() {							// Just a random print function, mainly for debugging
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
		std::cout << "]\n";
	}
}
	
std::vector<int> SwapSorter::swap_section(std::vector<int> parent, int l, int r) {
	std::vector<int> swapped_vector (numbers.size(), 0);
	for (int i = 0; i <  l; i++) {					// To fill anything before the section to be swapped
		swapped_vector[i] = numbers[i];
	}
	for (int i = l; i <= r; i++) {
		swapped_vector[l+(r-i)] = numbers[i];		// This to swap the section
	}
	for (int i = r+1; i < numbers.size(); i++) {	// This to fill anything after the section
		swapped_vector[i] = numbers[i];
	}
	return swapped_vector;
}

std::vector<int> SwapSorter::sort() {
	std::vector<int> result = {0};
	return result;// This should call the bbbIDS and BFS 
}

std::vector< std::vector<int> > SwapSorter::get_neighbors( std::vector<int> parent) {
	std::vector< std::vector<int> > neighbors;
	for (int a = 0; a < parent.size(); a++) {			// Should perform swaps from left to right
		for (int b = parent.size()-1; b >= 0; b--) {	// Should perform swaps from right to left
			neighbors.push_back(swap_section(parent, a, b));
		}
	}
	return neighbors;
}

bool SwapSorter::is_goal(std::vector<int> perm) {
	return perm == sorted_numbers;
}

bool SwapSorter::DFS(std::vector<int> perm, int depth) {
	if (is_goal(perm)) 
		return true;
	if (depth == 0) 
		return false;
	std::vector< std::vector<int> > neighbors = get_neighbors(perm);
	for (std::vector<int> n: neighbors) {
		int index = permToInt(perm);
		if (!visited[index]) {
			visited[index] = true;
			return DFS(n, depth-1);
		}
	}
	return false;
}
