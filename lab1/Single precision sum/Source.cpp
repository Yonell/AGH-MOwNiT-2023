#include <iostream>
#include <iomanip>
#include <chrono>

float addRek(float number, int n) {
	if (n == 0) return 0;
	if (n == 1) return number;
	if (n % 2 == 0) return 2 * addRek(number, n / 2);
	else return 2 * addRek(number, n / 2) + number;
}

int main() {
	std::cout.precision(11);
	float* tab = (float*) malloc(10000000 * sizeof(float));
	float sum = 0;
	for (int i = 0; i < 10000000; i++) {
		tab[i] = 0.53125;
	}
	auto start = std::chrono::high_resolution_clock::now();
	for (int i = 0; i < 10000000; i++) {
		sum += tab[i];
	}
	auto stop = std::chrono::high_resolution_clock::now();
	std::cout << sum << "\n";   // Wynik            :  5 030 840
								// Oczekiwany wynik :  5 312 500
								// Blad bezwzgledny : -  281 660
								// Blad wzgledny    : -5.3018...%
								// Blad wynika z wyrownywania mantysy za kazdym przejsciem petli
								// Podczas dodawania z tej mniejszej liczby "uciekaja" bity
								// Z tego powodu tez widzimy niedoszacowanie liczby
	std::cout << "Duration: " << std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count() << " micros\n";
	
	sum = 0;
	for (int i = 0; i < 10000000; i++) {
		sum += tab[i];
		if (i % 25000 == 0) {
			std::cout << (sum - (i * 0.53125)) / (i * 0.53125) * 100 << "%\n";
		}
	}
	free(tab);
	start = std::chrono::high_resolution_clock::now();
	sum = addRek(0.53125, 10000000);
	stop = std::chrono::high_resolution_clock::now();
	std::cout << sum << "\n";	// Wynik			:  5 312 500
								// Wynik jest rowny oczekiwanej wartosci
								// Blad jest rowny 0
								// Blad zniknal/bardzo zmalal, poniewaz teraz program nie musi wyruwnywac mantysy przy kazdym przejsciu
								// Jedynym miejscem, w ktorym blad moze wystapic jest dodawanie w nieparzystym przypadku
	std::cout << "Duration: " << std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count() << " micros\n";
								// Czas wykonania algorytmu drastycznie sie zmniejszyl
	sum = addRek(0.50000119246, 10000000);
	std::cout << sum << "\n";
	std::cout << 10000000* 0.50000119246 << "\n";
								// Algorytm zwraca blad dla takiej liczby, z powodow podanych wyzej
	std::cout << (sum - (10000000 * 0.50000119246)) / (10000000 * 0.50000119246) * 100 << "%\n";
}