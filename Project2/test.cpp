#include "MinHeap.hpp"
#include <vector> 
#include "SwapSorter.hpp"

int main() {
	MinHeap * h = new MinHeap(0, 50);
	std::vector<int> fst = {1, 2, 3, 4, 5};
	SwapSorter *sw = new SwapSorter(fst);
	std::vector< std::vector<int> > c = sw->get_neighbors( fst );
	

	for (std::vector<int> ci : c) {
		sw->print(ci);
		h->insertKey(ci, 0);
		h->print();
		std::cout << std::endl;
	}
	std::cout << "---------------------" << std::endl;
	std::vector<int> t;
	while (!h->empty()) {
		t = h->deleteMinKey();
		sw->print(t);
		h->print();
		std::cout << std::endl;
	}
	return 0;
}
