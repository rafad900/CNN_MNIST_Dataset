#include <algorithm>
#include "SwapSorter.hpp"
#include "permToInt.cpp"
#include <queue>
#include <stack>
#include "MinHeap.hpp"

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
		distance.push_back(0);
	}
}

void SwapSorter::paths(){
	int numOfmoves=0;
	int next_index = permToInt(sorted_numbers);
	while (parent[next_index] != -1) {
		numOfmoves++;
		path.push_back(next_index);
		next_index = parent[next_index];
	}
	std::cout<<"Number of moves to sort : "<< numOfmoves<<std::endl;
	print(path);
}
void SwapSorter::print(std::vector<int> perms) {							
	std::cout << "[ ";
	for (int i = 0; i < numbers.size(); i++) {
		std::cout << numbers[i] << " ";
    }
    std::cout << "]\n";
    for (int i = perms.size()-1; i >= 0; i--) {
	    std::vector<int> temp = intToPerm(perms[i], numbers.size());
        std::cout << "[ ";
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

std::vector< std::vector<int> > SwapSorter::get_neighbors( std::vector<int> parent) {
	std::vector< std::vector<int> > temp_neighbors;
	for (int a = 0; a < parent.size()-1; a++) {			// Should perform swaps from left to right
		for (int b = a+1; b < parent.size(); b++) {	// Should perform swaps from right to left
			temp_neighbors.push_back(swap_section(parent, a, b));
		}
	}
	return temp_neighbors;
}

bool SwapSorter::is_goal(std::vector<int> perm) { // THis quecks for the goal in IDS 
	return perm == sorted_numbers;
}

bool SwapSorter::sort() {
	std::fill(parent.begin(), parent.end(), -1);
	std::fill(visited.begin(), visited.end(), false);
	std::fill(distance.begin(),distance.end(),0);
	MinHeap *heap =  new MinHeap(0);
	heap->insertKey(numbers,0);
	while( !heap->empty() ) {
		std::vector<int> current = heap->deleteMinKey();
		int parentIndex = permToInt(current);
		visited[parentIndex] = true;
		if ( is_goal(current) ) { 
			std::cout<<"Max Size : " << heap->getmax_size()<<std::endl;
			return true; 
		}
		std::vector< std::vector<int> > neighbors = get_neighbors(current);
		for (std::vector<int> c : neighbors) {
			int index = permToInt(c);
			if (!visited[index] ){
				//visited[index] = true;     // REMOVING THIS WAS THE LAST PART, you already made it true on line 86 and I suppose doing this was messing with the search 
				if (parent[index] == -1) 
					parent[index] = parentIndex;
				else if (parent[index] <= parentIndex) 
					continue;
			}
			distance[index] = distance[parentIndex] +1 ;
			heap->insertKey(c,distance[index]);
		}
	}	
	return false;
}
