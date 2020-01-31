#ifndef SWAPSORTER
#define SWAPSORTER
#include <vector> 
#include <iostream> 

class SwapSorter {
	public:
		std::vector<int> sort();
		SwapSorter(std::vector<int> user_input);
		
	private:
		std::vector<int> numbers;
};
#endif
