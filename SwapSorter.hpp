#ifndef SWAPSORTER
#define SWAPSORTER
#include <vector> 
#include <iostream> 

class SwapSorter {
	public:
		std::vector<int> sort();
		std::vector<int> swap_section(int l, int r);
		SwapSorter(std::vector<int> user_input);
		void print();
		
	private:
		std::vector<int> numbers;
		std::vector< std::vector<int> > swaps;
		std::vector<bool> visited;
};
#endif
