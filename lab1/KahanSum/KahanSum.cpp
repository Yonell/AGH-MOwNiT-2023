#include <iomanip>
#include <iostream>
#include <chrono>

int main()
{
    std::cout.precision(12);
    float* tab = (float*)malloc(10000000 * sizeof(float));
    for (int i = 0; i < 10000000; i++) {
        tab[i] = 0.53125;
    }
    auto start = std::chrono::high_resolution_clock::now();
    float sum = 0;
    float err = 0;
    for (int i = 0; i < 10000000; ++i) {
        float y = tab[i] - err;
        float temp = sum + y;
        err = (temp - sum) - y;
        sum = temp;
    }
    auto stop = std::chrono::high_resolution_clock::now();
    std::cout << err << "\n";
    std::cout << sum << "\n";
    std::cout << 10000000 * 0.53125 << "\n";
    std::cout << (sum - (10000000 * 0.53125)) / (10000000 * 0.53125) * 100 << "%\n";
    std::cout << "Duration: " << std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count() << " micros\n";
    std::cout << "\n";
    for (int i = 0; i < 10000000; i++) {
        tab[i] = 0.50000119246;
    }
    start = std::chrono::high_resolution_clock::now();
    sum = 0;
    err = 0;
    for (int i = 0; i < 10000000; ++i) {
        float y = tab[i] - err;
        float temp = sum + y;
        err = (temp - sum) - y;
        sum = temp;
    }
    stop = std::chrono::high_resolution_clock::now();
    std::cout << err << "\n";
    std::cout << sum << "\n";
    std::cout << 10000000 * 0.50000119246 << "\n";
    std::cout << (sum - (10000000 * 0.50000119246)) / (10000000 * 0.50000119246) * 100 << "%\n";
    std::cout << "Duration: " << std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count() << " micros\n";
    free(tab);
                                        // Algorytm ten daje lepszy wynik, bo na biezaco poprawia bledy
                                        // err sluzy do przechowywania dotychczasowego bledu
                                        // Algorytm Kahana jest wolniejszy od algorytmu rekurencyjnego, a nawet od zliczania po kolei
                                        // Wynika to z wszystkich operacji wykonywanych po drodze
}