#include "MinHeap.hpp"
#include <vector> 

int main() {
	MinHeap * h = new MinHeap(0, 50);
	std::vector<int> fst = {1, 2, 3, 4, 5};
	h->insertKey(fst);
	h->print();
	return 0;
}
