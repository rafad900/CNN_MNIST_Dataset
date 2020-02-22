#ifndef MINHEAP
#define MINHEAP
#include <vector> 
#include <iostream> 

class MinHeap {
	public:
		MinHeap(int c, int tc);
		void insertKey(std::vector<int> perm);
		std::vector<int> deleteMinKey();
		int left(int i);
		int right(int i);
		int parent(int i);
		bool empty();
		void print();

		
	private:
		int totalcapacity;
		int capacity;
		std::vector< std::vector<int> > vectorheap;
		std::vector<int> breakheap;
		void printperm(std::vector<int> &perm);
		void heapify(int i);
		void swap(int c, int p);
		int breakpoints(std::vector<int> &perm);

};

#endif
