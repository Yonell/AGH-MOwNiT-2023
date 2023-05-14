#include <iostream>
#include <vector>
#include <armadillo>
#include <cstdlib>
#include <chrono>

class GaussJordanSolver {
	double** matrix = nullptr;
	int n;

	private:
		int findMax(int i) {
			int maxj = i;
			for (int j = i+1; j < n; j++) {
				if (abs(matrix[j][i]) > abs(matrix[maxj][i])) {
					maxj = j;
				}
			}
			return maxj;
		}

		void swapRows(int i, int j) {
			double* buff = matrix[i];
			matrix[i] = matrix[j];
			matrix[j] = buff;
			return;
		}

	public:

		GaussJordanSolver(int n, double** matrixarg) {
			this->n = n;
			matrix = (double**)malloc(n * sizeof(double*));
			for (int i = 0; i < n; i++) {
				matrix[i] = (double*)malloc((n + 1) * sizeof(double));
				memcpy(matrix[i], matrixarg[i], (n + 1) * sizeof(double));
			}
		}

		~GaussJordanSolver() {
			for (int i = 0; i < n; i++) {
				free(matrix[i]);
			}
			free(matrix);
		}

		double* solve() {
			for (int i = 0; i < n; i++) {
				int pivot = findMax(i);
				swapRows(i, pivot);
				for (int j = 0; j < n; j++) {
					if (j != i) {
						if (matrix[i][i] == 0) {
							throw std::runtime_error("Whole column is equal to 0");
						}
						double coeff = -(matrix[j][i] / matrix[i][i]);
						matrix[j][i] = 0;
						for (int k = i + 1; k < n + 1;k++) {
							matrix[j][k] += coeff * matrix[i][k];
						}
					}
				}
			}
			for (int i = 0; i < n; i++) {
				matrix[i][n] /= matrix[i][i];
				matrix[i][i] = 1;
			}
			double* result = (double* )malloc(n * sizeof(double));
			for (int i = 0; i < n; i++) {
				result[i] = matrix[i][n];
			}
			return result;
		}
};

int main() {
	int n = 2000;

	std::cout << "Setting up the matricies... \n" << "Matrix size: " << n << "x" << n + 1 << "\n";
	double** input = (double**)malloc(n * sizeof(double*));
	for (int i = 0;i < n;i++) {
		input[i] = (double*)malloc((n + 1) * sizeof(double));
	}
	arma::mat A(n, n);
	arma::vec B(n);

	srand(123);
	for (int i = 0; i < n;i++) {
		for (int j = 0; j < n;j++) {
			input[i][j] = rand() / 10000000.0;
			A.at(i,j) = input[i][j];
		}
	}
	for (int i = 0; i < n;i++) {
		input[i][n] = rand() / 1000.0;
		B.at(i) = input[i][n];
	}
	std::cout << "Matricies are set up!\n";


	std::cout << "Starting the custom solver...\n";
	GaussJordanSolver* matrix = new GaussJordanSolver(n,input);
	auto start = std::chrono::steady_clock::now();
	double* result = matrix->solve();
	auto end = std::chrono::steady_clock::now();
	std::cout << "GaussJordanSolver done, time elapsed: " << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << "ms\n";


	std::cout << "Starting Armadillo...\n";
	start = std::chrono::steady_clock::now();
	arma::vec Ans = arma::solve(A, B);
	end = std::chrono::steady_clock::now();
	std::cout << "Armadillo done, time elapsed: " << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << "ms\n";


	std::cout << "Performing equality check...\n";
	bool gitgut = true;
	for (int i = 0; i < n; i++) {
		if (Ans[i] - result[i] > 0.0001)
		{
			gitgut = false;
			break;
		}
	}
	std::cout << "Equality check: " << (gitgut ? "PASSED" : "FAILED") << "\n";


	std::cout << "Cleaning up...\n";
	free(result);
	for (int i = 0;i < n;i++) {
		free(input[i]);
	}
	free(input);
	return 0;
}