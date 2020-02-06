#include <algorithm>
#include "SwapSorter.hpp"
#include "permToInt.cpp"
#include <queue>


SwapSorter::SwapSorter(std::vector<int> user_input): numbers(user_input) {
	sorted_numbers = numbers; 
	std::sort(sorted_numbers.begin(), sorted_numbers.end());
	int accumulator = 1;
	for (int i = 1; i <= numbers.size(); i++) {
		accumulator*= i;
	}
	for (int i = 0; i < accumulator; i++) {
		parent.push_back(-1);
		visited.push_back(false);
	}
}

void SwapSorter::print(std::vector<int> perms) {							
	std::cout << "This is the original sequence: [";
	for (int i = 0; i < numbers.size(); i++) {
		std::cout << numbers[i] << " ";
	} 
	std::cout << "]\n\nThis is the path to the sorted sequence\n";
	for (int i = perms.size()-1; i >= 0; i--) {
		std::vector<int> temp = intToPerm(perms[i], numbers.size());
		std::cout << "[";
		for (int j = 0; j < temp.size(); j++) {
			std::cout << temp[j] << " ";
		}
		std::cout << "]\n";
	}
}

std::vector<int> SwapSorter::swap_section(std::vector<int> parent_perm, int l, int r) {
	std::vector<int> swapped_vector (numbers.size(), 0);
	for (int i = 0; i <  l; i++) {					// To fill anything before the section to be swapped
		swapped_vector[i] = parent_perm[i];
	}
	for (int i = l; i <= r; i++) {
		swapped_vector[l+(r-i)] = parent_perm[i];		// This to swap the section
	}
	for (int i = r+1; i < numbers.size(); i++) {	// This to fill anything after the section
		swapped_vector[i] = parent_perm[i];
	}
	return swapped_vector;
}

void SwapSorter::IDSsort() {								// THIS IS THE FUNCTION THAT RUNS BEGINS THE SORTATION

	if (IDS(numbers)){
		int next_index = permToInt(sorted_numbers);
		while (parent[next_index] != -1) {
			path.push_back(next_index);
			next_index = parent[next_index];
		}
		print(path);
	}



}

void SwapSorter::BFSsort(){
	int max_size = 0;
	if (BFS(numbers, max_size)) {
		int next_index = permToInt(sorted_numbers);
		while (parent[next_index] != -1) {
			path.push_back(next_index);
			next_index = parent[next_index];
		}
		print(path);
		std::cout<<"Max queue size: "<<max_size<<std::endl;
	}
}

std::vector< std::vector<int> > SwapSorter::get_neighbors( std::vector<int> parent) {
	std::vector< std::vector<int> > temp_neighbors;
	for (int a = 0; a < parent.size(); a++) {			// Should perform swaps from left to right
		for (int b = a+1; b < parent.size(); b++) {	// Should perform swaps from right to left
			temp_neighbors.push_back(swap_section(parent, a, b));
		}
	}
	return temp_neighbors;
}

bool SwapSorter::is_goal(std::vector<int> perm) { // THis quecks for the goal in IDS 
	/*std::cout << "This is the permutation: [";											/// This section prints out the swaps that are being compared to the sorted one
	  for (int i = 0; i < perm.size(); i++) {
	  std::cout << perm[i] << " ";
	  } 
	  std::cout << "] and this is the sorted [";
	  for (int i = 0; i < perm.size(); i++) {
	  std::cout << sorted_numbers[i] << " ";
	  } 
	  std::cout << "] and this is what they return: " << (perm == sorted_numbers) << "\n";
	  */
	return perm == sorted_numbers;
}

bool SwapSorter::DFS(std::vector<int> perm, int depth) {
	if (is_goal(perm)) {
		return true;
	}
	if (depth == 0) 
		return false;
	std::vector< std::vector<int> > neighbors = get_neighbors(perm);
	int parentIndex = permToInt(perm);
	visited[parentIndex] = true;
	for (std::vector<int> n: neighbors) {
		int childIndex = permToInt(n);
		if (!visited[childIndex]) {
			visited[childIndex] = true;
			parent[childIndex] = parentIndex;
			return DFS(n, depth-1);
		}
	}
	return false;
}

bool SwapSorter::IDS(std::vector<int> perm) {
	if (is_goal(perm)) {
		return true;
	}
	int depth = 1;
	
	while (!DFS(perm, depth)) {	
		//std::fill(visited.begin(), visited.end(), 0);// Reset both the parent and the visited vectors for the next iteration of DFS	
		//std::fill(parent.begin(), parent.end(), -1);
		depth++;
	}
	return true;
}


bool  SwapSorter::BFS (std::vector<int> perm, int &max_size){
	if (is_goal(perm)) return true;
	queue<vector<int>> Q;
	std::fill(visited.begin(), visited.end(), 0);
	std::fill(parent.begin(), parent.end(), -1);
	Q.push(perm);
	int index = permToInt(perm);
	visited[index] = true;
	std::vector<int> current;
	while (!Q.empty()){
		current = Q.front();
		int curr_size =Q.size();
		max_size = std::max(max_size, curr_size);
		
		Q.pop();
		int parentIndex = permToInt(current);
		if (is_goal(current)) return true;
		std::vector< std::vector<int> > neighbors = get_neighbors(current);
		for (std::vector<int> n: neighbors) {
			index = permToInt(n);
			if(!visited[index]){
				visited[index] =true;
				parent[index]= parentIndex;
				Q.push(n);
			}
		}
	}
	return false;

}
