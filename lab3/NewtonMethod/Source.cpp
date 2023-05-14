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
	result_t* find(double (*f)(double), double x_0, int max_iter, double error) {
		int i = 0;
		double x_n_plus_1 = x_0, x_n = x_0 + 0.0001, x_n_minus_1;
		while ((i < max_iter) && (abs(x_n_plus_1 - x_n) > error)) {
			x_n_minus_1 = x_n;
			x_n = x_n_plus_1;
			x_n_plus_1 = x_n - (*f)(x_n) * (0.0000001) / ((*f)(x_n) - (*f)(x_n - 0.0000001));
			i++;
		}
		result_t* act_result = new result_t;
		act_result->iteration_count = i;
		act_result->function_argument = x_n_plus_1;
		return act_result;
	}
}

int main() {
	std::cout << "Newton method" << "\n";
	zeroFinder::result_t* result = zeroFinder::find(&f1, 3 * M_PI / 2, 1000, 0.00000001);
	std::cout << "f1(x) = 0 for x = " << result->function_argument << "\n";
	std::cout << "f1(" << result->function_argument << ") = " << f1(result->function_argument) << "\n";
	std::cout << "Iteration count: " << result->iteration_count << "\n";
	delete result;
	result = zeroFinder::find(&f2, 0.2, 1000, 0.00000001);
	std::cout << "f2(x) = 0 for x = " << result->function_argument << "\n";
	std::cout << "f2(" << result->function_argument << ") = " << f2(result->function_argument) << "\n";
	std::cout << "Iteration count: " << result->iteration_count << "\n";
	delete result;
	result = zeroFinder::find(&f3, 1.1, 1000, 0.00000001);
	std::cout << "f3(x) = 0 for x = " << result->function_argument << "\n";
	std::cout << "f3(" << result->function_argument << ") = " << f3(result->function_argument) << "\n";
	std::cout << "Iteration count: " << result->iteration_count << "\n";
	delete result;
}