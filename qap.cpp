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

int awesome_swap_score_diff(int **A, int **B, int n, int *assignment, int poss1, int poss2) {
	int score_diff = 0;
	for (int i = 0; i < n; i++) {
		if (i == poss1 || i == poss2) {
			continue;
		}
		score_diff -= A[i][poss2] * B[assignment[i]][assignment[poss2]];
		score_diff -= A[poss1][i] * B[assignment[poss1]][assignment[i]];

		score_diff += A[i][poss1] * B[assignment[i]][assignment[poss2]];
		score_diff += A[poss2][i] * B[assignment[poss1]][assignment[i]];

	}
	score_diff -= A[poss1][poss2] * B[assignment[poss1]][assignment[poss2]];
	score_diff += A[poss2][poss1] * B[assignment[poss1]][assignment[poss2]];
	return score_diff*2;
}

void _test_swap_score(int **A, int **B, int n, int *assignment) {
	int a = rand() % n;
	int b = rand() % n;
	awesome_shuffle(assignment, n);
	int score = awesome_score(A, B, n, assignment);
	cout << "Score before swap " << score << endl;
	int score_diff = awesome_swap_score_diff(A, B, n, assignment, a, b);
	swap(assignment[a], assignment[b]);
	int new_score = awesome_score(A, B, n, assignment);
	cout << "Score after swapping " << a << " and " << b << " : " << new_score << endl;
	cout << "Score diffrence " << new_score-score << " vs " << score_diff << endl << endl;
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
	file.open("../instancje/chr12a.dat");
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
		//awesome_algorithm(A, B, n, assignment);
		_test_swap_score(A, B, n, assignment);
		licznik++;
	} while ((double)(clock() - time0) / CLOCKS_PER_SEC < 1
		|| licznik < 10); 


	for (int i = 0; i < n; i++) {
		delete[] A[i];
		delete[] B[i];
	}
	delete[] A;
	delete[] B;

	getchar();
	return 0;
}

