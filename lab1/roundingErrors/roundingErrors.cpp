#include <iostream>
#define precyzja double

precyzja xn(precyzja xnp, precyzja r) {
    return r * xnp * (1 - xnp);
}

int main()
{
    precyzja r = 4, x = 0.5673;
    for (int i = 0; i < 100; i++) {
        std::cout << x << "\n";
        x = xn(x, r);
    }
}