#include "MinHeap.hpp"

MinHeap::MinHeap(int c, int tc) : capacity{c}, totalcapacity{tc} {}

void MinHeap::insertKey(std::vector<int> perm) {
	int child = capacity - 1;
	int p;
	p = parent(child);
	breakheap.push_back( breakpoints(perm) );
	vectorheap.push_back( perm );
	while (child <= 0 && breakheap[p] > breakheap[child]) {
		swap(child, p);
	}
	capacity++;	
}

std::vector<int> MinHeap::deleteMinKey() {
	std::vector<int> empty = {};
	if (capacity == 0) 
		return empty;
	std::vector<int> root = vectorheap[0];
	if (capacity > 1) {
		vectorheap[0] = vectorheap[capacity-1];
		breakheap[0]  = breakheap[capacity-1];
		capacity--;
		heapify(0);
	}
	capacity--;
	return root;
}

void MinHeap::heapify(int i) {
	int l = left(i);
	int r = right(i);
	int s = i;
	if (l < capacity && breakheap[l] < breakheap[i]) 
		s = l;
	if (r < capacity && breakheap[r] < breakheap[i])
		s = r;
	if (s != i) {
		swap(s, i);
		heapify(s);
	}
}

int MinHeap::breakpoints(std::vector<int> &perm) {
	int bcount = 0;
	for (int i = 1; i < perm.size(); i++)
		if (abs(perm[i-1]-perm[i]) > 1)
			bcount++;
	return bcount;
}

void MinHeap::swap(int c, int p) {
	int breaktemp = breakheap[c];
	std::vector<int> vectortemp = vectorheap[c];
	breakheap[c]  = breakheap[p];
	breakheap[p]  = breaktemp;
	vectorheap[c] = vectorheap[p];
	vectorheap[p] = vectortemp;
}

int MinHeap::left(int i) {
	return (2*i + 1);
}

int MinHeap::right(int i) {
	return (2*i + 2);
}

int MinHeap::parent(int i) {
	return (i-1)/2;
}

bool MinHeap::empty() {
	if (capacity > 0) 
		return false;
	return true;
}
