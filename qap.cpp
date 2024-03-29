// permutacja.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <cstdlib>
#include <time.h>
#include <iostream>
#include <utility>
#include <fstream>
#include <vector>
#include <algorithm>

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
	return score_diff * 2;
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
	cout << "Score diffrence " << new_score - score << " vs " << score_diff << endl << endl;
}

void awesome_algorithm(int **A, int **B, int n, int *assignment) {
	//TODO
	awesome_shuffle(assignment, n);
	int score = awesome_score(A, B, n, assignment);
	cout << score << endl;
}


void alg_random(int **A, int **B, int n, int* assignment, int* assignment_best_random, double nseconds = 1) {


	clock_t time0 = clock();
	int max_score = awesome_score(A, B, n, assignment);
	//cout << max_score << endl;
	do {
		awesome_shuffle(assignment, n);
		int score = awesome_score(A, B, n, assignment);
		if (score < max_score) {
			max_score = score;
			for (int i = 0; i < n; i++) {
				assignment_best_random[i] = assignment[i];
			}
		}
	} while ((double)(clock() - time0) / CLOCKS_PER_SEC < nseconds);

	//cout << max_score << endl;
	//return score; we should return struct with all necessary information: score, number of iteration etc - check what we will need
}

int alg_steepest(int **A, int **B, int n, int* assignment) {

	int steps = 0;

	//int max_score = awesome_score(A, B, n, assignment);
	int min_score_diff;
	while (true) {
		int a, b;
		min_score_diff = 0;
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++) {
				int score_diff = awesome_swap_score_diff(A, B, n, assignment, i, j);
				if (score_diff < min_score_diff) {
					min_score_diff = score_diff;
					a = i; b = j;
					//cout << "   " << min_score_diff << endl;
				}
			}
		}
		steps++;
		if (min_score_diff >= 0) break;

		//cout << awesome_score(A, B, n, assignment) << endl; //calculating score is only neccesssary once after finding the best solution
		swap(assignment[a], assignment[b]);
		//cout << awesome_score(A, B, n, assignment) << endl;
	}
	return steps;
	//return score; we should return struct with all necessary information: score, number of iteration etc - check what we will need
}

int alg_greedy(int **A, int **B, int n, int* assignment) {
	//cout << awesome_score(A, B, n, assignment) << endl;
	int steps = 0;

	while (true) {
		int a, b;
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++) {
				int score_diff = awesome_swap_score_diff(A, B, n, assignment, i, j);
				if (score_diff < 0) {
					swap(assignment[i], assignment[j]);
					//cout << "   " << score_diff << endl;
					goto alg_greedy_better_loop_exit; //Czy to naprawdę było konieczne? Trochę przykro mi się zrobiło :/
				}
			}
		}
		break; //if the loop didnt reach goto statement then exit

	alg_greedy_better_loop_exit:
		//cout << awesome_score(A, B, n, assignment) << endl;
		steps++;
	}
	return steps;
	//return score; we should return struct with all necessary information: score, number of iteration etc - check what we will need
}

bool sortbysec(const pair<int, int> &a,
	const pair<int, int> &b)
{
	return (a.second < b.second);
}

bool sortbysec_rev(const pair<int, int> &a,
	const pair<int, int> &b)
{
	return (a.second > b.second);
}

int alg_heuristic(int **A, int **B, int n, int* assignment) {
	//cout << awesome_score(A, B, n, assignment) << endl;
	int steps = 0;
	vector< pair<int, int> > importance_rooms;
	vector< pair<int, int> > importance_doctors;

	for (int i = 0; i < n; i++) {
		importance_rooms.push_back(make_pair(i, 0));
		importance_doctors.push_back(make_pair(i, 0));
	}

	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			importance_doctors[i].second += A[i][j];
			importance_doctors[j].second += A[i][j];
			importance_rooms[i].second += B[i][j];
			importance_rooms[j].second += B[i][j];
		}
		//cout << importance_doctors[i].second << ";" << importance_rooms[i].second << " ";
	}

	sort(importance_rooms.begin(), importance_rooms.end(), sortbysec);
	sort(importance_doctors.begin(), importance_doctors.end(), sortbysec_rev);

	for (int i = 0; i < n; i++) {
		assignment[importance_rooms[i].first] = importance_doctors[i].first;
	}

	int example = awesome_score(A, B, n, assignment);

	return 0;
	//return score; we should return struct with all necessary information: score, number of iteration etc - check what we will need
}

void reroll_solution(int n, int* assignment) {
	for (int i = 0; i < n; i++)
		assignment[i] = i;
	awesome_shuffle(assignment, n);
}

int alg_sa(int **A, int **B, int n, int* assignment, int *best_assignment, float temp_max_fact = 0.5, float temp_min = 10, int p_max = 10, float alfa = 0.9) {
	//cout << awesome_score(A, B, n, assignment) << endl;

	memcpy(best_assignment, assignment, n * sizeof(int));
	int best_score = awesome_score(A, B, n, assignment);
	int curr_score = best_score;

	int l = pow(n, 1.5);
	float temp_curr = temp_max_fact * best_score;
	int steps = 1;
	int last_change = steps;

	while (steps - last_change < p_max*l && temp_curr > temp_min) {
		if (steps%l == 0)
			temp_curr = temp_curr * alfa;

		int a = rand() % n;
		int b = rand() % n;
		int score_diff = awesome_swap_score_diff(A, B, n, assignment, a, b);

		if (score_diff < 0) {
			swap(assignment[a], assignment[b]);
			curr_score += score_diff;
			if (curr_score < best_score) {
				best_score = curr_score;
				memcpy(best_assignment, assignment, n * sizeof(int));
				last_change = steps + 1;
			}
		}
		else {
			if (exp(-score_diff / temp_curr) >((float)rand()) / (float)RAND_MAX) {
				swap(assignment[a], assignment[b]);
				curr_score += score_diff;
			}
		}
		steps++;
	}
	return steps - 1;
	//return score; we should return struct with all necessary information: score, number of iteration etc - check what we will need
}


struct Neighbour {
	int i, j, diff;
};

bool sortbydiff(const Neighbour &a,
	const Neighbour &b)
{
	return (a.diff < b.diff);
}

vector< Neighbour > find_elite_neighbours(int **A, int **B, int n, int* assignment) {
	vector< Neighbour> elite_neighbours;
	for (int i = 0; i < n - 1; i++) {
		for (int j = i + 1; j < n; j++) {
			int score_diff = awesome_swap_score_diff(A, B, n, assignment, i, j);
			elite_neighbours.push_back({ i, j, score_diff });
		}
	}
	sort(elite_neighbours.begin(), elite_neighbours.end(), sortbydiff);

	return elite_neighbours;
}

int alg_TS(int **A, int **B, int n, int* assignment, int* assignment_best, int taboo_iters, int **Taboo, int p, int elite_nb) {
	int count_no_improvement = 0;
	int steps = 0;
	int l = pow(n, 1.5);
	memcpy(assignment_best, assignment, n * sizeof(int));
	int score = awesome_score(A, B, n, assignment);
	int best_score = score;
	bool elite_fail = true;
	vector< Neighbour > elite_neighbours;
	while (count_no_improvement < l*p) {
		if (elite_fail) {
			elite_neighbours = find_elite_neighbours(A, B, n, assignment);
			elite_fail = false;
		}
		int a = 0, b = 0;
		int min_score_diff = 0;
		for (int k = 0; k < elite_nb; k++) {
			int i = elite_neighbours[k].i;
			int j = elite_neighbours[k].j;

			int score_diff = awesome_swap_score_diff(A, B, n, assignment, i, j);

			if ((Taboo[i][j] == 0 || best_score > score + score_diff)
				&& (score_diff < min_score_diff)) {
				min_score_diff = score_diff;
				a = i; b = j;
			}

		}

		swap(assignment[a], assignment[b]);
		steps++;
		score = awesome_score(A, B, n, assignment);
		if (score < best_score) {
			best_score = score;
			memcpy(assignment_best, assignment, n * sizeof(int));
			count_no_improvement = 0;
		}
		else {
			count_no_improvement++;
			elite_fail = true;
		}
		if (a != b) {
			for (int i = 0; i < n - 1; i++) {
				for (int j = i + 1; j < n; j++) {
					Taboo[i][j] = Taboo[i][j] < 0 ? 0 : Taboo[i][j] - 1;
				}
			}
			Taboo[a][b] = taboo_iters;
			
		}

	}
	return steps;
}


//ARGUMENTS TO ADD:
//FILENAME
//METHOD TO USE (OR WE WILL ALWAYS USE ALL METHODS)
//DESTINATION DIRECTORY?

//ALSO we need to create a file with results (avg time, avg score max score, etc.) at the end of execution
int main()
{
	ifstream file;
	string filename = "chr12a";
	file.open("../instancje/" + filename + ".dat");
	int n;
	file >> n;
	int **A = new int*[n];
	int **B = new int*[n];
	int **Taboo = new int*[n];
	for (int i = 0; i < n; i++) {
		A[i] = new int[n];
		B[i] = new int[n];
		Taboo[i] = new int[n];
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
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			Taboo[i][j] = 0;;
		}
	}
	file.close();

	ofstream file_out;
	srand(time(NULL));
	int licznik = 0;
	int *assignment = new int[n];
	int *assignment_best = new int[n];
	/*
	for (int i = 0; i < n; i++)
	assignment[i] = i;
	awesome_shuffle(assignment, n);

	clock_t time0 = clock();
	do {
	//awesome_algorithm(A, B, n, assignment);
	//_test_swap_score(A, B, n, assignment);
	//alg_random(A, B, n); //example od random algorithm
	//alg_greedy_best(A, B, n);
	alg_greedy_better(A, B, n, assignment);
	getchar();
	licznik++;
	} while ((double)(clock() - time0) / CLOCKS_PER_SEC < 1
	|| licznik < 10); */

	clock_t time0;
	double time;
	/*
	//STEEPEST
	file_out.open("../wyniki/"+filename+"_s.txt", ios::out);
	double nseconds = 0.0; // żeby mieć dla randoma średni czas działania steepesta
	time0 = clock();
	for (int i = 0; i < 10; i++) {
	reroll_solution(n, assignment);
	file_out << awesome_score(A, B, n, assignment) << endl; //GS – wykres: jakość rozwiązania początkowego vs. jakość rozwiązania końcowego
	int steps = alg_steepest(A, B, n, assignment);
	for (int j = 0; j < n; j++)
	file_out << assignment[j] << " ";
	file_out << endl;
	file_out << awesome_score(A, B, n, assignment) << endl;
	file_out << steps << endl << endl;
	}
	time = (double)(clock() - time0) / CLOCKS_PER_SEC;
	file_out << time ;
	nseconds = time / 10;
	file_out.close();

	//GREEDY
	file_out.open("../wyniki/" + filename + "_g.txt", ios::out);
	time0 = clock();
	for (int i = 0; i < 10; i++) {
	reroll_solution(n, assignment);
	file_out << awesome_score(A, B, n, assignment) << endl; //GS – wykres: jakość rozwiązania początkowego vs. jakość rozwiązania końcowego
	int steps = alg_greedy(A, B, n, assignment);
	for (int j = 0; j < n; j++)
	file_out << assignment[j] << " ";
	file_out << endl;
	file_out << awesome_score(A, B, n, assignment) << endl;
	file_out << steps << endl << endl;
	}
	time = (double)(clock() - time0) / CLOCKS_PER_SEC;
	file_out << time;
	file_out.close();

	//RANDOM
	file_out.open("../wyniki/" + filename + "_r.txt", ios::out);
	time0 = clock();
	for (int i = 0; i < 10; i++) {
	reroll_solution(n, assignment);
	//file_out << awesome_score(A, B, n, assignment) << endl; //GS – wykres: jakość rozwiązania początkowego vs. jakość rozwiązania końcowego
	alg_random(A, B, n, assignment, assignment_best, nseconds);
	for (int j = 0; j < n; j++)
	file_out << assignment_best[j] << " ";
	file_out << endl;
	file_out << awesome_score(A, B, n, assignment_best) << endl << endl;
	}
	time = (double)(clock() - time0) / CLOCKS_PER_SEC;
	file_out << time;
	file_out.close();

	//HEURYSTYKA
	file_out.open("../wyniki/" + filename + "_h.txt", ios::out);
	time0 = clock();
	for (int i = 0; i < 10; i++) {
	reroll_solution(n, assignment);
	//file_out << awesome_score(A, B, n, assignment) << endl; //GS – wykres: jakość rozwiązania początkowego vs. jakość rozwiązania końcowego
	alg_heuristic(A, B, n, assignment);
	for (int j = 0; j < n; j++)
	file_out << assignment[j] << " ";
	file_out << endl;
	file_out << awesome_score(A, B, n, assignment) << endl << endl;
	}
	time = (double)(clock() - time0) / CLOCKS_PER_SEC;
	file_out << time;
	file_out.close();
	*/

	int p = 100;
	//TABOO SEARCH
	file_out.open("../wyniki/" + filename + "_ts.txt", ios::out);
	time0 = clock();
	for (int i = 0; i < 10; i++) {
		reroll_solution(n, assignment);
		//file_out << awesome_score(A, B, n, assignment) << endl; //GS – wykres: jakość rozwiązania początkowego vs. jakość rozwiązania końcowego
		int steps = alg_TS(A, B, n, assignment, assignment_best, n / 4, Taboo, p, n / 10);
		for (int j = 0; j < n; j++)
			file_out << assignment_best[j] << " ";
		file_out << endl;
		file_out << awesome_score(A, B, n, assignment_best)  << endl;
		file_out << steps << endl << endl;
	}
	time = (double)(clock() - time0) / CLOCKS_PER_SEC;
	file_out << time;
	file_out.close();

	//SA
	file_out.open("../wyniki/" + filename + "_sa.txt", ios::out);
	time0 = clock();
	for (int i = 0; i < 10; i++) {
		reroll_solution(n, assignment);
		//file_out << awesome_score(A, B, n, assignment) << endl; //GS – wykres: jakość rozwiązania początkowego vs. jakość rozwiązania końcowego
		int steps = alg_sa(A, B, n, assignment, assignment_best, 1, 10, p, 0.9);
		for (int j = 0; j < n; j++)
			file_out << assignment_best[j] << " ";
		file_out << endl;
		file_out << awesome_score(A, B, n, assignment_best) << endl;
		file_out << steps << endl << endl;
	}
	time = (double)(clock() - time0) / CLOCKS_PER_SEC;
	file_out << time;
	file_out.close();


	for (int i = 0; i < n; i++) {
		delete[] A[i];
		delete[] B[i];
		delete[] Taboo[i];
	}
	delete[] A;
	delete[] B;
	delete[] Taboo;
	delete[] assignment;
	delete[] assignment_best;

	//getchar();
	return 0;
}

