// permutacja.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <cstdlib>
#include <time.h>
#include <iostream>
#include <utility>
#include <fstream>

using namespace std;

void awesome_shuffle(int *vec, int n) {
	for (; n > 1; n--) 
		swap(vec[n - 1], vec[rand() % n]);
}

int awesome_score(int **A, int **B, int n, int *assignment) {
	int score = 0;
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			score += A[i][j] * B[assignment[i]][assignment[j]];
		}
	}
	return score;
}

void awesome_algorithm(int **A, int **B, int n, int *assignment) {
	//TODO
	awesome_shuffle(assignment, n);
	int score = awesome_score(A, B, n, assignment);
	cout << score << endl;
}

int main()
{
	ifstream file;
	file.open("instancje/chr12a.dat");
	int n;
	file >> n;
	int **A = new int*[n];
	int **B = new int*[n];
	for (int i = 0; i < n; i++) {
		A[i] = new int[n];
		B[i] = new int[n];
	}
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			file >> A[i][j];
		}
	}
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			file >> B[i][j];
		}
	}
	file.close();

	srand(time(NULL));
	int licznik = 0;
	int *assignment = new int[n];
	for (int i = 0; i < n; i++)
		assignment[i] = i;
	awesome_shuffle(assignment, n);

	clock_t time0 = clock();
	do {
		awesome_algorithm(A, B, n, assignment);
		licznik++;
	} while ((double)(clock() - time0) / CLOCKS_PER_SEC < 100
		&& licznik < 10);

	int tab[12] = { 6,  4, 11,  1,  0,  2,  8, 10, 9,  5,  7,  3 };
	int score = awesome_score(A, B, n, tab);
	cout << "Test: " << score;


	for (int i = 0; i < n; i++) {
		delete[] A[i];
		delete[] B[i];
	}
	delete[] A;
	delete[] B;

	getchar();
    return 0;
}

