#include <stdio.h>
#include <conio.h>

int main()
{
    // int a = 11;
    // int *k = &a;   //读取地址
    // *k = 22;         //修改对应的值
    // printf("%p", k); //返回地址
    // printf("%d", *k); //返回地址对应的值

    // int a[6];
    // a[0] = 1;
    // printf("%p\n", a);     // 无需用&取地址
    // printf("%p\n", &a[4]); // []需要用&取地址

    // int func(int *a); //形参为指针，却可以接受数组作为实参
    // printf("%d\n", *a);
    // printf("%d\n", a[0]); //*a==a[0]

    // int b[5] = {1, 2, 3, 4, 5};
    // int a[];
    // b = a; //b为const 指针

    int i = 14;
    int j = 24;
    const int *p = &i;
    printf("%d\n", *p); // 14
    p = &j;             // 通过指向另一地址改变const指针
    printf("%d", *p);   // 24
}