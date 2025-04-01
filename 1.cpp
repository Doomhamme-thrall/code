#include <iostream>
using namespace std;
int main()
{
    int a = 0;
    int b = (a = 5) ? 7 : 8;
    cout << b << endl;
}