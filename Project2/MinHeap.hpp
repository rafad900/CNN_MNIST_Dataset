#ifndef MINHEAP
#define MINHEAP
#include <vector> 
#include <iostream> 

class MinHeap {
	public:
		MinHeap(int c);
		void insertKey(std::vector<int> perm, int w);
		std::vector<int> deleteMinKey();
		int left(int i);
		int right(int i);
		int parent(int i);
		bool empty();
		void print();
		void printperm(std::vector<int> &perm);
		double  breakpoints(std::vector<int> &perm);
		int getmax_size(){ return max_size;}

	private:
		int max_size=0;
		int capacity;
		std::vector< std::vector<int> > vectorheap;
		std::vector<double> breakheap;
		void heapify(int i);
		void swap(int c, int p);

};

#endif
