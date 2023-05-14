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
	result_t* find(double (*f)(double), double a, double b, double error) {
		if (sgn((*f)(a)) == sgn((*f)(b))) {
			throw std::runtime_error("Bad arguments");
		}
		int n_op = (int)ceil(log((b - a) / error) / log(2.0));
		int i=0;
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
}

int main() {
	zeroFinder::result_t* result = zeroFinder::find(&f1, 3 * M_PI / 2, 2 * M_PI, 0.00000001);
	std::cout << "f1(x) = 0 for x = " << result->function_argument << "\n";
	std::cout << "f1(" << result->function_argument << ") = " << f1(result->function_argument) << "\n";
	std::cout << "Iteration count: " << result->iteration_count << "\n";
	delete result;
	result = zeroFinder::find(&f2, 0, M_PI / 2, 0.00000001);
	std::cout << "f2(x) = 0 for x = " << result->function_argument << "\n";
	std::cout << "f2(" << result->function_argument << ") = " << f2(result->function_argument) << "\n";
	std::cout << "Iteration count: " << result->iteration_count << "\n";
	delete result;
	result = zeroFinder::find(&f3, 1, 3, 0.00000001);
	std::cout << "f3(x) = 0 for x = " << result->function_argument << "\n";
	std::cout << "f3(" << result->function_argument << ") = " << f3(result->function_argument) << "\n";
	std::cout << "Iteration count: " << result->iteration_count << "\n";
	delete result;
}