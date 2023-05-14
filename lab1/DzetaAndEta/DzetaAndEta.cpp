#include <iostream>
#include <math.h>

float dzetaForwSP(float s, int n) {
    float sum = 0;
    for (int k = 1; k <= n; k++) {
        sum += 1 / (powf(k, s));
    }
    return sum;
}

float dzetaBackSP(float s, int n) {
    float sum = 0;
    for (int k = n; k >= 1; k--) {
        sum += 1 / (powf(k, s));
    }
    return sum;
}

float etaForwSP(float s, int n) {
    float sum = 0;
    for (int k = 1; k <= n; k++) {
        sum += (k % 2 == 0 ? -1 : 1) / (powf(k, s));
    }
    return sum;
}

float etaBackSP(float s, int n) {
    float sum = 0;
    for (int k = n; k >= 1; k--) {
        sum += (k % 2 == 0 ? -1 : 1) / (powf(k, s));
    }
    return sum;
}

double dzetaForwDP(double s, int n) {
    double sum = 0;
    for (int k = 1; k <= n; k++) {
        sum += 1 / (powf(k, s));
    }
    return sum;
}

double dzetaBackDP(double s, int n) {
    double sum = 0;
    for (int k = n; k >= 1; k--) {
        sum += 1 / (powf(k, s));
    }
    return sum;
}

double etaForwDP(double s, int n) {
    double sum = 0;
    for (int k = 1; k <= n; k++) {
        sum += (k % 2 == 0 ? -1 : 1) / (powf(k, s));
    }
    return sum;
}

double etaBackDP(double s, int n) {
    double sum = 0;
    for (int k = n; k >= 1; k--) {
        sum += (k % 2 == 0 ? -1 : 1) / (powf(k, s));
    }
    return sum;
}

int main()
{
    std::cout.precision(24);
    double* arguments = (double*)malloc(5 * sizeof(double));
    arguments[0] = 2;
    arguments[1] = 3.66666666666666666666667;
    arguments[2] = 5;
    arguments[3] = 7.2;
    arguments[4] = 10;
    int* ns = (int*) malloc(5 * sizeof(int));
    ns[0] = 50;
    ns[1] = 100;
    ns[2] = 200;
    ns[3] = 500;
    ns[4] = 1000;
    for (int i = 0; i < 5; i++) {
        std::cout << "s = " << arguments[i] << "\n";
        for (int j = 0; j < 5; j++) {
            std::cout << "n = " << ns[j] << "\n";
            std::cout << "dzetaForwSP(s) = " << dzetaForwSP(arguments[i], ns[j]) << "; " << "dzetaBackSP(s) = " << dzetaBackSP(arguments[i], ns[j]) << "; "\
                << "etaForwSP(s) = " << etaForwSP(arguments[i], ns[j]) << "; " << "etaBackSP(s) = " << dzetaBackSP(arguments[i], ns[j]) << "; " << "\n";
            std::cout << "dzetaForwDP(s) = " << dzetaForwDP(arguments[i], ns[j]) << "; " << "dzetaBackDP(s) = " << dzetaBackDP(arguments[i], ns[j]) << "; "\
                << "etaForwDP(s) = " << etaForwDP(arguments[i], ns[j]) << "; " << "etaBackDP(s) = " << dzetaBackDP(arguments[i], ns[j]) << "; " << "\n";
        }
        std::cout << "\n";
    }
    // Z moich obserwacji wynika, ze sumowanie od konca daje troszke blizsze wyniki
    // Powodem tego jest prawdopodobnie to samo, co widzielismy w zadaniu 1
    // Sumowanie duzych wartosci z malymi powoduje duzy blad
    // Sumujac od tylu w kazdym przejsciu sumujemy wartosci blizej siebie
}