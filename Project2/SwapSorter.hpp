#ifndef SWAPSORTER
#define SWAPSORTER
#include <vector> 
#include <iostream>

class SwapSorter {
	public:
		void BFSsort();
		void IDSsort();
		std::vector<int> swap_section(std::vector<int> perm, int l, int r);
		SwapSorter(std::vector<int> user_input);
		void print(std::vector<int> perms);

	private:
		bool BFS(std::vector<int> perm, int& max_size, int &count);
		bool IDS(std::vector<int> perm, int &count);
		bool is_goal(std::vector<int> perm);
		std::vector< std::vector<int> > get_neighbors( std::vector<int> parent);
		bool DFS(std::vector<int> perm, int depth, int &count);
		std::vector<int> numbers;
		std::vector<int> sorted_numbers;
		std::vector< std::vector<int> > swaps;
		std::vector<bool> visited;
		std::vector<int> parent;
		std::vector<int> path;
};

#endif
