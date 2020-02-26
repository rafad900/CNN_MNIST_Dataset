#ifndef SWAPSORTER
#define SWAPSORTER
#include <vector> 
#include <iostream>

class SwapSorter {
	public:
		//void BFSsort();
		//void IDSsort();

		std::vector<int> swap_section(std::vector<int> perm, int l, int r);
		SwapSorter(std::vector<int> user_input);
		void print(std::vector<int> perms);
		void paths();
		bool sort();

	private:
		bool is_goal(std::vector<int> perm);
		std::vector< std::vector<int> > get_neighbors( std::vector<int> parent);
		std::vector<int> numbers;
		std::vector<int> sorted_numbers;
		std::vector< std::vector<int> > swaps;
		std::vector<int> parent;
		std::vector<bool> visited;
		std::vector<int> distance;
		std::vector<int> path;
		int accumulator = 0;

		/* Things we were using the previous project. 
		 * They are not implemented in the cpp file
		 * just in case you were wondering			*/
		//bool IDS(std::vector<int> perm, int &count);
		//bool BFS(std::vector<int> perm, int& max_size, int &count);
		//bool DFS(std::vector<int> perm, int depth, int &count);
};

#endif
