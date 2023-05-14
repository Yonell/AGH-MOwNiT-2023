#include <iostream>
#define _USE_MATH_DEFINES
#include <math.h>

double f1(double x) {
	return cos(x) * cosh(x) - 1;
}

double f2(double x) {
	return 1 / x - tan(x);
}

double f3(double x) {
	return pow(2.0, -x) + pow(exp(1), x) + 2 * cos(x) - 6;
}

namespace zeroFinder {
	struct result_t {
		double function_argument;
		int iteration_count;
	};

	double sgn(double x) {
		return (double)((0 < x) - (x < 0));
	}
	result_t* findBisection(double (*f)(double), double a, double b, double error) {
		if (sgn((*f)(a)) == sgn((*f)(b))) {
			throw std::runtime_error("Bad arguments");
		}
		int n_op = (int)ceil(log((b - a) / error) / log(2.0));
		int i = 0;
		double average = (a + b) / 2;
		for (i = 0; i < n_op; ++i) {
			if (sgn((*f)(a)) == sgn((*f)(average))) {
				a = average;
			}
			else if (sgn((*f)(average)) == sgn((*f)(b))) {
				b = average;
			}
			average = (a + b) / 2;
		}
		result_t* act_result = new result_t;
		act_result->iteration_count = i;
		act_result->function_argument = average;
		return act_result;
	}

	result_t* findSecant(double (*f)(double), double x_0, int max_iter, double error) {
		int i = 0;
		double x_n_plus_1 = x_0, x_n = x_0 + 0.0001, x_n_minus_1;
		while ((i < max_iter) && (abs(x_n_plus_1 - x_n) > error)) {
			x_n_minus_1 = x_n;
			x_n = x_n_plus_1;
			x_n_plus_1 = x_n - (*f)(x_n) * (x_n - x_n_minus_1) / ((*f)(x_n) - (*f)(x_n_minus_1));
			i++;
		}
		result_t* act_result = new result_t;
		act_result->iteration_count = i;
		act_result->function_argument = x_n_plus_1;
		return act_result;
	}
}

int main() {
	int iter = 0;
	zeroFinder::result_t* result = zeroFinder::findBisection(&f1, 3 * M_PI / 2, 2 * M_PI, 0.01);
	std::cout << "After bisection:" << "\n";
	std::cout << "f1(x) = 0 for x = " << result->function_argument << "\n";
	std::cout << "f1(" << result->function_argument << ") = " << f1(result->function_argument) << "\n";
	std::cout << "Iteration count: " << result->iteration_count << "\n";
	iter += result->iteration_count;
	result = zeroFinder::findSecant(&f1, result->function_argument, 100, 0.00000001);
	iter += result->iteration_count;
	std::cout << "After secant:" << "\n";
	std::cout << "f1(x) = 0 for x = " << result->function_argument << "\n";
	std::cout << "f1(" << result->function_argument << ") = " << f1(result->function_argument) << "\n";
	std::cout << "Iteration count sum: " << iter << "\n";
	delete result;
}