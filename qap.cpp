// permutacja.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <cstdlib>
#include <time.h>
#include <iostream>
#include <utility>

using namespace std;

void awesome_algorithm() {
	//TODO
}

void awesome_shuffle(int *vec, int n) {
	for (; n > 1; n--) 
		swap(vec[n - 1], vec[rand() % n]);
}

int main()
{
	srand(time(NULL));
	int tab[8], licznik=0;
	for (int i = 0; i < 8; i++)
		tab[i] = i + 1;
	awesome_shuffle(tab, 8);

	clock_t time0 = clock();
	do {
		awesome_algorithm();
		licznik++;
	} while ((double)(clock() - time0) / CLOCKS_PER_SEC < 100
		&& licznik < 10);

	getchar();
    return 0;
}

