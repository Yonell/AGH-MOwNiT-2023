#include <iostream>
#include <chrono>

namespace LUFactorizer {

	int LUFactorize(int n, double** input) {
		for (int i = 0; i < n; i++) {
			for (int j = i+1; j < n; j++) {
				if (input[i][i] == 0) {
					throw std::runtime_error("Whole column is equal to 0");
				}
				double coeff = (input[j][i] / input[i][i]);
				input[j][i] = coeff;
				for (int k = i + 1; k < n + 1;k++) {
					input[j][k] -= coeff * input[i][k];
				}
			}
		}
	}

	double getLFromFactorized(int i, int j, double** factorized) {
		if (i == j) {
			return 1;
		}
		if (i > j) {
			return factorized[i][j];
		}
		return 0;
	}

	double getUFromFactorized(int i, int j, double** factorized) {
		if (i <= j) {
			return factorized[i][j];
		}
		return 0;
	}

	bool checkFactorization(int n, double** original, double** factorized) {
		double errorsum = 0;
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++) {
				double calculatedValue = 0;
				for (int ii = 0; ii < n; ii++) {
						calculatedValue += getLFromFactorized(i, ii, factorized) * getUFromFactorized(ii, j, factorized);
				}
				errorsum += abs(original[i][j] - calculatedValue);
			}
		}
		return errorsum < 0.00001;
	}
};

int main() {
	int n = 1000;

	std::cout << "Setting up the matrix...\n" << "Matrix size: " << n << "x" << n << "\n";
	double** input = (double**)malloc(n * sizeof(double*));
	double** original = (double**)malloc(n * sizeof(double*));
	for (int i = 0;i < n;i++) {
		input[i] = (double*)malloc((n + 1) * sizeof(double));
		original[i] = (double*)malloc((n + 1) * sizeof(double));
	}
	srand(123);

	for (int i = 0; i < n;i++) {
		for (int j = 0; j < n;j++) {
			input[i][j] = rand() / 10000.0;
			original[i][j] = input[i][j];
		}
	}


	std::cout << "Factorizing... \n";
	auto start = std::chrono::steady_clock::now();
	LUFactorizer::LUFactorize(n, input);
	auto stop = std::chrono::steady_clock::now();
	std::cout << "Factorized, operation duration: " << std::chrono::duration_cast<std::chrono::milliseconds>(stop - start).count() << "ms\n";


	std::cout << "Performing factorization check... \n";
	bool didItWork = LUFactorizer::checkFactorization(n, original, input);
	std::cout << "A = LU equality check: " << (didItWork ? "PASSED" : "FAILED") << "\n";


	std::cout << "Cleaning up...\n";
	for (int i = 0; i < n;i++) {
		free(input[i]);
	}
	free(input);
	for (int i = 0; i < n;i++) {
		free(original[i]);
	}
	free(original);
	return 0;
}