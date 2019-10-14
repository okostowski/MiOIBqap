// permutacja.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <cstdlib>
#include <time.h>
#include <iostream>
#include <utility>

using namespace std;


void random_permute(int *vec, int n) {
	for (; n > 1; n--) 
		swap(vec[n - 1], vec[rand() % n]);
}

int main()
{
	srand(time(NULL));
	int tab[8];
	for (int i = 0; i < 8; i++)
		tab[i] = i + 1;
	random_permute(tab, 8);
	for (int i = 0; i < 8; i++)
		cout << tab[i] << " ";
	getchar();
    return 0;
}

